# File: neural_architecture/neural_network.py
# Author: cha0s
# Date: 2024-04-26

"""
============================================================
File: neural_network.py
Author: cha0s
Date: 2024-04-26
Description:
    Implementacja klasy NeuralNetwork, która modeluje warstwy sieci neuronowej.

    Funkcjonalności:
        - Dodawanie neuronów i synaps.
        - Przechowywanie struktury sieci.

Future Enhancements:
    - Dodanie funkcji propagacji aktywacji.
    - Integracja z mechanizmami uczenia sieci.
============================================================
"""

import logging


class NeuralNetwork:
    def __init__(self):
        self.neurons = {}
        self.synapses = []
        logging.info("NeuralNetwork initialized.")

    def add_neuron(self, neuron):
        if neuron.name not in self.neurons:
            self.neurons[neuron.name] = neuron
            logging.info(f"Neuron dodany do sieci: {neuron.name}")
        else:
            logging.warning(f"Neuron {neuron.name} już istnieje w sieci.")

    def add_synapse(self, synapse):
        self.synapses.append(synapse)
        logging.info(f"Synapsa dodana do sieci: {synapse}")

    def get_neurons(self):
        return self.neurons

    def get_synapses(self):
        return self.synapses
