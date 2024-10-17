# File: meta_architecture/dependency_parser.py
# Author: cha0s
# Date: 2024-10-16

import spacy
import stanza
import logging


class DependencyParser:
    def __init__(self, system='UD'):
        self.system = system.lower()
        self.ud_mapping = self.load_ud_dependencies()
        self.stanford_mapping = self.load_stanford_dependencies()
        try:
            if self.system == 'ud':
                try:
                    self.nlp = spacy.load('pl_core_news_sm')
                    logging.info("DependencyParser initialized with Universal Dependencies (UD) system.")
                except OSError:
                    logging.info("Model 'pl_core_news_sm' nie jest zainstalowany. Pobieranie...")
                    from spacy.cli import download
                    download('pl_core_news_sm')
                    self.nlp = spacy.load('pl_core_news_sm')
                    logging.info("Model 'pl_core_news_sm' został pomyślnie zainstalowany i załadowany.")
            elif self.system == 'stanford':
                stanza.download('pl', processors='tokenize,pos,lemma,depparse', verbose=False)
                self.nlp = stanza.Pipeline('pl', processors='tokenize,pos,lemma,depparse', verbose=False, use_gpu=False)
                logging.info("DependencyParser initialized with Stanford Dependencies system via Stanza.")
            else:
                raise ValueError(f"Unsupported dependency system: {self.system}")
        except Exception as e:
            logging.error(f"Nie udało się załadować parsera zależności: {e}")
            raise e

    def load_ud_dependencies(self):
        return {
            'nsubj': 'nominal subject',
            'obj': 'object',
            'dobj': 'direct object',
            'iobj': 'indirect object',
            'amod': 'adjective modifier',
            'advmod': 'adverbial modifier',
            'case': 'case marker',
            'nmod': 'nominal modifier',
            'det': 'determiner',
            'punct': 'punctuation',
            'conj': 'conjunction',
            'compound': 'compound modifier',
            'obl': 'oblique nominal',
            'root': 'root',
            'acl': 'clausal modifier of noun',
            'advcl': 'adverbial clause modifier',
            'ccomp': 'clausal complement',
            'xcomp': 'open clausal complement',
            'cc': 'coordinating conjunction',
            'mark': 'marker',
            'dep': 'unspecified dependency',
            'expl': 'expletive',
            'parataxis': 'parataxis',
            'discourse': 'discourse element',
            'list': 'list',
            'orphan': 'orphan',
            'goeswith': 'goes with',
            'reparandum': 'reparandum',
            # Dodaj więcej zależności w razie potrzeby
        }

    def load_stanford_dependencies(self):
        return {
            'nsubj': 'nominal subject',
            'obj': 'object',
            'dobj': 'direct object',
            'iobj': 'indirect object',
            'amod': 'adjectival modifier',
            'advmod': 'adverbial modifier',
            'prep': 'prepositional modifier',
            'case': 'case marker',
            'nmod': 'nominal modifier',
            'det': 'determiner',
            'punct': 'punctuation',
            'conj': 'conjunction',
            'compound': 'compound modifier',
            'obl': 'oblique nominal',
            'root': 'root',
            'acl': 'clausal modifier of noun',
            'advcl': 'adverbial clause modifier',
            'ccomp': 'clausal complement',
            'xcomp': 'open clausal complement',
            'cc': 'coordinating conjunction',
            'mark': 'marker',
            'dep': 'unspecified dependency',
            'expl': 'expletive',
            'parataxis': 'parataxis',
            'discourse': 'discourse element',
            'list': 'list',
            'orphan': 'orphan',
            'goeswith': 'goes with',
            'reparandum': 'reparandum',
            # Dodaj więcej zależności w razie potrzeby
        }

    def parse(self, text):
        if self.system == 'ud':
            return self.parse_ud(text)
        elif self.system == 'stanford':
            return self.parse_stanford(text)

    def parse_ud(self, text):
        doc = self.nlp(text)
        parsed_relations = []
        for token in doc:
            dep_full = token.dep_.lower()
            # Rozdzielenie zależności z prefiksem
            if ':' in dep_full:
                dep_base = dep_full.split(':')[0]
            else:
                dep_base = dep_full
            dep = self.ud_mapping.get(dep_base, 'unknown')
            if dep == 'unknown':
                logging.warning(f"Nieznana zależność: {dep_full} dla słowa: {token.text}")
            parsed_relations.append({
                'word': token.text,
                'dependency': dep,
                'head': token.head.text if token.head else 'ROOT',
                'pos': token.pos_
            })
        logging.info(f"Parsed relations (UD): {parsed_relations}")
        return parsed_relations

    def parse_stanford(self, text):
        doc = self.nlp(text)
        parsed_relations = []
        for sentence in doc.sentences:
            for word in sentence.words:
                dep_full = word.deprel.lower()
                # Rozdzielenie zależności z prefiksem
                if ':' in dep_full:
                    dep_base = dep_full.split(':')[0]
                else:
                    dep_base = dep_full
                dep = self.stanford_mapping.get(dep_base, 'unknown')
                if dep == 'unknown':
                    logging.warning(f"Nieznana zależność: {dep_full} dla słowa: {word.text}")
                head = sentence.words[word.head - 1].text if word.head > 0 else 'ROOT'
                pos = word.upos  # Universal POS
                parsed_relations.append({
                    'word': word.text,
                    'dependency': dep,
                    'head': head,
                    'pos': pos
                })
        logging.info(f"Parsed relations (Stanford): {parsed_relations}")
        return parsed_relations
