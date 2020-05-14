#encoding=utf8
import os
import argparse
try:
    import paho.mqtt.client as mqtt
except:
    os.system('pip install paho-mqtt')
# host = "192.168.212.73"
# # host = "192.168.9.129"
# port = 1893

host = "172.24.140.219"
# port = 1893
port = 8083


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc),userdata,flags)
    client.subscribe("server/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def receive():
    client = mqtt.Client(transport='websockets')
    # client.username_pw_set('1000212','adswew2')
    # client.username_pw_set('edbox_client_inland', 'kkclient2018.inland')
    client.username_pw_set('admin', 'public')
    # client.username_pw_set('1000286','2323sd')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 60)
    client.loop_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=3306, type=int)
    parser.add_argument('--user', default='root')
    parser.add_argument('--passwd', help='user password')
    parser.add_argument('--daybefore', default=14, type=int)
    args = parser.parse_args()
    receive()
