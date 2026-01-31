import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen';
import QuantumScreen from './screens/QuantumScreen';
import NeuralScreen from './screens/NeuralScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#0A0E27' },
          headerTintColor: '#00D9FF',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: '🌟 Synova AI' }} />
        <Stack.Screen
          name="Quantum"
          component={QuantumScreen}
          options={{ title: '⚛️ Quantum Processing' }}
        />
        <Stack.Screen
          name="Neural"
          component={NeuralScreen}
          options={{ title: '🧠 Mind Interface' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
