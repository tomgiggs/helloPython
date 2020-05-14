#encoding=utf8

import paho.mqtt.client as mqtt
import time

# host = "192.168.9.129"
# host ='192.168.212.73'
# port = 1883  http://mqtt.edbox-dev.101.com:8086/

host = "172.24.140.219"
port = 1883

def on_connect(client,userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("server/videoEditor/userTask/userId/930516")


def on_message(client, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

def send():
    client = mqtt.Client()

    # client.username_pw_set('admin','public')
    client.username_pw_set('edbox_client','kkclient2018')
    # client.username_pw_set('1000212','adswew2')
    # client.username_pw_set('redis001','passwd')
    client.connect(host, port, 60)
    for i in range(100):
        time.sleep(2)
        client.publish("server/videoEditor/userTask/userId/930516","hello i am producer python 131", 1)
    client.loop_forever()


if __name__ == '__main__':
    send()
