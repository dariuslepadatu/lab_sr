import json

import numpy as np
from bs4 import BeautifulSoup
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

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
    taken_ids = []
    for pd in products_data:
        if pd.get('gtin13', '') not in taken_ids:
            html = pd.get('description', '')
            raw_text = BeautifulSoup(html, 'html.parser').get_text(" ", strip=True)
            preprocessed_text = preprocess_text(raw_text)
            products.append({'name': pd.get('name', ''), 'id': pd.get('gtin13', ''), 'text': preprocessed_text})
            taken_ids.append(pd.get('gtin13', ''))
    print("Preprocessed text")


    corpus = [p.get('text', '') for p in products]

    # Vectorize all descriptions of products
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print("Vectorized text")

    # Compute similarity matrix
    sim_matrix = cosine_similarity(tfidf_matrix)

    # Fill the identity diagonal with 0 values in order to remove self comparison
    np.fill_diagonal(sim_matrix, 0)
    print(sim_matrix)

    # Find out the cosine similarity
    i, j = np.unravel_index(sim_matrix.argmax(), sim_matrix.shape)

    print(f"Most similar products: {products[i].get('id', '')} and {products[j].get('id', '')} -> Score {sim_matrix[i, j]:.4f}")
