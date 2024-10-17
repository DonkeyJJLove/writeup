import unittest
from neural_architecture.neuron import Neuron
from neural_architecture.synapse import Synapse
from modules.neuron_visualizer import NeuronVisualizer
import contextlib
import plotly.io as pio


class TestProjectNeuralNetworkRepresentation(unittest.TestCase):

    def setUp(self):
        """
        Setup logic before each test, initializing common components.
        """
        # Tworzenie neuronów reprezentujących moduły projektu
        self.neuron_main = Neuron("main.py", pos=(0, 0, 0))
        self.neuron_gui = Neuron("gui.py", pos=(1, 1, 1))
        self.neuron_dependency_parser = Neuron("dependency_parser.py", pos=(2, 2, 2))
        self.neuron_neuron_visualizer = Neuron("neuron_visualizer.py", pos=(3, 3, 3))
        self.neuron_synapse = Neuron("synapse.py", pos=(4, 4, 4))
        self.neuron_neuron = Neuron("neuron.py", pos=(5, 5, 5))

        # Tworzenie dynamicznych synaps z różnymi wagami opartymi na bardziej skomplikowanych relacjach
        self.synapse_main_to_gui = Synapse(source=self.neuron_main, target=self.neuron_gui, type='import', weight=1.0)
        self.synapse_gui_to_dependency_parser = Synapse(source=self.neuron_gui, target=self.neuron_dependency_parser,
                                                        type='dependency', weight=self.calculate_weight('dependency'))
        self.synapse_gui_to_neuron_visualizer = Synapse(source=self.neuron_gui, target=self.neuron_neuron_visualizer,
                                                        type='dependency', weight=self.calculate_weight('visualization'))
        self.synapse_dependency_parser_to_synapse = Synapse(source=self.neuron_dependency_parser, target=self.neuron_synapse,
                                                            type='relation', weight=self.calculate_weight('relation'))
        self.synapse_neuron_to_synapse = Synapse(source=self.neuron_neuron, target=self.neuron_synapse,
                                                 type='relation', weight=self.calculate_weight('processing-relation'))
        self.synapse_neuron_visualizer_to_neuron = Synapse(source=self.neuron_neuron_visualizer, target=self.neuron_neuron,
                                                           type='visualization', weight=self.calculate_weight('visualization'))

        # Connect neurons
        self.connect_neurons()

    def calculate_weight(self, relation_type):
        """
        Dynamically calculates the weight of a synapse based on the relationship type.
        """
        weights = {
            'import': 1.0,
            'dependency': 1.5,
            'visualization': 1.8,
            'relation': 1.2,
            'processing-relation': 1.4
        }
        return weights.get(relation_type, 1.0)

    def connect_neurons(self):
        """
        Establishes the connections (synapses) between the neurons.
        """
        self.neuron_main.connect(self.neuron_gui, self.synapse_main_to_gui)
        self.neuron_gui.connect(self.neuron_dependency_parser, self.synapse_gui_to_dependency_parser)
        self.neuron_gui.connect(self.neuron_neuron_visualizer, self.synapse_gui_to_neuron_visualizer)
        self.neuron_dependency_parser.connect(self.neuron_synapse, self.synapse_dependency_parser_to_synapse)
        self.neuron_neuron.connect(self.neuron_synapse, self.synapse_neuron_to_synapse)
        self.neuron_neuron_visualizer.connect(self.neuron_neuron, self.synapse_neuron_visualizer_to_neuron)

    def test_project_structure_representation(self):
        """
        Test creates a logical representation of the project structure as a generative neural network process.
        """
        # Lista neuronów (elementów projektu)
        neurons = [self.neuron_main, self.neuron_gui, self.neuron_dependency_parser, self.neuron_neuron_visualizer, self.neuron_synapse, self.neuron_neuron]

        # Inicjalizacja wizualizatora z dynamiczną możliwością dodania nowych neuronów i synaps
        visualizer = NeuronVisualizer(neurons)

        # Użycie contextlib do obsługi zasobów, które mogą być otwarte przez plotly
        with contextlib.closing(pio.renderers.default) as renderer:
            # Wizualizacja procesu (zakomentowane w przypadku testów automatycznych)
            visualizer.visualize_plotly()

        # Test sprawdza, czy struktura sieci jest poprawnie zbudowana
        self.assertEqual(len(visualizer.G.nodes()), 6, "Incorrect number of nodes in the network.")
        self.assertEqual(len(visualizer.G.edges()), 6, "Incorrect number of edges in the network.")

    def tearDown(self):
        """
        Clean-up after each test if needed.
        """
        # Optional: implement any cleanup logic if necessary
        pass


if __name__ == '__main__':
    unittest.main()
