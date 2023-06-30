import asyncio
import paho.mqtt.client as mqtt

async def connect_mqtt():
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    broker_address = "192.168.1.220"
    broker_port = 1884

    # Set the MQTT broker's WebSocket URI
    websocket_uri = f"ws://{broker_address}:{broker_port}/mqtt"

    # Connect to the MQTT broker over WebSocket
    client.ws_set_options(path="/mqtt")  # Set the WebSocket path
    client.connect(broker_address, broker_port, 60)

    # Start the MQTT client's network loop
    client.loop_start()

async def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("test/servo")

async def on_message(client, userdata, msg):
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

# Run the connect_mqtt coroutine
asyncio.run(connect_mqtt())