import human_curl
from human_curl.async import AsyncClient
from human_curl.core import Request
import pycurl
import socket


def success_call(response, **kwargs):
    print(response.content)
    pass

def fail_call(response, **kwargs):
    print(response.content)

def get_ip():
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    print(ip)
#get_ip()

url = 'https://blog.csdn.net/fly_zhyu/article/details/76408158'
client = AsyncClient(success_callback=success_call, fail_callback=fail_call)
request = Request(network_interface=get_ip(),method='GET', url=url)
print(request.response)
request.send()
response = request.response
print(response.content)
print(request.make_response())
# request._network_interface='172.17.35.241'
# #
# opener = pycurl.Curl()
# da = {'network_interface': get_ip(),}
#
# client.add_handler(**da)
# #client.configure_opener(opener, data=da)
# client.get(url)
# client.start()
