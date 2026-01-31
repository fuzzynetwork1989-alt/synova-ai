import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const colors = {
  background: '#0A0E27',
  primary: '#00D9FF',
  white: '#FFFFFF',
  button: '#1A1F4B',
};

export default function QuantumScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>⚛️ Quantum Processing</Text>
      <Text style={styles.description}>
        Experience the power of quantum computing with our advanced processing capabilities.
      </Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Quantum Features</Text>
        <Text style={styles.cardText}>• Superposition</Text>
        <Text style={styles.cardText}>• Entanglement</Text>
        <Text style={styles.cardText}>• Quantum Tunneling</Text>
      </View>

      <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
        <Text style={styles.buttonText}>Back to Home</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  backButton: {
    alignItems: 'center',
    backgroundColor: colors.button,
    borderRadius: 10,
    bottom: 30,
    left: 20,
    padding: 15,
    position: 'absolute',
    right: 20,
    width: '100%',
  },
  buttonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: '600',
  },
  card: {
    backgroundColor: colors.button,
    borderRadius: 10,
    marginBottom: 20,
    padding: 20,
  },
  cardText: {
    color: colors.white,
    fontSize: 16,
    marginBottom: 10,
    marginLeft: 10,
  },
  cardTitle: {
    color: colors.primary,
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  container: {
    backgroundColor: colors.background,
    flex: 1,
    padding: 20,
    paddingTop: 60,
  },
  description: {
    color: colors.white,
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 30,
    textAlign: 'center',
  },
  title: {
    color: colors.primary,
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
});
