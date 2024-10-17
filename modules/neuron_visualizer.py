# File: modules/neuron_visualizer.py
# Author: cha0s
# Date: 2024-10-16

"""
============================================================
File: neuron_visualizer.py
Author: cha0s
Date: 2024-10-16
Description:
    Klasa odpowiedzialna za wizualizację sieci neuronowej w 3D.

    Funkcjonalności:
        - Generowanie wizualizacji 3D sieci neuronowej z użyciem Plotly.
        - Kolorowanie połączeń na podstawie ich typu i siły.
        - Wyświetlanie etykiet neuronów i połączeń.
        - Automatyczne rozmieszczenie neuronów w przestrzeni 3D.

Future Enhancements:
    - Integracja z innymi bibliotekami wizualizacyjnymi.
    - Dodanie interaktywnych filtrów do ukrywania lub pokazywania określonych typów połączeń.
============================================================
"""

import logging
import plotly.graph_objects as go
import networkx as nx
from neural_architecture.neuron import Neuron
from neural_architecture.synapse import Synapse


class NeuronVisualizer:
    def __init__(self, neurons):
        """
        Inicjalizuje wizualizator neuronów.

        :param neurons: Lista obiektów Neuron
        """
        self.neurons = neurons
        logging.info(f"NeuronVisualizer initialized with {len(self.neurons)} neurons.")
        self.G = self.build_graph()

    def build_graph(self):
        """
        Buduje graf z listy neuronów i ich synaps.

        :return: Obiekt grafu NetworkX
        """
        G = nx.DiGraph()
        for neuron in self.neurons:
            G.add_node(neuron.name, pos=neuron.pos)
            for synapse in neuron.synapses:
                G.add_edge(neuron.name, synapse.target.name,
                           type=synapse.type, weight=synapse.weight)
        logging.info("Graf sieci neuronowej zbudowany.")
        return G

    def visualize(self, backend='plotly', parent=None):
        """
        Generuje wizualizację sieci neuronowej.

        :param backend: Backend do wizualizacji ('plotly' domyślnie)
        :param parent: Obiekt rodzica (dla integracji z GUI, jeśli potrzebne)
        """
        if backend == 'plotly':
            self.visualize_plotly()
        else:
            logging.warning(f"Nieobsługiwany backend: {backend}")

    def visualize_plotly(self):
        """
        Wizualizacja sieci neuronowej za pomocą Plotly w 3D.
        """
        try:
            # Użycie układu grafu do rozmieszczenia neuronów
            pos = nx.spring_layout(self.G, dim=3, seed=42)  # 'dim=3' dla 3D

            # Dodanie pozycji do węzłów
            for node in self.G.nodes():
                self.G.nodes[node]['pos'] = pos[node]

            # Grupowanie połączeń według typu
            edge_types = {}
            for edge in self.G.edges(data=True):
                edge_type = edge[2]['type']
                if edge_type not in edge_types:
                    edge_types[edge_type] = {'x': [], 'y': [], 'z': [], 'width': []}
                x0, y0, z0 = self.G.nodes[edge[0]]['pos']
                x1, y1, z1 = self.G.nodes[edge[1]]['pos']
                edge_types[edge_type]['x'] += [x0, x1, None]
                edge_types[edge_type]['y'] += [y0, y1, None]
                edge_types[edge_type]['z'] += [z0, z1, None]
                edge_types[edge_type]['width'].append(max(1, edge[2]['weight']))

            # Definicja kolorów dla typów synaps
            type_colors = {
                'association': 'blue',
                'object': 'green',
                'conjunction': 'red',
                'other': 'gray'
            }

            # Tworzenie śladów dla połączeń
            edge_traces = []
            for edge_type, data in edge_types.items():
                color = type_colors.get(edge_type, 'gray')
                # Średnia grubość dla danego typu
                avg_width = sum(data['width']) / len(data['width']) if data['width'] else 2
                edge_traces.append(go.Scatter3d(
                    x=data['x'],
                    y=data['y'],
                    z=data['z'],
                    mode='lines',
                    line=dict(color=color, width=avg_width),
                    hoverinfo='none',
                    name=edge_type
                ))

            # Przygotowanie pozycji dla węzłów
            node_x = []
            node_y = []
            node_z = []
            node_text = []

            for node in self.G.nodes(data=True):
                node_x.append(node[1]['pos'][0])
                node_y.append(node[1]['pos'][1])
                node_z.append(node[1]['pos'][2])
                node_text.append(node[0])

            # Ślad dla węzłów
            node_trace = go.Scatter3d(
                x=node_x,
                y=node_y,
                z=node_z,
                mode='markers+text',
                text=node_text,
                textposition='top center',
                hoverinfo='text',
                marker=dict(
                    color='orange',  # Kolor węzłów
                    size=10,  # Rozmiar węzłów
                    line=dict(width=2, color='DarkSlateGrey')
                )
            )

            # Utworzenie wykresu
            fig = go.Figure(data=edge_traces + [node_trace],
                            layout=go.Layout(
                                title='Neuron Network Visualization',
                                titlefont_size=16,
                                showlegend=True,
                                hovermode='closest',
                                margin=dict(b=20, l=5, r=5, t=40),
                                scene=dict(
                                    xaxis=dict(showbackground=False, showticklabels=False, zeroline=False),
                                    yaxis=dict(showbackground=False, showticklabels=False, zeroline=False),
                                    zaxis=dict(showbackground=False, showticklabels=False, zeroline=False)
                                ),
                                annotations=[
                                    dict(
                                        showarrow=False,
                                        text="",
                                        xref="paper", yref="paper"
                                    )
                                ],
                                height=800,
                                width=1000
                            ))

            # Dodanie legendy dla typów synapsy
            for edge_type, color in type_colors.items():
                fig.add_trace(go.Scatter3d(
                    x=[None],
                    y=[None],
                    z=[None],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=color,
                        line=dict(width=0),
                        symbol='circle'
                    ),
                    showlegend=True,
                    name=edge_type
                ))

            fig.show()
            logging.info("Wizualizacja Plotly wygenerowana pomyślnie.")
        except Exception as e:
            logging.error(f"Error during visualization: {e}")
