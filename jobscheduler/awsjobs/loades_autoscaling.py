# encoding=utf8
from __future__ import with_statement
import datetime
import logging
import redis
import json
import socket
import threading
import time
import pymysql
import os
from flask import Flask, session, jsonify, escape, request, g, config, g, abort, flash, render_template, make_response
from flask_httpauth import HTTPBasicAuth
from contextlib import closing
import sqlite3
from flask import url_for, redirect
from flask_restful import Resource, Api, abort
from flask_restful import reqparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

'''
要理解flask的运行过程就在请求中打断点，然后就可以看到一个核心的文件--app.py中有很多的变量，
将断点打在dispatch_request函数中，可以看到很多的有价值的信息

'''
# from sqlalchemy.dialects.mysql import pymysql

try:
    import thread
except:
    import _thread
from jobscheduler.awsjobs.BaseJob import Jobs
# filename = os.path.join(app.instance_path, 'application.cfg')
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
from jobscheduler.awsjobs.instance import settings
from flask_sqlalchemy import SQLAlchemy
parser = reqparse.RequestParser()
#import pymysql
app = Flask(__name__)
#app.config.from_pyfile('./instance/settings.py')
app.config.from_object(settings.TestConfig)
app.config.from_object(__name__)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
'''
下面代码用来将flask的session添加到redis，数据库等地方
'''
import redis
from flask import Flask, session
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_PERMANENT'] = False  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379')  # 用于连接redis的配置
Session(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


# copy from https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

def verify_token(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=token).first()
        if not user:
            return False
    g.user = user
    return True

def connect_db():
    # rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    # return sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    # return pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='root',db='test')
    print(app.config)
    return pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='root',db='test')
    # return pymysql.connect(host=app.config['mysqlhost'],port= app.config['mysqlport'],user =app.config['mysqluser'] ,passwd=app.config['mysqlpassword'],db=app.config['mysqldb'])

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/login')
@auth.login_required
def get_auth_token():
    handler = logging.FileHandler('flask2.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.logger.info(request.authorization)
    print(request.authorization)
    print(g.user.username)
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('./instance/create.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
#
#
#这段代码会引起问题： File "G:\program\Python\lib\site-packages\flask\app.py", line 2309, in __call__
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('./instance/create.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

def varify_url_token(f):
    def decorate(*args,**kwargs):
        global parser
        args = parser.parse_args()
        parser.add_argument('token', location=['json', 'args'])
        query_param = dict(args)
        token = ''
        if 'token' not in query_param:
            token = request.args.to_dict()['token']
        else:
            token = query_param['token']
        print(token)
        if verify_token(token):
            return f(*args,**kwargs)
        else:
            return 'auth failed'
    return decorate

@app.route('/deco')
@varify_url_token
def urltoken_test():
    resp = make_response('success ',200)
    resp
    return 'decorate work well'

@app.route('/clientinfo')
def client_info():
    req = request
    print(request.path)
    print(request.remote_addr)
    print(request.user_agent)

#$ curl -u eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0MjY0MzAwOSwiZXhwIjoxNTQyNjQzNjA5fQ.eyJpZCI6NH0.Y5VW8tBMyXzYffkW_fA4o3ibSad7YHLsC8mi1OT0Kow:unused -i -X GEThttp://localhost:8888/
#这个用curl可以顺利请求，但是用post 的bearer token就不成功
@app.route('/')
#@auth.login_required#这个要靠近函数定义，放在上面的话会无法生效
def hello_world():
    # # 获取 url 参数内容
    # x = request.args.get("x")
    # # 获取 form 表单内容
    # y = request.form.get("y")
    # # 获取 http 头部内容
    # z = request.headers.get("z")
    # # 获取json格式的body，返回直接就是dict类型
    # content = request.get_json(silent=True)

    global parser
    args = parser.parse_args()
    parser.add_argument('token', location=['json', 'args'])
    query_param = dict(args)
    cookies = request.cookies.get('Name')
    token = ''
    if 'token' not in query_param:
        token = request.args.to_dict()['token']
    else:
        token = query_param['token']
    print(token)
    outdate = datetime.datetime.today() + datetime.timedelta(days=30)
    if verify_token(token):
        resp = make_response('auth success', 200)
        resp.header['url'] = 'xxx'
        resp.set_cookie('_gid','xxxxxddddddss2',expires=outdate)
        #resp.delete_cookie('_gid')
        return resp
        #return 'auth success'
    return "hello world"
    # response = redirect(url_for('asset', asset_id=info, page=2, tag='balances'))
    # return response
@app.route('/sessioninfo')
def getsession():
    print(session.get('uname'))
    return session.set('username','teeeeeeeeeeeeeeeeeeeeeest')

    pass




@app.route('/getjob', methods=['GET', 'POST'])
# @verify_password(get_auth_token)
def getjob():
    if request.method == 'POST':
        # return  "this is a post request"
        print(request.get_data())
        request_data = json.loads(request.get_data())
        country = request_data['country']
        ip = request_data['ip']
        return json.dumps(job.get_job(country, ip))
    else:
        return " this is a get request"


@app.route('/setjob', methods=['GET', 'POST'])
def setjob():
    if request.method == 'POST':
        # return  "this is a post request"
        print(request)
        return request.get_data()
    else:
        return " this is a get request"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # return  "this is a post request"
        #session['username'] = request.form['username']
        print(request.get_data())
        request_data = json.loads(request.get_data())
        ip = request_data['serverip']

        return job.register(ip)
    else:
        return " this is a get request"

@app.route('/finshreport', methods=['GET', 'POST'])
def finshreport():
    if request.method == 'POST':
        # return  "this is a post request"
        print(request)  # <Request 'http://127.0.0.1:5000/getjob' [POST]>
        return request.get_data()  # this is a string, not a dict
    else:
        return " this is a get request"

    #return redirect(url_for('status'))

@app.route('/status', methods=['GET', 'POST'])
def jobstatus():
    if request.method == 'GET':
        runing_job = job.running_job_list
        finshed_job = job.finshed_job_list
        server_list = job.server_list
        failed_list = job.failed_list
        return render_template(
            # 渲染模板语言
            'jobstatus.html',
            job='hello world',
            failed=failed_list,
            running=runing_job,
            finshed=finshed_job,
            servers=server_list
        )
    else:
        return " please use get method"

# step1 定义过滤器
def do_listreverse(li):
    temp_li = list(li)
    temp_li.reverse()
    return temp_li

# step2 添加自定义过滤器
app.add_template_filter(do_listreverse, 'listreverse')

if __name__ == '__main__':
    job = Jobs()
    #init_db()
    app.run(host='0.0.0.0', port=8888, debug=True)
