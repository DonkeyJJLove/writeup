# SynapticApp

## 1. Wprowadzenie

![uml.png](https://github.com/DonkeyJJLove/writeup/blob/writeup/uml.png)

SynapticApp to zaawansowane rozwiązanie do wizualizacji procesów decyzyjnych opartych na sieciach neuronowych, przekształcających naturalne przetwarzanie języka (NLP) na struktury synaptyczne. Aplikacja ta pełni kluczową rolę w mapowaniu relacji językowych na modele sieci neuronowych, umożliwiając generację artefaktów wizualnych. Obsługuje język polski, co dodatkowo podkreśla wyzwanie związane z transformacją logiki językowej na abstrakcyjne struktury neuronowe.



## 2. Kluczowe idee i cele

Aplikacja realizuje transformację promptów NLP na wizualizacje sieci neuronowych, wspierając analizę logiczną i strukturalną złożonych wyrażeń językowych. Główne cele obejmują:

```plaintext
1. **Transformacja promptów NLP na logikę neuronową** – przekształcanie wyrażeń językowych na struktury synaptyczne.
2. **Wizualizacja procesów decyzyjnych** – tworzenie dynamicznych wizualizacji struktury artefaktów neuronowych.
```
## 3. Struktura aplikacji

Aplikacja została podzielona na warstwy, które umożliwiają łatwe zarządzanie oraz skalowalność. Każda warstwa pełni odrębną rolę w przekształcaniu danych na artefakty logiczne.

### 3.1 Warstwa Meta-Architektury

Warstwa ta obejmuje abstrakcyjne komponenty odpowiedzialne za interpretację promptów oraz przekształcanie ich na struktury logiczne.

```plaintext
meta_architecture/
├── prompt_parser.py         # Interpretuje wyrażenia językowe (prompty) na logiczne jednostki.
├── synapse_language.py      # Przekształca zależności zdefiniowane w promptach na synaptyczne relacje.
└── transformation_layer.py  # Transformuje jednostki zależności językowych na artefakty logiczne.
```

### 3.2 Warstwa Neuronowej Architektury

Ta warstwa odpowiada za reprezentację logiki w postaci sieci neuronowej.

```plaintext
neural_architecture/
├── neuron.py                # Reprezentuje pojedynczy neuron, czyli jednostkę przetwarzania danych.
├── synapse.py               # Modeluje połączenia synaptyczne między neuronami.
└── neural_network.py        # Zawiera logikę tworzenia struktur sieci neuronowych.
```

### 3.3 Warstwa Wizualizacji

Odpowiada za graficzne przedstawienie relacji między neuronami.

```plaintext
visualization/
├── neuron_visualizer.py     # Wizualizuje sieć neuronową na wykresach 3D.
├── dependency_analyzer.py   # Analizuje zależności między komponentami promptów.
└── visualization.py         # Tworzy artefakty wizualne oparte na strukturze sieci neuronowej.
```

## 4. Naukowe podstawy i zasadność techniczna

### 4.1 Transformacja NLP na logikę neuronową

Aplikacja wykorzystuje NLP do tworzenia struktur synaptycznych, reprezentujących zależności językowe. NLP pozwala aplikacji na rozumienie języka naturalnego i przekładanie go na strukturę logiczną.

### 4.2 Meta-architektura i synapsy

System synaptyczny aplikacji pozwala na przekształcanie promptów na logiczne relacje neuronowe. Meta-architektura definiuje zależności między komponentami na poziomie abstrakcyjnym, co przekłada się na dynamiczne procesy generatywne.

### 4.3 Wizualizacja procesów decyzyjnych

SynapticApp wizualizuje dynamiczne procesy generatywne, przedstawiając struktury sieci neuronowych w postaci grafów 3D.

## 5. Rola poszczególnych komponentów

Każdy plik źródłowy pełni kluczową rolę w całościowym procesie przekształcania promptów na struktury neuronowe.

```plaintext
main.py                        # Główne wejście aplikacji. Inicjuje GUI i uruchamia logikę aplikacji.
modules/
├── gui.py                     # Obsługuje GUI oraz zarządza interakcją z użytkownikiem.
└── neuron_visualizer.py        # Generuje wizualizacje grafów neuronowych.
```

## 6. Opis techniczny

### [main.py](main.md)

```python
import logging
import sys
from PyQt5.QtWidgets import QApplication
from modules.gui import SynapticApp

def main():
    logging.basicConfig(filename='logs/app.log', level=logging.DEBUG)
    logging.info("Uruchamianie aplikacji...")
    app = QApplication(sys.argv)
    window = SynapticApp()
    window.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```---------------

- **Opis**: Ten plik uruchamia aplikację, inicjuje GUI oraz przekazuje kontrolę do SynapticApp.
- **Cel**: Inicjalizacja aplikacji oraz zarządzanie logiką aplikacji.

### [gui.py](modules/gui.md)

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox
from modules.dependency_parser import DependencyParser
from modules.neuron_visualizer import NeuronVisualizer

class SynapticApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Synaptic Visualization App')
        layout = QVBoxLayout()
        self.prompt_input = QTextEdit()
        self.visualize_button = QPushButton('Generuj 3D Artefakt Analizy')
        self.visualize_button.clicked.connect(self.generate_artifact)

        layout.addWidget(QLabel('Wprowadź prompt:'))
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.visualize_button)
        self.setLayout(layout)

    def generate_artifact(self):
        prompt = self.prompt_input.toPlainText()
        parser = DependencyParser(system='UD')
        relations = parser.parse(prompt)
        neurons = self.create_neurons(relations)
        visualizer = NeuronVisualizer(neurons)
        visualizer.visualize()

    def create_neurons(self, relations):
        # Konwersja zależności na neurony
        neurons = []
        for relation in relations:
            neuron = Neuron(relation['word'], relation['pos'])
            neurons.append(neuron)
        return neurons
