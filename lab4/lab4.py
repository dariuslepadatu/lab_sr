import json
from bs4 import BeautifulSoup

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


if __name__ == '__main__':
    products_data = read_json('tesco_sample.json')
    for product in products_data:
        html = product.get('description', '')
        text = BeautifulSoup(html, 'html.parser').get_text(" ", strip=True)
        print(text)
        print("==========================")


