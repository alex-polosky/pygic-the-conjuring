from hashlib import md5
import json
import os
import pickle
import re
from time import time
from uuid import UUID
from models.scryfall import ScryfallCard

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
BIN_FILE = os.path.join(DATA_DIR, 'bin', 'oracle-cards.bin')
CARDS_FILE = os.path.join(DATA_DIR, 'lib', 'oracle-cards.json')
CARD_NAME_FILE = os.path.join(DATA_DIR, 'lib', 'oracle-names.txt')

ABILITY_RE = re.compile(r'701\.\d+\. (.*)')
KEYWORD_RE = re.compile(r'702\.\d+\. (.*)')


def timeit(f, n=10, args=[], kwargs={}):
    times = []
    for i in range(n):
        start = time()
        f(*args, **kwargs)
        end = time()
        times.append(end - start)
    return sum(times) / n


def get_scryfall_cards_via_json() -> dict[UUID, ScryfallCard]:
    with open(CARDS_FILE) as f:
        data = [ScryfallCard(**x) for x in json.load(f)]
    data = {
        card.oracle_id: card
        for card in data
    }
    return data


def get_scryfall_cards() -> dict[UUID, ScryfallCard]:
    with open(BIN_FILE, 'rb') as f:
        b = f.read()
    with open(BIN_FILE + '.md5', 'r') as f:
        checksum = f.read()
    m = md5(b).hexdigest()
    if checksum != m:
        raise AssertionError('invalid checksum')
    data = pickle.loads(b)
    return data


def get_card_names() -> list[str]:
    with open(CARD_NAME_FILE) as f:
        data = [x for x in f.read().split('\n') if x]
    return data


def get_latest_magic_rules() -> str:
    path = os.path.join(DATA_DIR, 'lib')
    matches = [name for name in os.listdir(path) if name.lower().startswith('magiccomprules') and name.lower().endswith('.txt')]
    newest = 0
    filename = ''
    for m in matches:
        dt = int(m.split('.')[0][-8:])
        if dt > newest:
            newest = dt
            filename = m
    with open(os.path.join(path, filename)) as f:
        data = f.read()
    return data


def get_abilities_from_rules() -> list[str]:
    rules = get_latest_magic_rules()
    matches = ABILITY_RE.findall(rules)[1:]
    return matches


def get_keywords_from_rules() -> list[str]:
    rules = get_latest_magic_rules()
    matches = KEYWORD_RE.findall(rules)[1:]
    return matches
