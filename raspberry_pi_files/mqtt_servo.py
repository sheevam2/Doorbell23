
from time import *
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqtt

kit = ServoKit(channels=16)
kit.servo[8].angle = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/servo")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # Perform desired action based on the received message
    if msg.payload.decode() == 'This is lock':
        # Trigger the lock action on the Raspberry Pi
        # Your lock action code goes here
        print("Lock action triggered")
    elif msg.payload.decode() == 'This is unlock':
        # Trigger the unlock action on the Raspberry Pi
        # Your unlock action code goes here
        print("Unlock action triggered")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.220", 1884, 60)

client.loop_forever()



