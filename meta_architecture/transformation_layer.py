# File: meta_architecture/transformation_layer.py
# Author: cha0s
# Date: 2024-04-26

import logging
from neural_architecture.synapse import Synapse
from neural_architecture.neuron import Neuron


class TransformationLayer:
    def __init__(self, synapse_language):
        self.synapse_language = synapse_language
        self.neurons = {}  # Klucz: nazwa słowa, Wartość: obiekt Neuron
        self.synapses = []  # Lista obiektów Synapse
        logging.info("TransformationLayer initialized.")

    def transform(self, analysis):
        """
        Przekształca analizę promptu na neurony i synapsy.

        :param analysis: Słownik z jednostkami i relacjami
        :return: Tuple (neurons, synapses)
        """
        logging.info("Przekształcanie analizy promptu na neurony i synapsy...")

        # Tworzenie neuronów
        for unit in analysis['units']:
            word = unit['word']
            pos = unit['pos']
            if word not in self.neurons:
                self.neurons[word] = Neuron(name=word, pos=pos)
                logging.info(f"Neuron utworzony: {word} ({pos})")

        # Tworzenie synaps na podstawie relacji
        for relation in analysis['relations']:
            child_word = relation['word']
            parent_word = relation['head']
            syn_type = relation['dependency']

            if child_word in self.neurons and parent_word in self.neurons:
                synapse = Synapse(
                    source=self.neurons[parent_word],
                    target=self.neurons[child_word],
                    type=syn_type
                )
                self.synapses.append(synapse)
                logging.info(f"Synapsa utworzona: {parent_word} -> {child_word} ({syn_type})")
            else:
                logging.warning(f"Brak neuronu dla słowa: {child_word} lub {parent_word}")

        logging.info(f"Przekształcona analiza: {len(self.neurons)} neuronów, {len(self.synapses)} synaps")
        return self.neurons, self.synapses
