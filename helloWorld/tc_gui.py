# encoding=utf8
'''
打包成exe文件使用这个命令：D:\program\python27\Scripts\pyinstaller.exe -F -p D:\program\python27\Lib  tc_gui.py
使用python3.6 时会出现问题：OSError: [WinError 193] %1 不是有效的 Win32 应用程序。
'''
from tkinter import *  # python3.2之前使用这个来导入：from TKinter import *
import hashlib, hmac, json, time, os
from datetime import datetime
import requests
import base64
import uuid
import struct
# from distutils.core import setup
# import py2exe

root = Tk()
root.title("文字转语音-power-by-tencentCloud")
root.geometry('120x50')

# 密钥参数
secret_id = ""
secret_key = ""

service = "tts"
host = "tts.tencentcloudapi.com"
endpoint = "https://" + host
region = "ap-guangzhou"
action = "TextToVoice"
version = "2019-08-23"
algorithm = "TC3-HMAC-SHA256"
ct = "application/json; charset=utf-8"

signed_headers = "content-type;host"
timestamp = int(time.time())
date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
credential_scope = date + "/" + service + "/" + "tc3_request"


def wav_merge(file1, file2, targe_file):
    if not targe_file:
        targe_file = str(int(time.time())) + ".wav"
    with open(file1, 'rb+') as file:
        data1 = file.read()
    with open(file2, 'rb+') as file:
        data2 = file.read()
    data_info = data1[:44]  # 复制帧头参考
    data_out = data1[44:] + data2[44:]  # 将两个音频的数据帧合并（都是相同格式）
    data_info = data_info[:4] + struct.pack('<L', len(data_out) + 44) + data_info[8:]  # 更新WAV文件的总byte数（两个文件数据帧和+44）
    data_info = data_info[:40] + struct.pack('<L', len(data_out)) + data_info[44:]  # 更新WAV文件的数据byte数（两个文件数据帧和）
    # *** 生成合并后的WAV文件 *** #
    with open(targe_file, 'wb') as f:
        f.write(data_info + data_out)
    print('合并完成')
    os.remove(file1)
    os.remove(file2)
    return targe_file


# ************* 步骤 1：拼接规范请求串 *************
def getReqStr(method, queryStr, queryData):
    http_request_method = method
    canonical_uri = "/"
    canonical_querystring = queryStr
    payload = json.dumps(queryData)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)

    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)
    # print(canonical_request)
    return canonical_request


# ************* 步骤 2：拼接待签名字符串 *************
def getUnsignStr(params):
    canonical_request = getReqStr('POST', '', params)
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)
    # print(string_to_sign)
    return string_to_sign


# ************* 步骤 3：计算签名 *************
# 计算签名摘要函数
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_auth_str(params):
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    string_to_sign = getUnsignStr(params)
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    # print(signature)
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)
    # print(authorization)
    return authorization


def process(text):
    print(text)
    params = {
        "Text": text,
        "SessionId": str(uuid.uuid4()),
        "Volume": 1,
        "Speed": 0.8,
        "ProjectId": 0,
        "ModelType": 1,
        "VoiceType": 6,
        "PrimaryLanguage": 1,
        "SampleRate": 16000,
        "Codec": "wav"
    }
    global timestamp, date, credential_scope
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    dateStr = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d-%H-%M-%S")
    credential_scope = date + "/" + service + "/" + "tc3_request"
    head = {
        "Authorization": get_auth_str(params),
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region,
    }

    result = requests.post(endpoint, json=params, headers=head)
    print(result.content)
    b64_str = json.loads(result.content)['Response']['Audio']
    audio_output = open(dateStr + '.wav', 'wb')
    audio_output.write(base64.b64decode(b64_str))
    audio_output.close()
    print("tts过程完成")
    return dateStr + ".wav"


def main(text,output):
    loc = 0
    count = int(len(text) / 100)
    latestFilename = ''
    for i in range(count + 1):
        newFileName = process(text[loc:loc + 100])
        if i > 0:
            if i == count:
                latestFilename = wav_merge(latestFilename, newFileName, output + '.wav')
            else:
                latestFilename = wav_merge(latestFilename, newFileName, '')
        else:
            latestFilename = newFileName
        loc += 100


def start(*args, **kwargs):
    textBody = t.get(1.0, 999.0)
    filename = output_file_name.get()
    print(textBody, filename)
    result = main(textBody, filename)
    t2.insert(1.0, '转换完成')


Label(root, text="待转换文字：").grid(row=0, sticky=W)
t = Text(root, height=20, width=100, setgrid=True)
t.grid(row=0, column=2)

Label(root, text="输出文件名称：").grid(row=1, sticky=W)
output_file_name = StringVar()
Entry(root, textvariable=output_file_name).grid(row=1, column=2, sticky=W)

Label(root, text="进度：").grid(row=3, sticky=W)
t2 = Text(root, height=1, width=10, setgrid=True)
t2.grid(row=3, column=1)

Button(root, text="开始", bg="green", command=start).grid(row=4, column=2)

root.mainloop()


# setup(console=('tc_gui.py'))