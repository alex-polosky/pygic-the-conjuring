from hashlib import md5
import json
import os
import pickle
from models.scryfall import ScryfallCard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'lib', 'oracle-cards.json')
BIN_FILE = os.path.join(DATA_DIR, 'bin', 'oracle-cards.bin')


def main():
    with open(DATA_FILE) as f:
        data = [ScryfallCard(**x) for x in json.load(f)]
    data = {
        card.oracle_id: card
        for card in data
    }
    b = pickle.dumps(data)
    m = md5(b).hexdigest()
    with open(BIN_FILE, 'wb') as f:
        f.write(b)
    with open(BIN_FILE + '.md5', 'w') as f:
        f.write(m)


if __name__ == '__main__':
    main()
