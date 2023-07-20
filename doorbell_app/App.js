import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button, TouchableOpacity, ScrollView} from 'react-native';
import React, { useState, useEffect, useRef } from 'react'; // Import useState and useEffect from 'react'
//import { MqttClient, MqttConnectionState } from 'sp-react-native-mqtt';
//import Mqtt from 'react_native_mqtt';
//import mqtt from 'mqtt';
//import ws from 'ws';
//const Mqtt = require('react_native_mqtt');

//import  paho;
import { Client, Message } from 'react-native-paho-mqtt';

// const brokerUrl = '192.168.1.220';
// const clientId = '2023';
// const client = Paho.MQTT.Client(brokerUrl, Number(1883), "/", clientId);
//const client = new MqttClient('mqtt://192.168.1.220:1883');

//const client = new Mqtt.Client('mqtt://192.168.1.220:1883');

// client.connect({
//   username: 'doorbell_mqtt',
//   password: 'Doorbell123!',
//   clientId: '2023',
// });

// client.on('connect', () => {
//   console.log('Connected to MQTT broker');
// });

export default function App() {

  // const brokerUrl = "192.168.1.220";
  // const clientId = "2023";
  // const client = Paho.Client(brokerUrl, Number(1883), "/", clientId);

  //const client = new Client({ uri: 'ws://0.0.0.0:1883/ws', clientId: '2023'});
  //const client = new Mqtt.Client('0.0.0.0:1883');

const [connected, setConnected] = React.useState(false);
  
const storage = {
  setItem: () => {},
  getItem: () => {},
  removeItem: () => {},
};

const client = new Client({
  uri: 'ws://192.168.1.220:1884/mqtt',
  clientId: 'hi3333',
  storage: storage,
});

React.useEffect(() => {

  client.connect()
    .then(() => {
      console.log('Connected to MQTT broker');
      // Subscribe to the desired MQTT topic
      setConnected(true)
      client.subscribe('test/servo');
    })
    .catch((error) => {
      setConnected(false)
      console.log('Connection failed:', error);
    });
    
}, []);

const RectangularButton = ({ title, onPress }) => {
  return (
    <TouchableOpacity style={styles.buttonContainer} onPress={onPress}>
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );
};

const RectangularButton2 = ({ title, onPress }) => {
  return (
    <TouchableOpacity style={styles.buttonContainer2} onPress={onPress}>
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );
};

const LogScreen = ({ messages }) => {
  return (
    <ScrollView style={styles.logContainer} inverted>
      {messages.map((message, index) => (
        <Text key={index} style={styles.logText}>
          {message}
        </Text>
      ))}
    </ScrollView>
  );
};

const [messages, setMessages] = useState([]);

/*const handleButtonPress = () => {
  const message = 'Button pressed!';
  // Update the messages state with the new message
  setMessages((prevMessages) => [...prevMessages, message]);
};*/

  
const lock_button = () => {
  //const message = new Message('This is lock');  // Replace 'your message' with the desired message payload
  //message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  //client.send(message);
  const message1 = 'Lock Button Pressed!';
  setMessages((prevMessages) => [message1, ...prevMessages]);
};

const unlock_button = () => {
  //const message = new Message('This is unlock');  // Replace 'your message' with the desired message payload
  //message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  //client.send(message);
  const message1 = 'Unlock Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const FR_button = () => {
  const message1 = 'Facial Recognition Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const newface_button = () => {
  const message1 = 'New Face Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const connect_button = () => {
  const message1 = 'Connect Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};


  return (
    <View style={styles.container}>
      <Text style={styles.title}>DOORBELL PROJECT </Text>
      {connected ? (
        <Text style={styles.connectedText}>Status: Connected</Text>
      ) : (
        <Text style={styles.disconnectedText}>Status: Disconnected</Text>
      )}
      <View style = {styles.container2}>
      <RectangularButton2 title = 'Lock' onPress={lock_button}/>
      <RectangularButton2 title = 'Unlock' onPress={unlock_button}/>
      </View>
      <View style = {styles.container3}>
      <RectangularButton title = "Start Facial Recognition" onPress={FR_button}/>
      <RectangularButton title = "Add New Face" onPress={newface_button}/>
      <RectangularButton title = 'Connect' onPress={connect_button}/>
      <LogScreen messages={messages} />
      </View>
      <StatusBar style="auto" />
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131414',
    alignItems: 'center',
    justifyContent: 'center',
    
  },
  container2: {
    flexDirection: 'row',
    backgroundColor: '#131414',
    justifyContent: 'space-between',
    padding: 10,
    
    position: 'absolute',
    top: 200,
  },

  container3: {
    backgroundColor: '#131414',
    justifyContent: 'center',
    position: 'absolute',
    top: 320,
  },

  title: {
    fontSize: 32,
    fontWeight: 'bold',
    position: 'absolute',
    top: 40,
    marginTop: 40,
    color: '#2b87ed',
    textAlign: 'center'
  },
  connectedText: {
    fontSize: 18,
    color: 'green',
    position: 'absolute',
    top: 130,
    marginTop: 10,
    fontWeight: 'bold',
  },
  disconnectedText: {
    fontSize: 18,
    color: 'red',
    position: 'absolute',
    top: 130,
    marginTop: 10,
    fontWeight: 'bold',
  },
  button1: {
    position: 'absolute',
    top: 40,
  },

  buttonContainer: {
    backgroundColor: '#2b87ed',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    justifyContent: 'center', // Center the text vertically
    alignItems: 'center', // Center the text horizontally
    marginBottom: 30,
    width: 350,
    height: 90,
  },

  buttonContainer2: {
    
    backgroundColor: '#2b87ed',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    justifyContent: 'center', // Center the text vertically
    alignItems: 'center', // Center the text horizontally
    marginBottom: 30,
    marginHorizontal: 20,
    width: 155,
    height: 70,
  },
  
  buttonText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },

  logContainer: {
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    padding: 10,
    marginTop: 20,
    width: 350, 
    height: 85,
    maxHeight: 200,
    overflow: 'scroll',
  },
  logText: {
    color: '#333',
    fontSize: 16,
    marginBottom: 5,
  },
  
  
});
