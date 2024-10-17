# File: neural_architecture/synapse.py
# Author: cha0s
# Date: 2024-10-16

class Synapse:
    def __init__(self, source=None, target=None, type='association', weight=1.0):
        self.source = source
        self.target = target
        self.type = type
        self.weight = weight

    def __repr__(self):
        return f"Synapse({self.source.name} -> {self.target.name}, Type: {self.type}, Weight: {self.weight})"
