import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button } from 'react-native';
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

client.connect()
  .then(() => {
    console.log('Connected to MQTT broker');
    // Subscribe to the desired MQTT topic
    client.subscribe('test/servo');
  })
  .catch((error) => {
    console.log('Connection failed:', error);
  });


const lock_button = () => {
  const message = new Message('This is lock');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
};

const unlock_button = () => {
  const message = new Message('This is unlock');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
};


  return (
    <View style={styles.container}>
      <Text>Unlock the Door!</Text>
      <Button title="Lock" onPress={lock_button}/>
      <Button title="Unlock" onPress={unlock_button}/>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
