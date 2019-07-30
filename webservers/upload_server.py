# encoding=utf8
from __future__ import with_statement
import json
import time
import traceback
import os
from flask import Flask
from flask import Flask, session, jsonify, send_from_directory
from flask_restful import request
from flask_restful import Resource, Api, abort
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))



upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "upload")
if os.path.exists(upload_path):
    print('upload dir exist')
else:
    os.mkdir(upload_path)
    print('mkdir upload dir success')

parser = reqparse.RequestParser()

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)),'upload.html')

def unzip_deploy(filename):
    os.system('unzip upload/' + filename)
    os.system('mv Edbox_JSLibs libs')
    unix_time = str(int(time.time()) * 100)
    os.system('mv 235/libs 235/xxxx && mv 234/libs 234/xxxx &&  mv 233/libs 233/xxxx '.replace('xxxx',unix_time))
    os.system('cp -R libs 235/ && cp -R libs 234/ && mv libs 233/')



@app.route('/upload', methods=['POST'])
def upload():
    # if request.method == 'POST':
    if request.method == 'POST':
        f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
        fname = f.filename
        if f:  # 判断是否是允许上传的文件类型
            print(fname)
            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            unix_time = str(int(time.time())*100)
            new_filename = 'upload_' + unix_time + '.' + ext  # 修改上传的文件名
            f.save(os.path.join(upload_path, new_filename))  # 保存文件到upload目录
            try:
                unzip_deploy(new_filename)
            except:
                traceback.print_exc()
                return "deploy file error"
            result = {'oldfile': fname,'newfile': new_filename, 'success': 1}
            return json.dumps(result)
        else:
            result = {'file': fname, 'success': 0,'reason':'file type illegal'}
            return json.dumps(result)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)