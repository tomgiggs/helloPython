import paho.mqtt.client as mqtt
import time
host = "192.168.9.131"
port = 1883

def on_connect(client,userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("app2dev/")


def on_message(client, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

def send():
    client = mqtt.Client()
    client.username_pw_set('admin','public')

    client.connect(host, port, 60)
    for i in range(100):
        time.sleep(2)
        client.publish("app2dev/","hello i am producer python 131", 1)
    client.loop_forever()


if __name__ == '__main__':
    send()
