from hashlib import md5
import json
import os
import pickle
from time import time
from uuid import UUID
from models.scryfall import ScryfallCard

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'lib', 'oracle-cards.json')
BIN_FILE = os.path.join(DATA_DIR, 'bin', 'oracle-cards.bin')


def load_json() -> dict[UUID, ScryfallCard]:
    with open(DATA_FILE) as f:
        data = [ScryfallCard(x) for x in json.load(f)]
    data = {
        card.oracle_id: card
        for card in data
    }
    return data


def load_bin() -> dict[UUID, ScryfallCard]:
    with open(BIN_FILE, 'rb') as f:
        b = f.read()
    with open(BIN_FILE + '.md5', 'r') as f:
        checksum = f.read()
    m = md5(b).hexdigest()
    if checksum != m:
        raise AssertionError('invalid checksum')
    data = pickle.loads(b)
    return data


def timeit(f, n=10, args=[], kwargs={}):
    times = []
    for i in range(n):
        start = time()
        f(*args, **kwargs)
        end = time()
        times.append(end - start)
    return sum(times) / n


def main():
    js = timeit(load_json)
    bi = timeit(load_bin)
    print('Average for 10 runs:')
    print(f'JSON: {js:0.6f}')
    print(f'BIN : {bi:0.6f}')


if __name__ == '__main__':
    main()
