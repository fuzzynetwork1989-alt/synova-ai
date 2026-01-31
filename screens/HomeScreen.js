import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const colors = {
  background: '#0A0E27',
  primary: '#00D9FF',
  white: '#FFFFFF',
  button: '#1A1F4B',
};

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to Synova AI</Text>
      <Text style={styles.subtitle}>Explore the future of quantum computing</Text>

      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Quantum')}>
        <Text style={styles.buttonText}>⚛️ Quantum Processing</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Neural')}>
        <Text style={styles.buttonText}>🧠 Mind Interface</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: 'center',
    backgroundColor: colors.button,
    borderRadius: 10,
    marginVertical: 10,
    padding: 15,
    width: '80%',
  },
  buttonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: '600',
  },
  container: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  subtitle: {
    color: colors.white,
    fontSize: 16,
    marginBottom: 40,
    textAlign: 'center',
  },
  title: {
    color: colors.primary,
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
});
