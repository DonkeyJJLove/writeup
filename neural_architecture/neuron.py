# File: neural_architecture/neuron.py
# Author: cha0s
# Date: 2024-10-16

class Neuron:
    def __init__(self, name, pos=(0, 0, 0)):
        self.name = name
        self.pos = pos
        self.functionality = functionality  # Adding functionality attribute
        self.synapses = []  # Lista obiektów Synapse

    def connect(self, target_neuron, synapse):
        self.synapses.append(synapse)
        synapse.source = self
        synapse.target = target_neuron

    def __repr__(self):
        return f"Neuron({self.name}, POS: {self.pos})"