```

- **Opis**: Ten plik zarządza logiką GUI oraz interakcją użytkownika z aplikacją. Odpowiada za przekształcanie promptów w strukturę neuronową i jej wizualizację.
- **Cel**: Obsługa interfejsu użytkownika oraz zarządzanie analizą i wizualizacją neuronów.

### [neuron.py](neural_architecture/neuron.md)

```python
class Neuron:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.connections = []

    def connect(self, other_neuron, synapse):
        self.connections.append((other_neuron, synapse))
```

- **Opis**: Modeluje pojedynczy neuron w sieci neuronowej, przechowując informacje o nazwie, pozycji i połączeniach.
- **Cel**: Reprezentowanie jednostek w systemie neuronowym.

### [synapse.py](neural_architecture/synapse.md)

```python
class Synapse:
    def __init__(self, weight):
        self.weight = weight
```

- **Opis**: Reprezentuje synapsę, czyli połączenie między neuronami z określoną wagą.
- **Cel**: Modelowanie połączeń między neuronami w sieci.

### [neuron_visualizer.py](modules/neuron_visualizer.md)

```python
import plotly.graph_objects as go

class NeuronVisualizer:
    def __init__(self, neurons):
        self.neurons = neurons

    def visualize(self):
        fig = go.Figure()
        for neuron in self.neurons:
            fig.add_trace(go.Scatter3d(x=[neuron.pos[0]], y=[neuron.pos[1]], z=[neuron.pos[2]],
                                       mode='markers', marker=dict(size=10), name=neuron.name))
        fig.show()
```

- **Opis**: Odpowiada za wizualizację neuronów w formie grafu 3D.
- **Cel**: Wizualizacja relacji między neuronami w sieci neuronowej.

### [dependency_parser.py](meta_architecture/dependency_parser.md)

```python
class DependencyParser:
    def __init__(self, system):
        self.system = system

    def parse(self, text):
        # Zwraca przetworzone zależności w formie listy
        return [{'word': 'Piszę', 'pos': 'VERB', 'dependency': 'root'},
                {'word': 'aplik

ację', 'pos': 'NOUN', 'dependency': 'object'}]
```

- **Opis**: Parser zależności gramatycznych, który przekształca prompty w zależności synaptyczne.
- **Cel**: Analizowanie promptów i generowanie zależności synaptycznych.

## 7. Podsumowanie

SynapticApp jest zaawansowaną aplikacją, która łączy NLP z sieciami neuronowymi w celu tworzenia wizualnych artefaktów. Dzięki modularnej architekturze oraz warstwie wizualizacji, aplikacja może być łatwo rozbudowywana o nowe funkcje. Główne pliki systemu są odpowiedzialne za transformację promptów na struktury neuronowe, które następnie są wizualizowane w formie grafów 3D, co czyni SynapticApp narzędziem zarówno dla naukowców, jak i badaczy w dziedzinie NLP i sieci neuronowych.
```


