import os
from models.scryfall import ScryfallCard
from util import get_abilities_from_rules, get_keywords_from_rules, get_card_names

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_OUT = os.path.join(BASE_DIR, 'data', 'out', 'card-names-with-abkws.txt')


def main():
    print('Loading data files')
    abilities = get_abilities_from_rules()
    keywords = get_keywords_from_rules()
    card_names = get_card_names()

    tots = abilities + keywords
    badnames = [x for x in tots if x in card_names]

    with open(DATA_OUT, 'w') as f:
        f.write('\n'.join(badnames))

    return badnames


def format_scry_search(names):
    return ' or '.join([f'!"{name}"' for name in names])


if __name__ == '__main__':
    names = main()
    print(format_scry_search(names))
