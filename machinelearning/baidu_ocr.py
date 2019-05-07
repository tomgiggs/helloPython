from aip import AipOcr
import json
import os
import sys
#在做tesseract的时候发现了百度的这个api,还是很好用的，搞个小工具自己用挺好的。需要安装baudu aip Python包pip3 install baidu-aip
#api注册地址 https://console.bce.baidu.com/ai/#/ai/ocr/app/detail~appId=963935

config = {
    'appId': '',
    'apiKey': '',
    'secretKey': ''
}

client = AipOcr(**config)
def read_dir():
    file_list = os.listdir('./images')
    for image in file_list:
        print(img_to_str('./images/'+image))

def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()

def img_to_str(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    print(json.dumps(result))
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])

# print(img_to_str('./test.png'))
read_dir()