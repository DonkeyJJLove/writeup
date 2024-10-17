# File: meta_architecture/synapse_language.py
# Author: cha0s
# Date: 2024-04-26

"""
============================================================
File: synapse_language.py
Author: cha0s
Date: 2024-04-26
Description:
    Implementacja klasy SynapseLanguage definiującej reguły synaptyczne
    na podstawie części mowy źródła i celu.

    Funkcjonalności:
        - Definiowanie reguł synaptycznych.
        - Zarządzanie regułami.

Future Enhancements:
    - Dodanie reguł dynamicznych na podstawie analizy danych.
    - Integracja z systemami uczenia maszynowego do automatycznego tworzenia reguł.
============================================================
"""

import logging


class SynapseLanguage:
    def __init__(self):
        self.rules = []
        self.alphabet = []  # Opcjonalnie: lista wszystkich części mowy używanych w regułach
        self.define_default_rules()

    def add_rule(self, rule):
        """
        Dodaje regułę synaptyczną.

        :param rule: Słownik z kluczami 'source_pos', 'target_pos', 'type'
        """
        self.rules.append(rule)
        if rule['source_pos'] not in self.alphabet:
            self.alphabet.append(rule['source_pos'])
        if rule['target_pos'] not in self.alphabet:
            self.alphabet.append(rule['target_pos'])
        logging.info(f"Reguła synaptyczna dodana: {rule}")

    def define_default_rules(self):
        """
        Definiuje domyślne reguły synaptyczne.
        """
        # Przykładowa reguła: rzeczownik może być połączony z czasownikiem
        self.add_rule({'source_pos': 'NOUN', 'target_pos': 'VERB', 'type': 'association'})
        # Dodaj inne reguły według potrzeb
        self.add_rule({'source_pos': 'ADP', 'target_pos': 'NOUN', 'type': 'prepositional modifier'})
        self.add_rule({'source_pos': 'VERB', 'target_pos': 'NOUN', 'type': 'object'})
        self.add_rule({'source_pos': 'VERB', 'target_pos': 'ADP', 'type': 'prepositional modifier'})
        self.add_rule({'source_pos': 'VERB', 'target_pos': 'VERB', 'type': 'conjunction'})
        self.add_rule({'source_pos': 'NOUN', 'target_pos': 'NOUN', 'type': 'compound modifier'})
        self.add_rule({'source_pos': 'ADJ', 'target_pos': 'NOUN', 'type': 'adjective modifier'})
        self.add_rule({'source_pos': 'ADV', 'target_pos': 'VERB', 'type': 'adverbial modifier'})
        self.add_rule({'source_pos': 'DET', 'target_pos': 'NOUN', 'type': 'determiner'})
        self.add_rule({'source_pos': 'CONJ', 'target_pos': 'NOUN', 'type': 'conjunction'})
        self.add_rule({'source_pos': 'PUNCT', 'target_pos': 'VERB', 'type': 'punctuation'})
        self.add_rule({'source_pos': 'CL', 'target_pos': 'NOUN', 'type': 'clausal modifier'})
        self.add_rule({'source_pos': 'COORD', 'target_pos': 'NOUN', 'type': 'coordinating conjunction'})
        self.add_rule({'source_pos': 'RELCL', 'target_pos': 'NOUN', 'type': 'relative clausal modifier'})
        self.add_rule({'source_pos': 'XCOMP', 'target_pos': 'VERB', 'type': 'open clausal complement'})
        self.add_rule({'source_pos': 'DEPV', 'target_pos': 'VERB', 'type': 'dependency'})
        self.add_rule({'source_pos': 'EXPL', 'target_pos': 'VERB', 'type': 'expletive'})
        self.add_rule({'source_pos': 'PARATAXIS', 'target_pos': 'VERB', 'type': 'parataxis'})
        self.add_rule({'source_pos': 'DISCOURSE', 'target_pos': 'VERB', 'type': 'discourse element'})
        self.add_rule({'source_pos': 'LIST', 'target_pos': 'NOUN', 'type': 'list'})
        self.add_rule({'source_pos': 'ORPHAN', 'target_pos': 'NOUN', 'type': 'orphan'})
        self.add_rule({'source_pos': 'GOESWITH', 'target_pos': 'NOUN', 'type': 'goes with'})
        self.add_rule({'source_pos': 'REPARANDUM', 'target_pos': 'NOUN', 'type': 'reparandum'})
        # Dodaj więcej reguł dla nowych zależności
        logging.info("Domyślne reguły synaptyczne zdefiniowane.")
