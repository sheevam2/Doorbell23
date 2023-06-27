import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import Mqtt from 'react-native-mqtt';

//__________MQTT__________________________

const client = new Mqtt.Client('mqtt://192.168.1.220:1883');
client.connect({
  username: 'doorbell_mqtt',
  password: 'Doorbell123!',
  clientId: '2023',
});

client.on('connect', () => {
  console.log('Connected to MQTT broker');
});



//______________APP UI__________________

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
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
