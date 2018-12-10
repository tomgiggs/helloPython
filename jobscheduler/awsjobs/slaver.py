import requests
import json
import traceback
import socket


master_ip = "127.0.0.1:5000"

def get_ip_address():
    servername = socket.getfqdn(socket.gethostname())
    ipaddr = socket.gethostbyname(servername)
    print servername
    print ipaddr
    return ipaddr

ip = get_ip_address()
data = {'serverip': ip,}

req = requests.post('http://'+master_ip+'/register',json=data)
print(req.text)

