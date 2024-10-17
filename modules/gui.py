# File: modules/gui.py
# Author: cha0s
# Date: 2024-10-16

"""
============================================================
File: gui.py
Author: cha0s
Date: 2024-10-16
Description:
    Implementacja graficznego interfejsu użytkownika (GUI) aplikacji za pomocą PyQt5.
    Klasa SynapticApp tworzy główne okno aplikacji, zarządza interakcjami użytkownika
    oraz integruje wszystkie inne moduły, takie jak parser zależności, wizualizator neuronów
    i procesy generatywne.

    Funkcjonalności:
        - Wprowadzanie i ocena promptów przez użytkownika.
        - Generowanie analizy zależności na podstawie promptów.
        - Wizualizacja analizy zależności w formie 3D.
        - Zarządzanie procesami generatywnymi i ich wizualizacja.
        - Wyciąganie wniosków z analiz i procesów generatywnych.
        - Testowanie funkcji wizualizacyjnych.

Future Enhancements:
    - Rozbudowa interfejsu użytkownika o dodatkowe funkcjonalności (np. zapisywanie wyników).
    - Dodanie opcji personalizacji wyglądu wizualizacji.
    - Integracja z systemami zewnętrznymi do przechowywania i analizy danych.
    - Implementacja wielowątkowości w celu poprawy wydajności aplikacji.
============================================================
"""

import logging
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel,
    QComboBox, QMessageBox, QSplitter, QDialog, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

# Importowanie klas z innych modułów
from meta_architecture.dependency_parser import DependencyParser
from meta_architecture.synapse_language import SynapseLanguage
from meta_architecture.transformation_layer import TransformationLayer
from neural_architecture import Neuron, Synapse
from neural_architecture.neural_network import NeuralNetwork
from neural_architecture.visualization import Visualization

# Importowanie dummy modułów
from modules.language_definition import LanguageDefinition
from modules.generative_processes import GenerativeProcess
from modules.prompt_evaluator import PromptEvaluator
from modules.neuron_visualizer import NeuronVisualizer


