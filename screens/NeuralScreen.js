import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const colors = {
  background: '#0A0E27',
  primary: '#00D9FF',
  white: '#FFFFFF',
  button: '#1A1F4B',
};

export default function NeuralScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🧠 Mind Interface</Text>
      <Text style={styles.description}>
        Connect with the neural network and explore the boundaries of artificial intelligence.
      </Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Neural Features</Text>
        <Text style={styles.cardText}>• Deep Learning</Text>
        <Text style={styles.cardText}>• Neural Networks</Text>
        <Text style={styles.cardText}>• Cognitive Computing</Text>
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
