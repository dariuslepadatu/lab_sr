import json
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_sm")

class Product:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.vectorized = None

    def compute_cosine_similarity(self):
        self.vectorized = [1]


def read_json(filename):
    d = {}
    try:
        with open(filename) as f:
            d = json.load(f)
    except Exception as e:
        print(e)
        pass
    return d


def preprocess_text(text: str) -> list[str]:
    """
    Pipeline:
    1. tokenize
    2. lowercase
    3. lemmatize
    4. remove stopwords + punctuation + non-alphabetic tokens
    """
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha ]
    return tokens



if __name__ == '__main__':
    products_data = read_json('tesco_sample.json')
    for product in products_data:
        html = product.get('description', '')
        text = BeautifulSoup(html, 'html.parser').get_text(" ", strip=True)
        processed_text = preprocess_text(text)
        print(processed_text)
        print("==========================")