class SynapticApp(QWidget):
    def __init__(self):
        super().__init__()
        # Konfiguracja logowania
        logging.basicConfig(
            filename='logs/app.log',
            filemode='a',
            format='%(asctime)s %(levelname)s:%(message)s',
            level=logging.INFO
        )
        logging.info("Inicjalizacja GUI...")

        # Inicjalizacja komponentów NLP i sieci neuronowej
        try:
            self.dependency_parser = DependencyParser(system='UD')
            self.synapse_language = SynapseLanguage()
            self.transformation_layer = TransformationLayer(synapse_language=self.synapse_language)
            self.neural_network = NeuralNetwork()
            self.visualization = Visualization(self.neural_network)
            self.language_def = LanguageDefinition('Polski')
            self.prompt_evaluator = PromptEvaluator()
            self.generative_process = None  # Inicjalizacja procesu generatywnego
            logging.info("Komponenty NLP i sieci neuronowej zainicjalizowane pomyślnie.")
        except Exception as e:
            logging.error(f"Error initializing NLP components: {e}")
            QMessageBox.critical(self, 'Initialization Error', f"Failed to initialize NLP components: {e}")
            sys.exit(1)

        # Budowa interfejsu użytkownika
        self.initUI()
        logging.info("GUI zainicjalizowane pomyślnie.")

    def initUI(self):
        self.setWindowTitle('Synaptic Visualization App')
        self.setGeometry(100, 100, 1400, 800)  # Zwiększenie szerokości dla dwóch paneli

        main_layout = QHBoxLayout()

        # Użycie QSplitter dla elastycznego podziału
        splitter = QSplitter(Qt.Horizontal)

        # Panel dla Promptów
        prompt_panel = QWidget()
        prompt_layout = QVBoxLayout()

        # Sekcja: Wprowadzenie Promptu
        self.prompt_label = QLabel('Wprowadź prompt:')
        prompt_layout.addWidget(self.prompt_label)

        self.prompt_text = QTextEdit(self)
        prompt_layout.addWidget(self.prompt_text)

        self.evaluate_button = QPushButton('Oceń Prompt', self)
        self.evaluate_button.clicked.connect(self.evaluate_prompt)
        prompt_layout.addWidget(self.evaluate_button)

        self.evaluation_result = QLabel('')
        prompt_layout.addWidget(self.evaluation_result)

        # Sekcja: Parsowanie Zależności
        self.parser_label = QLabel('Wybierz system zależności:')
        prompt_layout.addWidget(self.parser_label)

        self.parser_combo = QComboBox(self)
        self.parser_combo.addItems(['UD', 'Stanford'])
        prompt_layout.addWidget(self.parser_combo)

        self.generate_artifact_button = QPushButton('Generuj Analizę', self)
        self.generate_artifact_button.clicked.connect(self.generate_artifact)
        prompt_layout.addWidget(self.generate_artifact_button)

        self.artifact_label = QLabel('Wygenerowana Analiza:')
        prompt_layout.addWidget(self.artifact_label)

        self.artifact_text = QTextEdit(self)
        self.artifact_text.setReadOnly(True)
        prompt_layout.addWidget(self.artifact_text)

        # Sekcja: Generowanie 3D Artefaktu dla Promptu
        self.visualize_dependency_3d_button = QPushButton('Generuj 3D Artefakt Analizy', self)
        self.visualize_dependency_3d_button.clicked.connect(self.generate_dependency_3d_artifact)
        prompt_layout.addWidget(self.visualize_dependency_3d_button)

        # Sekcja: Wyciąganie Wniosków dla Promptu
        self.extract_conclusions_prompt_button = QPushButton('Wyciągnij Wnioski z Analizy', self)
        self.extract_conclusions_prompt_button.clicked.connect(self.extract_conclusions_prompt)
        prompt_layout.addWidget(self.extract_conclusions_prompt_button)

        # Przycisk Testowy
        self.test_visualization_button = QPushButton('Test Wizualizacji 3D', self)
        self.test_visualization_button.clicked.connect(self.test_visualization)
        prompt_layout.addWidget(self.test_visualization_button)

        prompt_panel.setLayout(prompt_layout)
        splitter.addWidget(prompt_panel)

        # Panel dla Procesów Generatywnych
        process_panel = QWidget()
        process_layout = QVBoxLayout()

        # Sekcja: Definicja Języka
        self.lang_label = QLabel('Definiowanie Języka:')
        process_layout.addWidget(self.lang_label)

        self.define_alphabet_button = QPushButton('Zdefiniuj Alfabet', self)
        self.define_alphabet_button.clicked.connect(self.define_alphabet)
        process_layout.addWidget(self.define_alphabet_button)

        self.define_grammar_button = QPushButton('Dodaj Regułę Gramatyczną', self)
        self.define_grammar_button.clicked.connect(self.define_grammar)
        process_layout.addWidget(self.define_grammar_button)

        # Sekcja: Procesy Generatywne
        self.gen_proc_label = QLabel('Procesy Generatywne:')
        process_layout.addWidget(self.gen_proc_label)

        self.create_process_button = QPushButton('Utwórz Proces Generatywny', self)
        self.create_process_button.clicked.connect(self.create_generative_process)
        process_layout.addWidget(self.create_process_button)

        # Sekcja: Wizualizacja Drzewa Synaptycznego
        self.visualize_tree_button = QPushButton('Wizualizuj Drzewo Synaptyczne', self)
        self.visualize_tree_button.clicked.connect(self.visualize_synaptic_tree)
        process_layout.addWidget(self.visualize_tree_button)

        # Sekcja: Generowanie 3D Artefaktu dla Procesów Generatywnych
        self.visualize_process_3d_button = QPushButton('Generuj 3D Artefakt Drzewa Synaptycznego', self)
        self.visualize_process_3d_button.clicked.connect(self.generate_process_3d_artifact)
        process_layout.addWidget(self.visualize_process_3d_button)

        # Sekcja: Wyciąganie Wniosków dla Procesów Generatywnych
        self.extract_conclusions_process_button = QPushButton('Wyciągnij Wnioski z Procesu', self)
        self.extract_conclusions_process_button.clicked.connect(self.extract_conclusions_process)
        process_layout.addWidget(self.extract_conclusions_process_button)

        process_panel.setLayout(process_layout)
        splitter.addWidget(process_panel)

        # Ustawienie podziału
        splitter.setSizes([700, 700])  # Równe rozmiary obu paneli
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    # -------------------- Funkcje dla Promptów --------------------

    def evaluate_prompt(self):
        logging.info("Ocena promptu...")
        prompt = self.prompt_text.toPlainText()
        evaluation = self.prompt_evaluator.evaluate_prompt(prompt)
        self.evaluation_result.setText(f'Ocena Promptu: {evaluation}')
        logging.info(f'Ocena promptu: {evaluation}')

    def generate_artifact(self):
        logging.info("Generowanie analizy zależności...")
        prompt = self.prompt_text.toPlainText()
        system = self.parser_combo.currentText()
        try:
            relations = self.dependency_parser.parse(prompt)
            artifact = "\n".join([f"{rel['word']} ({rel['dependency']}) -> {rel['head']}" for rel in relations])
            self.artifact_text.setText(artifact)
            logging.info("Analiza zależności wygenerowana pomyślnie.")
        except Exception as e:
            logging.exception("Wystąpił błąd podczas generowania analizy zależności.")
            QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas generowania analizy zależności: {str(e)}')

    def generate_dependency_3d_artifact(self):
        logging.info("Generowanie 3D artefaktu analizy promptu...")
        try:
            artifact = self.artifact_text.toPlainText()
            relations = artifact.split('\n') if artifact else []
            logging.info(f"Zwrócone relacje do wizualizacji: {relations}")  # Dodane logowanie
            if not relations or all(not rel.strip() for rel in relations):
                QMessageBox.warning(self, 'Brak Analizy', 'Najpierw wygeneruj analizę zależności.')
                logging.warning("Próba generowania 3D artefaktu bez dostępnej analizy.")
                return

            # Utworzenie listy neuronów na podstawie relacji
            neurons = {}
            for relation in relations:
                relation = relation.strip()
                if not relation:
                    continue
                try:
                    child_part, parent = relation.split(' -> ')
                    child_word, dep = child_part.split(' (')
                    dep = dep.rstrip(')')
                    child_word = child_word.strip()
                    parent = parent.strip()

                    if child_word not in neurons:
                        neurons[child_word] = Neuron(child_word, pos=(0, 0, 0))  # Przykładowa pozycja
                    if parent not in neurons:
                        neurons[parent] = Neuron(parent, pos=(0, 0, 0))  # Przykładowa pozycja

                    # Określenie typu synapsy na podstawie zależności
                    synapse_type = dep.lower()
                    # Przykładowa logika przypisywania typu synapsy
                    if 'object' in synapse_type:
                        syn_type = 'object'
                    elif 'association' in synapse_type:
                        syn_type = 'association'
                    elif 'conjunction' in synapse_type:
                        syn_type = 'conjunction'
                    else:
                        syn_type = 'other'

                    # Przykładowa waga synapsy, można ją modyfikować na podstawie innych kryteriów
                    syn_weight = 1.0

                    synapse = Synapse(weight=syn_weight, type=syn_type)
                    neurons[parent].connect(neurons[child_word], synapse)
                except ValueError as ve:
                    logging.error(f"Nie można sparsować relacji: {relation} - {ve}")

            neurons_list = list(neurons.values())
            logging.info(f"Liczba neuronów do wizualizacji: {len(neurons_list)}")
            for neuron in neurons_list:
                logging.info(
                    f"Neuron: {neuron.name}, Połączenia: {[synapse.target.name for synapse in neuron.synapses]}")

            if not neurons_list:
                QMessageBox.warning(self, 'Brak Neuronów', 'Nie znaleziono neuronów do wizualizacji.')
                logging.warning("Brak neuronów do wizualizacji po parsowaniu relacji.")
                return

            # Inicjalizacja wizualizatora i wywołanie metody wizualizacji
            visualizer = NeuronVisualizer(neurons_list)
            visualizer.visualize(backend='plotly', parent=self)
            logging.info("3D artefakt analizy promptu wygenerowany pomyślnie.")
        except Exception as e:
            logging.exception("Wystąpił błąd podczas generowania 3D artefaktu analizy promptu.")
            QMessageBox.critical(self, 'Błąd',
                                 f'Wystąpił błąd podczas generowania 3D artefaktu analizy promptu: {str(e)}')

    def extract_conclusions_prompt(self):
        logging.info("Wyciąganie wniosków z analizy promptu...")
        try:
            artifact = self.artifact_text.toPlainText()
            relations = artifact.split('\n') if artifact else []
            if not relations or all(not rel.strip() for rel in relations):
                QMessageBox.warning(self, 'Brak Analizy', 'Najpierw wygeneruj analizę zależności.')
                logging.warning("Próba wyciągnięcia wniosków bez dostępnej analizy.")
                return
            # Prosty przykład wyciągania wniosków: liczenie rodzajów zależności
            dep_counts = {}
            for relation in relations:
                parts = relation.split(' (')
                if len(parts) >= 2:
                    dep = parts[1].rstrip(')').strip()
                    dep_counts[dep] = dep_counts.get(dep, 0) + 1
            conclusions = "Wnioski z analizy promptu:\n"
            for dep, count in dep_counts.items():
                conclusions += f"{dep}: {count}\n"
            QMessageBox.information(self, 'Wnioski', conclusions)
            logging.info("Wnioski z analizy promptu wyciągnięte pomyślnie.")
        except Exception as e:
            logging.exception("Wystąpił błąd podczas wyciągania wniosków z analizy promptu.")
            QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wyciągania wniosków z analizy promptu: {str(e)}')

    # -------------------- Funkcje dla Procesów Generatywnych --------------------

    def define_alphabet(self):
        logging.info("Definiowanie alfabetu...")
        dialog = DefineAlphabetDialog(self)
        if dialog.exec_():
            alphabet = dialog.get_alphabet()
            self.language_def.define_alphabet(alphabet)
            QMessageBox.information(self, 'Alfabet Zdefiniowany',
                                    f'Alfabet: {", ".join(self.language_def.get_alphabet())}')
            logging.info(f'Alfabet zdefiniowany: {", ".join(self.language_def.get_alphabet())}')

    def define_grammar(self):
        logging.info("Dodawanie reguły gramatycznej...")
        dialog = DefineGrammarDialog(self)
        if dialog.exec_():
            rule = dialog.get_rule()
            self.language_def.define_grammar_rule(rule)
            QMessageBox.information(self, 'Reguła Dodana',
                                    f'Aktualne Reguły:\n' + "\n".join(self.language_def.get_grammar_rules()))
            logging.info(f'Reguła gramatyczna dodana: {rule}')

    def create_generative_process(self):
        logging.info("Tworzenie procesu generatywnego...")
        dialog = CreateGenerativeProcessDialog(self)
        if dialog.exec_():
            process_name = dialog.get_process_name()
            try:
                self.generative_process = GenerativeProcess(process_name)
                QMessageBox.information(self, 'Proces Utworzony',
                                        f'Proces generatywny "{process_name}" został utworzony.')
                logging.info(f'Proces generatywny utworzony: {process_name}')
                # Można dodać dalsze kroki do definiowania neuronów i synaps
            except Exception as e:
                logging.exception("Wystąpił błąd podczas tworzenia procesu generatywnego.")
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas tworzenia procesu generatywnego: {str(e)}')

    def visualize_synaptic_tree(self):
        logging.info("Wizualizacja drzewa synaptycznego...")
        if self.generative_process:
            try:
                self.generative_process.visualize_synaptic_tree()
                logging.info("Drzewo synaptyczne wizualizowane pomyślnie.")
            except Exception as e:
                logging.exception("Wystąpił błąd podczas wizualizacji drzewa synaptycznego.")
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wizualizacji drzewa synaptycznego: {str(e)}')
        else:
            QMessageBox.warning(self, 'Brak Procesu', 'Najpierw utwórz proces generatywny.')
            logging.warning("Próba wizualizacji drzewa synaptycznego bez utworzonego procesu generatywnego.")

    def generate_process_3d_artifact(self):
        logging.info("Generowanie 3D artefaktu drzewa synaptycznego...")
        try:
            if not self.generative_process:
                QMessageBox.warning(self, 'Brak Procesu', 'Najpierw utwórz proces generatywny.')
                logging.warning("Próba generowania 3D artefaktu bez utworzonego procesu generatywnego.")
                return
            # Przygotowanie neuronów do wizualizacji
            neurons = {}
            for node, data in self.generative_process.synaptic_tree.graph.nodes(data=True):
                neuron = Neuron(node, data.get('content', ''))
                neurons[node] = neuron
            for source, target, data in self.generative_process.synaptic_tree.graph.edges(data=True):
                weight = data.get('weight', 1.0)
                label = data.get('label', '')
                if source in neurons and target in neurons:
                    synapse = Synapse(source=neurons[source], target=neurons[target], type=label)
                    neurons[source].connect(neurons[target], synapse)
            neurons_list = list(neurons.values())
            logging.info(f"Liczba neuronów do wizualizacji: {len(neurons_list)}")
            for neuron in neurons_list:
                logging.info(f"Neuron: {neuron.name}, Połączenia: {[conn.target.name for conn in neuron.synapses]}")

            if not neurons_list:
                QMessageBox.warning(self, 'Brak Neuronów', 'Nie znaleziono neuronów do wizualizacji.')
                logging.warning("Brak neuronów do wizualizacji po parsowaniu relacji.")
                return

            # Inicjalizacja wizualizatora i wywołanie metody wizualizacji
            visualizer = NeuronVisualizer(neurons_list)
            visualizer.visualize(backend='plotly', parent=self)
            logging.info("3D artefakt drzewa synaptycznego wygenerowany pomyślnie.")
        except Exception as e:
            logging.exception("Wystąpił błąd podczas generowania 3D artefaktu drzewa synaptycznego.")
            QMessageBox.critical(self, 'Błąd',
                                 f'Wystąpił błąd podczas generowania 3D artefaktu drzewa synaptycznego: {str(e)}')

    def extract_conclusions_process(self):
        logging.info("Wyciąganie wniosków z procesu generatywnego...")
        try:
            if not self.generative_process:
                QMessageBox.warning(self, 'Brak Procesu', 'Najpierw utwórz proces generatywny.')
                logging.warning("Próba wyciągnięcia wniosków bez utworzonego procesu generatywnego.")
                return
            G = self.generative_process.synaptic_tree.graph
            if G.number_of_nodes() == 0:
                QMessageBox.warning(self, 'Puste Drzewo', 'Drzewo synaptyczne jest puste.')
                logging.warning("Próba wyciągnięcia wniosków z pustego drzewa synaptycznego.")
                return
            # Prosty przykład wyciągania wniosków: liczenie węzłów i krawędzi
            node_count = G.number_of_nodes()
            edge_count = G.number_of_edges()
            conclusions = f'Wnioski z procesu generatywnego "{self.generative_process.process_name}":\n'
            conclusions += f'Liczba neuronów: {node_count}\n'
            conclusions += f'Liczba synaps: {edge_count}\n'
            QMessageBox.information(self, 'Wnioski', conclusions)
            logging.info("Wnioski z procesu generatywnego wyciągnięte pomyślnie.")
        except Exception as e:
            logging.exception("Wystąpił błąd podczas wyciągania wniosków z procesu generatywnego.")
            QMessageBox.critical(self, 'Błąd',
                                 f'Wystąpił błąd podczas wyciągania wniosków z procesu generatywnego: {str(e)}')

    # -------------------- Metoda Testowa --------------------
    def test_visualization(self):
        logging.info("Test wizualizacji 3D...")
        try:
            neuron1 = Neuron("Neuron1", "Content1")
            neuron2 = Neuron("Neuron2", "Content2")
            neuron3 = Neuron("Neuron3", "Content3")

            synapse1 = Synapse(source=neuron1, target=neuron2, type='association')
            synapse2 = Synapse(source=neuron2, target=neuron3, type='object')
            synapse3 = Synapse(source=neuron3, target=neuron1, type='conjunction')

            neuron1.synapses.append(synapse1)
            neuron2.synapses.append(synapse2)
            neuron3.synapses.append(synapse3)

            neurons = [neuron1, neuron2, neuron3]
            visualizer = NeuronVisualizer(neurons)
            visualizer.visualize(backend='plotly', parent=self)
            logging.info("Test wizualizacji 3D zakończony pomyślnie.")
        except Exception as e:
            logging.exception("Błąd podczas testu wizualizacji 3D.")
            QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas testu wizualizacji 3D: {str(e)}')


# -------------------- Dialogi dla Definiowania Alfabetu i Gramatyki --------------------

class DefineAlphabetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Definiuj Alfabet")
        self.setGeometry(150, 150, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Wprowadź litery alfabetu oddzielone przecinkami:")
        layout.addWidget(self.label)

        self.alphabet_input = QLineEdit(self)
        layout.addWidget(self.alphabet_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_alphabet(self):
        text = self.alphabet_input.text()
        return [letter.strip() for letter in text.split(',') if letter.strip()]


class DefineGrammarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj Regułę Gramatyczną")
        self.setGeometry(150, 150, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Wprowadź regułę gramatyczną:")
        layout.addWidget(self.label)

        self.rule_input = QLineEdit(self)
        layout.addWidget(self.rule_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_rule(self):
        return self.rule_input.text().strip()


class CreateGenerativeProcessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Utwórz Proces Generatywny")
        self.setGeometry(150, 150, 400, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Wprowadź nazwę procesu generatywnego:")
        layout.addWidget(self.label)

        self.process_input = QLineEdit(self)
        layout.addWidget(self.process_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_process_name(self):
        return self.process_input.text().strip()
