# File: meta_architecture/prompt_parser.py
# Author: cha0s
# Date: 1728854400

"""
============================================================
File: prompt_parser.py
Author: cha0s
Date: 1728854400
Description:
    Ten moduł implementuje PromptParser, który wykorzystuje DependencyParser do analizy tekstu.

    Funkcjonalności:
        - Parsowanie promptów przy użyciu DependencyParser.
        - Logowanie procesu parsowania.

Future Enhancements:
    - Dodanie bardziej zaawansowanych metod analizy promptów.
    - Integracja z innymi narzędziami NLP.
============================================================
"""

import logging
from meta_architecture.dependency_parser import DependencyParser


class PromptParser:
    def __init__(self, system='UD'):
        self.dependency_parser = DependencyParser(system=system)
        logging.info(f"PromptParser initialized with DependencyParser system: {system}")

    def parse_prompt(self, prompt):
        """
        Parsuje prompt i zwraca analizę zależności.

        :param prompt: Tekst promptu
        :return: Lista relacji zależności
        """
        logging.info("Parsowanie promptu za pomocą DependencyParser...")
        parsed_relations = self.dependency_parser.parse(prompt)
        logging.info(f"Parsed relations: {parsed_relations}")
        return parsed_relations
