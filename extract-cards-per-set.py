import json
import os
from models.scryfall import ScryfallCard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'lib', 'oracle-bulk.json')
DATA_FILE_OUT = os.path.join(DATA_DIR, 'out', 'cards-per-set.json')


def main():
    print('Loading data file')
    with open(DATA_FILE) as f:
        data = json.load(f)
    sets = {}
    total = len(data)
    print(f'Set-ting {total} cards...')
    for i, card_json in enumerate(data):
        if i and i % 1_000 == 0:
            print(f'Loaded {i} cards: {i/total*100:0.2f}%')
        card = ScryfallCard(card_json)
        if card.set not in sets:
            sets[card.set] = []
        id_ = str(card.oracle_id)
        if id_ not in sets[card.set]:
            sets[card.set].append(id_)
    with open(DATA_FILE_OUT, 'w') as f:
        json.dump(sets, f, indent=4)


if __name__ == '__main__':
    main()
