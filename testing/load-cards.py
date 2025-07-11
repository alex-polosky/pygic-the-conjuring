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


with open(CARDS_FILE) as f:
    data = json.load(f)

for x in data:
    y = ScryfallCard(**x)
