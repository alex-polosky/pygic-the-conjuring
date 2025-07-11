import json
import os
import re
from models.scryfall import ScryfallCard
from util import get_scryfall_cards, get_abilities_from_rules, get_keywords_from_rules

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_OUT = os.path.join(BASE_DIR, 'data', 'out', 'oracle-text.txt')


def replace(s: str, d: dict[str, str]) -> str:
    for k,v in d.items():
        s = s.replace(k, v)
    return s


def cardthings(card: ScryfallCard, ignore_card_names: list[str], set_types: list[str]):
    if card.set_type not in set_types:
        return
    if not any([x == 'legal' for x in card.legalities.values()]) and card.layout == 'normal' and card.set_type != 'token':# and card.layout not in ('planar', 'scheme'):
        return
    if 'Checklist' in card.name:
        return
    if card.oracle_text:
        faces = [(card.name, card.oracle_text)]
    elif card.card_faces:
        faces = [
            (face.name if face.name else card.name, face.oracle_text)
            for face in card.card_faces
        ]
    else:
        faces = []
    if card.oracle_text and card.card_faces:
        pass

    replacements = {}
    for i, face in enumerate(faces):
        name = face[0]
        if name.startswith('A-') and face[0][2:] in face[1]:
            name = name[2:]
        if name not in ignore_card_names:
            value = f'~{i if i else ""}'
            replacements[name] = value
            if ',' in name:
                replacements[name.split(',')[0]] = value
            value = value.replace('A-', '')

    return [
        line.split('(')[0].strip()
            for face in faces
        for line in replace(face[1], replacements).split('\n')
        if line
    ]

def main(set_types=['core','expansion','commander','token','masters']):
    print('Loading data files')
    data = get_scryfall_cards()
    abilities = get_abilities_from_rules()
    keywords = get_keywords_from_rules()
    texts = []

    ignore_card_names = [
        'Blessing',
        'Chaos',
        'Done',
        'Fly',
        'Leave',
        'Life',
        'Order',
        'Reduce',
        'Remove',
        'Return',
        'Take',
        'Turn',
        'Their','There', 'They\'re',
        'What', 'When','Where','Who', 'Why',
        'X',
    ] + abilities + keywords

    total = len(data)
    print(f'Chunk-ing {total} cards...')
    for i, oracle_id in enumerate(data):
        if i and i % 1_000 == 0:
            print(f'Loaded {i} cards: {i/total*100:0.2f}%')
        card = data[oracle_id]
        result = cardthings(card, ignore_card_names, set_types)
        if result:
            texts += result

    texts = sorted(set(texts))
    with open(DATA_OUT, 'w') as f:
        f.write('\n'.join(texts))


if __name__ == '__main__':
    main()
