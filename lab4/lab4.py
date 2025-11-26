import json

import numpy as np
from bs4 import BeautifulSoup
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

class Product:
    def __init__(self, name, id_):
        self.name = name
        self.id = id_


def read_json(filename):
    d = {}
    try:
        with open(filename) as f:
            d = json.load(f)
    except Exception as e:
        print(e)
        pass
    return d


def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower()
            for token in doc
            if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


if __name__ == '__main__':

    products_data = read_json('tesco_sample.json')
    print("Loaded json")

    products = []
    corpus = []

    print("Preprocessing text")
    for pd in products_data:
        html = pd.get('description', '')
        raw_text = BeautifulSoup(html, 'html.parser').get_text(" ", strip=True)

        preprocessed_text = preprocess_text(raw_text)

        p = Product(name=pd.get('name', ''), id_=pd.get('gtin13', ''))
        products.append(p)
        corpus.append(preprocessed_text)

    print("Vectorizing text")

    # Vectorize all descriptions of products
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)


    # Compute similarity matrix
    sim_matrix = cosine_similarity(tfidf_matrix)

    # Fill the identity diagonal with 1 values in order to remove self comparison
    np.fill_diagonal(sim_matrix, 1)

    # Find out the lowest cosine similarity
    i, j = np.unravel_index(sim_matrix.argmin(), sim_matrix.shape)

    print(f"Most similar products are {products[i].name} and {products[j].name}")
