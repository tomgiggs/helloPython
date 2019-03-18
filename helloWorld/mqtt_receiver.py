import paho.mqtt.client as mqtt

host = "192.168.254.129"
port = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("app2dev/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def receive():
    client = mqtt.Client()
    client.username_pw_set('admin','public')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 60)
    client.loop_forever()

if __name__ == '__main__':
    receive()