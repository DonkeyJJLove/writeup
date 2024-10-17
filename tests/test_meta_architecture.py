import unittest
from neural_architecture.neuron import Neuron
from neural_architecture.synapse import Synapse
from modules.neuron_visualizer import NeuronVisualizer
import contextlib
import plotly.io as pio


class MetaArchitectureTest(unittest.TestCase):

    def setUp(self):
        """
        Inicjalizacja neuronów, synaps i meta-logiki przed każdym testem.
        """
        # Tworzenie neuronów dla poszczególnych plików projektu
        self.neuron_main = Neuron("main.py", pos=(0, 0, 0))
        self.neuron_gui = Neuron("gui.py", pos=(1, 1, 1))
        self.neuron_dependency_parser = Neuron("dependency_parser.py", pos=(2, 2, 2))
        self.neuron_neuron_visualizer = Neuron("neuron_visualizer.py", pos=(3, 3, 3))
        self.neuron_synapse = Neuron("synapse.py", pos=(4, 4, 4))
        self.neuron_neuron = Neuron("neuron.py", pos=(5, 5, 5))

        # Meta-elementy reprezentujące procesy w systemie
        self.neuron_logic_handler = Neuron("logic_handler.py", pos=(6, 6, 6))
        self.neuron_event_manager = Neuron("event_manager.py", pos=(7, 7, 7))
        self.neuron_state_manager = Neuron("state_manager.py", pos=(8, 8, 8))

        # Synapsy dynamicznie obliczane dla meta-zależności
        self.synapse_logic_main = Synapse(source=self.neuron_logic_handler, target=self.neuron_main, type='meta-process', weight=self.calculate_meta_weight('meta-process'))
        self.synapse_event_gui = Synapse(source=self.neuron_event_manager, target=self.neuron_gui, type='event-dependency', weight=self.calculate_meta_weight('event-dependency'))
        self.synapse_state_synapse = Synapse(source=self.neuron_state_manager, target=self.neuron_synapse, type='state-management', weight=self.calculate_meta_weight('state-management'))

        # Tworzenie regularnych synaps między głównymi neuronami projektu
        self.synapse_main_to_gui = Synapse(source=self.neuron_main, target=self.neuron_gui, type='import', weight=1.0)
        self.synapse_gui_to_dependency_parser = Synapse(source=self.neuron_gui, target=self.neuron_dependency_parser, type='dependency', weight=1.5)
        self.synapse_gui_to_neuron_visualizer = Synapse(source=self.neuron_gui, target=self.neuron_neuron_visualizer, type='dependency', weight=1.8)
        self.synapse_dependency_parser_to_synapse = Synapse(source=self.neuron_dependency_parser, target=self.neuron_synapse, type='relation', weight=1.2)
        self.synapse_neuron_to_synapse = Synapse(source=self.neuron_neuron, target=self.neuron_synapse, type='relation', weight=1.4)
        self.synapse_neuron_visualizer_to_neuron = Synapse(source=self.neuron_neuron_visualizer, target=self.neuron_neuron, type='visualization', weight=1.8)

        # Łączenie neuronów
        self.connect_neurons()

    def calculate_meta_weight(self, relation_type):
        """
        Oblicza wagę synapsy meta-procesu na podstawie typu relacji.
        """
        weights = {
            'meta-process': 2.0,
            'event-dependency': 1.7,
            'state-management': 1.9
        }
        return weights.get(relation_type, 1.0)

    def connect_neurons(self):
        """
        Tworzy połączenia (synapsy) między neuronami, zarówno regularne jak i meta.
        """
        # Połączenia między głównymi neuronami projektu
        self.neuron_main.connect(self.neuron_gui, self.synapse_main_to_gui)
        self.neuron_gui.connect(self.neuron_dependency_parser, self.synapse_gui_to_dependency_parser)
        self.neuron_gui.connect(self.neuron_neuron_visualizer, self.synapse_gui_to_neuron_visualizer)
        self.neuron_dependency_parser.connect(self.neuron_synapse, self.synapse_dependency_parser_to_synapse)
        self.neuron_neuron.connect(self.neuron_synapse, self.synapse_neuron_to_synapse)
        self.neuron_neuron_visualizer.connect(self.neuron_neuron, self.synapse_neuron_visualizer_to_neuron)

        # Meta-połączenia dla zarządzania logiką, zdarzeniami i stanem
        self.neuron_logic_handler.connect(self.neuron_main, self.synapse_logic_main)
        self.neuron_event_manager.connect(self.neuron_gui, self.synapse_event_gui)
        self.neuron_state_manager.connect(self.neuron_synapse, self.synapse_state_synapse)

    def test_meta_architecture(self):
        """
        Test tworzy meta-architekturę sieci neuronowej, przedstawiając zależności na poziomie logiki procesów.
        """
        neurons = [self.neuron_main, self.neuron_gui, self.neuron_dependency_parser, self.neuron_neuron_visualizer, self.neuron_synapse, self.neuron_neuron,
                   self.neuron_logic_handler, self.neuron_event_manager, self.neuron_state_manager]

        # Inicjalizacja wizualizatora z dynamicznymi neuronami meta
        visualizer = NeuronVisualizer(neurons)

        # Użycie contextlib do obsługi zasobów, które mogą być otwarte przez plotly
        with contextlib.closing(pio.renderers.default) as renderer:
            # Wizualizacja procesu (zakomentowane dla testów automatycznych)
            visualizer.visualize_plotly()

        # Testowanie poprawności struktury sieci neuronowej z uwzględnieniem neuronów meta
        self.assertEqual(len(visualizer.G.nodes()), 9, "Incorrect number of nodes in the network (should include meta-nodes).")
        self.assertEqual(len(visualizer.G.edges()), 9, "Incorrect number of edges in the network (should include meta-edges).")

    def tearDown(self):
        """
        Czyszczenie po każdym teście.
        """
        pass


if __name__ == '__main__':
    unittest.main()
