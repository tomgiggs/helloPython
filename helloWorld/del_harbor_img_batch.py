#encoding=utf8
import requests
import json
import time
harbor_host = '192.168.19.55'
# client = requests.session()
def del_all():
    for i in range(10):
        get_img_list(5,i,25)
        # time.sleep(1)
    pass

def get_img_list(proj_id,page,size):
    url = 'http://'+harbor_host+'/api/repositories'
    params = {
        "page":page,
        "page_size":size,
        "project_id":proj_id
    }
    result = requests.get(url,params,auth=('admin', 'xxx.com'))
    if result.status_code == 200:
        body = json.loads(result.content)
        print(body)
        for img in body:
            del_img(img)


def del_img(img_info):
    img_name = img_info['name']
    product_info= img_name.split('_')
    # print(img_name,product_info)
    if len(img_name) in (56,57,61,62,70) and len(product_info)==6:
        url = 'http://' + harbor_host + '/api/repositories/'+img_name
        print(url)
        requests.delete(url,auth=('admin', 'harbor@edbox.101.com'))
        # print('this is img is to be deleted')


# get_img_list(7)
for i in range(5):
    del_all()
    time.sleep(2)
