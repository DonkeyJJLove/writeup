# The file **`dependency_parser.py`** defines the `DependencyParser` class, which handles linguistic parsing using two different systems: Universal Dependencies (UD) and Stanford Dependencies (via the Stanza library). Here's a detailed breakdown of the class and its functionality:

### **Key Components of `dependency_parser.py`**

#### 1. **Initialization (`__init__` Method):**
   - The class is initialized with an argument `system`, which determines whether the Universal Dependencies (UD) or Stanford Dependencies system is used for parsing.
   - The parser loads different language models depending on the selected system:
     - **Universal Dependencies (UD)**: It uses the **spaCy** library and the `pl_core_news_sm` model (specifically for Polish).
     - **Stanford Dependencies**: It uses the **Stanza** library with processors for tokenization, part-of-speech tagging, lemmatization, and dependency parsing.
   
   ```python
   if self.system == 'ud':
       self.nlp = spacy.load('pl_core_news_sm')
   elif self.system == 'stanford':
       stanza.download('pl', processors='tokenize,pos,lemma,depparse')
       self.nlp = stanza.Pipeline('pl', processors='tokenize,pos,lemma,depparse')
   ```

#### 2. **Loading Dependency Mappings:**
   - Two methods are responsible for loading mappings that translate dependency labels (like "nsubj" for nominal subject) into more readable descriptions.
     - **`load_ud_dependencies()`**: Loads mappings for Universal Dependencies (UD).
     - **`load_stanford_dependencies()`**: Loads mappings for Stanford Dependencies.
   
   These mappings help translate dependency labels into human-readable terms for better understanding during the parsing process.

   ```python
   self.ud_mapping = self.load_ud_dependencies()
   self.stanford_mapping = self.load_stanford_dependencies()
   ```

#### 3. **Parsing Methods:**
   The parser has two key methods for parsing text depending on the selected system:

   - **`parse_ud()`**: This method uses the **spaCy** model for UD to process text. It extracts the word, its dependency, the head of the dependency (the word it depends on), and the part of speech (POS) tag. It maps dependency labels to readable forms using `self.ud_mapping`.
   
   ```python
   def parse_ud(self, text):
       doc = self.nlp(text)
       for token in doc:
           dep = self.ud_mapping.get(token.dep_.lower(), 'unknown')
           parsed_relations.append({
               'word': token.text,
               'dependency': dep,
               'head': token.head.text,
               'pos': token.pos_
           })
   ```

   - **`parse_stanford()`**: This method uses the **Stanza** model for Stanford Dependencies. It follows a similar structure to `parse_ud()` but processes the text using Stanza’s pipeline and maps dependencies using `self.stanford_mapping`.

   ```python
   def parse_stanford(self, text):
       doc = self.nlp(text)
       for sentence in doc.sentences:
           for word in sentence.words:
               dep = self.stanford_mapping.get(word.deprel.lower(), 'unknown')
               parsed_relations.append({
                   'word': word.text,
                   'dependency': dep,
                   'head': head,
                   'pos': pos
               })
   ```

#### 4. **Error Handling and Logging:**
   The code has extensive logging to track the initialization of models and parsing processes. Any issues encountered during initialization or parsing (such as missing models or unknown dependencies) are logged as warnings or errors.

   ```python
   logging.error(f"Nie udało się załadować parsera zależności: {e}")
   ```

### **Summary:**
The `DependencyParser` class in **`dependency_parser.py`** provides a flexible framework for processing text and extracting syntactic dependencies. It supports two parsing systems:
- **Universal Dependencies (UD)**: Uses **spaCy** to process and map linguistic relationships.
- **Stanford Dependencies**: Uses **Stanza** to parse text with dependency labels and part-of-speech tagging.

The class allows for detailed linguistic analysis by mapping abstract dependency labels to more understandable descriptions, which are logged for transparency.