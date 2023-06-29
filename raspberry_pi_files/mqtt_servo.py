import asyncio
import websockets
import paho.mqtt.client as mqtt

async def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    websocket_uri = "ws://192.168.1.220:1884/mqtt"  # Replace with your WebSocket URI

    # Connect to the MQTT broker over WebSocket
    transport, protocol = await websockets.client.connect(websocket_uri)

    # Set the transport to the MQTT client
    client._transport = transport

    # Start the MQTT client's event loop
    client.loop_start()

    # Wait for the connection to establish
    while not client.is_connected():
        await asyncio.sleep(0.1)

    # Subscribe to the desired MQTT topic
    client.subscribe("test/servo")

async def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

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