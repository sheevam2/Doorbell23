import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button, TouchableOpacity, ScrollView, Modal, TextInput, Image} from 'react-native';
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

const storage = {
  setItem: () => {},
  getItem: () => {},
  removeItem: () => {},
};

/*const storage2 = {
  setItem: () => {},
  getItem: () => {},
  removeItem: () => {},
};*/

const client = new Client({
  uri: 'ws://192.168.1.220:1884/mqtt',
  //uri: 'ws://192.168.1.251:1885/mqtt',
  clientId: 'hi3333',
  storage: storage,
  /*messageArrived: (message) => {
    console.log("HI")
    console.log('Received Message:', message);
    const payloadBytes = message.payloadBytes;
    const payloadString = String.fromCharCode.apply(null, new Uint8Array(payloadBytes));
    console.log(payloadString);
  },*/
});

/*const client2 = new Client({
  uri: 'ws://192.168.1.251:1885/mqtt', // Replace with the URI of your second broker
  clientId: 'your_client_id',   // Choose a unique client ID for the second broker
  storage: storage2,
});*/
 

export default function App() {

  // const brokerUrl = "192.168.1.220";
  // const clientId = "2023";
  // const client = Paho.Client(brokerUrl, Number(1883), "/", clientId);

  //const client = new Client({ uri: 'ws://0.0.0.0:1883/ws', clientId: '2023'});
  //const client = new Mqtt.Client('0.0.0.0:1883');

//const [connected, setConnected] = React.useState(false);

const [connected, setConnected] = useState(false);
const [username, setUsername] = useState('');
const [inputNumber, setInputNumber] = useState('');
const [isModalVisible, setModalVisible] = useState(false);
const [messages, setMessages] = useState([]);

const [videoFrame, setVideoFrame] = useState(null);
const [isVideoModalVisible, setVideoModalVisible] = useState(false);



client.on('connected', () => {
  console.log('PART 2');
  //client.subscribe('test/servo');
});

useEffect(() => {

  client.connect()
    .then(() => {
      console.log('Connected to MQTT broker');
      // Subscribe to the desired MQTT topic
      setConnected(true)
      client.subscribe('test/servo')
      .then(() => {
        console.log('Subscribed to the topic');
      })
      .catch((error) => {
        console.log('Error subscribing to the topic:', error);
      });
      client.subscribe("test/app")
      client.subscribe("test/popup")
      client.subscribe("test/video")

      client.on('messageReceived', (message) => {
        const topic = message.destinationName; // Get the topic of the received message
        if (topic === "test/video") {
          handleVideoFrame(message)
        }
        if (topic === 'test/app') {
          console.log('Message:', message.payloadString);
          setMessages((prevMessages) => [message.payloadString, ...prevMessages]);
          if (message.payloadString == "Please Enter User Information") {
            toggleModal()
          }
          if (message.payloadString == "Facial Recognition is finished!") {
            setVideoModalVisible(false)
          }
        }
      });

    })
    .catch((error) => {
      setConnected(false)
      console.log('Connection failed:', error);
    });
  }, []);

  /*client2.connect()
    .then(() => {
      console.log('Connected to MQTT broker COMPUTER');
      // Subscribe to the desired MQTT topic
      //setConnected(true)
      client2.subscribe('test/servo')
      .then(() => {
        console.log('Subscribed to the topic COMPUTER');
      })
      .catch((error) => {
        console.log('Error subscribing to the topic COMPUTER:', error);
      });
    })
    .catch((error) => {
      //setConnected(false)
      console.log('Connection failed COMPUTER:', error);
    }); */

  /*const onMessageArrived = (message) => {
    //msg = message.payloadString;
    //console.log(msg);
    console.log("HI")
    console.log('Received Message:', message);
    const payloadBytes = message.payloadBytes;
    const payloadString = String.fromCharCode.apply(null, new Uint8Array(payloadBytes));
    console.log(payloadString);
    //setMessages((prevMessages) => [msg, ...prevMessages]);
    // You can process the message further and display it in your app's UI, if required.
  };*/

  //onMessageArrived("YOOO");

  //client.onMessageArrived = onMessageArrived
  
/*const storage = {
  setItem: () => {},
  getItem: () => {},
  removeItem: () => {},
};

const client = new Client({
  uri: 'ws://192.168.1.220:1884/mqtt',
  clientId: 'hi3333',
  storage: storage,
});

//React.useEffect(() => {

  client.connect()
    .then(() => {
      console.log('Connected to MQTT broker');
      // Subscribe to the desired MQTT topic
      //setConnected(true)
      client.subscribe('test/servo');
    })
    .catch((error) => {
      //setConnected(false)
      console.log('Connection failed:', error);
    });
    
//}, []); */

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

/*const handleButtonPress = () => {
  const message = 'Button pressed!';
  // Update the messages state with the new message
  setMessages((prevMessages) => [...prevMessages, message]);
};*/

  
const lock_button = () => {
  const message = new Message('This is lock');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
  const message1 = 'Lock Button Pressed!';
  setMessages((prevMessages) => [message1, ...prevMessages]);
};

const unlock_button = () => {
  const message = new Message('This is unlock');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
  const message1 = 'Unlock Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const FR_button = () => {
  const message = new Message('This is Facial Recognition');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
  const message1 = 'Facial Recognition Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
  setVideoModalVisible(true);
};

const newface_button = () => {
  const message = new Message('This is New Face');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
  const message1 = 'New Face Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const connect_button = () => {
  const message = new Message('This is connected');  // Replace 'your message' with the desired message payload
  message.destinationName = 'test/servo';  // Replace 'your/topic' with the desired topic
  client.send(message);
  const message1 = 'Connect Button Pressed!';
  setMessages((prevMessages) => [ message1, ...prevMessages]);
};

const toggleModal = () => {
  setModalVisible(!isModalVisible);
};

const handleSubmit = () => {
  // Validate the input fields if needed
  // Send the username and ID to the Raspberry Pi using MQTT
  const payload = JSON.stringify({ username, inputNumber });
  const message = new Message(payload);
  message.destinationName = 'test/popup'; // Replace 'test/app' with the desired topic to receive the username and ID on Raspberry Pi
  client.send(message);

  const message2 = new Message("Start Data Collection");
  message2._destinationName = 'test/servo';
  client.send(message2)

  toggleModal();
  setUsername('');
  setInputNumber('');

  // Optional: Update your messages state with a confirmation message
  const confirmationMessage = `Username: ${username}, ID: ${inputNumber} submitted`;
  setMessages((prevMessages) => [confirmationMessage, ...prevMessages]);
};

const handleVideoFrame = (message) => {
  setVideoFrame(message.payloadString);
};

/*const handleNumberSubmit = () => {
  // Process the inputNumber (e.g., send it via MQTT)
  console.log('Submitted number:', inputNumber);

  // Close the modal after submission
  toggleModal();
};*/

/*client.on('message', (topic, message) => {
 // if (topic === 'test/servo') {
    const msg = message.toString();
    console.log(msg)
    setMessages((prevMessages) => [ msg, ...prevMessages])
    // You can process the message further and display it in your app's UI, if required.
  //}
});*/


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


      <Modal visible={isModalVisible} animationType="slide">
        <View style={styles.modalContainer}>
          <Text style={styles.modalTitle}>Enter Info</Text>
          
          <TextInput
            style={styles.input}
            placeholder="Enter username"
            onChangeText={(text) => setUsername(text)}
            value={username}
          />
         
          <TextInput
            style={styles.input}
            placeholder="Enter a number"
            onChangeText={(text) => setInputNumber(text)}
            value={inputNumber}
            keyboardType="numeric"
          />
         
          <RectangularButton title="Submit" onPress={handleSubmit} />
        </View>
      </Modal>

      <Modal visible={isVideoModalVisible} animationType="slide">
        <View style={styles.videoModalContainer}>
          {/* Display the received video frame as an Image */}
          {videoFrame && <Image source={{ uri: `data:image/jpeg;base64,${videoFrame}` }} style={styles.videoFrame} />}
        </View>
      </Modal>

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

  modalContainer: {
    flex: 1,
    backgroundColor: '#131414',
    alignItems: 'center',
    justifyContent: 'center',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2b87ed',
    marginBottom: 20,
  },
  input: {
    backgroundColor: '#f0f0f0',
    width: 300,
    height: 40,
    paddingHorizontal: 10,
    marginBottom: 20,
    borderRadius: 8,
  },
  videoModalContainer: {
    flex: 1,
    backgroundColor: 'black',
    alignItems: 'center',
    justifyContent: 'center',
  },
  videoFrame: {
    width: 320,
    height: 240,
  }, 
  
});
