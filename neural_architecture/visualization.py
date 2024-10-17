# File: neural_architecture/visualization.py
# Author: cha0s
# Date: 2024-04-26

"""
============================================================
File: visualization.py
Author: cha0s
Date: 2024-04-26
Description:
    Implementacja klasy Visualization, która generuje wizualizacje sieci neuronowej.

    Funkcjonalności:
        - Generowanie wizualizacji 2D/3D.
        - Tworzenie artefaktów synaptycznych.

Future Enhancements:
    - Dodanie interaktywnych elementów do wizualizacji.
    - Integracja z bibliotekami graficznymi (np. PyOpenGL, matplotlib).
============================================================
"""

import logging
import matplotlib.pyplot as plt
import networkx as nx


class Visualization:
    def __init__(self, neural_network):
        """
        Inicjalizuje wizualizację.

        :param neural_network: Obiekt NeuralNetwork
        """
        self.neural_network = neural_network
        logging.info("Visualization initialized.")

    def visualize(self):
        """
        Generuje wizualizację sieci neuronowej.
        """
        G = nx.DiGraph()

        # Dodawanie neuronów jako węzłów
        for neuron in self.neural_network.get_neurons().values():
            G.add_node(neuron.name, pos=neuron.pos)

        # Dodawanie synaps jako krawędzi
        for synapse in self.neural_network.get_synapses():
            G.add_edge(synapse.source.name, synapse.target.name, type=synapse.type)

        # Generowanie pozycji węzłów
        pos = nx.spring_layout(G)

        # Rysowanie węzłów
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

        # Rysowanie etykiet węzłów
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Rysowanie krawędzi
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='->', arrowsize=20)

        # Rysowanie etykiet krawędzi
        edge_labels = nx.get_edge_attributes(G, 'type')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        plt.title("Synaptic Network Visualization")
        plt.axis('off')
        plt.show()
