import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark'), encoding='utf-8') as f:
    grammar = f.read()

class MTGTransformer(Transformer):
    pass

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)
transformer = MTGTransformer()

# test it:
for expr, expected in (
("{2}{W}, {T}, Sacrifice a green creature, a white creature, and a blue creature", ["{2}{W}", "{T}", "Sacrifice a green creature, a white creature, and a blue creature"]),
("{3}, {T} or {G}, {T}", ["{3}", "{T} or {G}", "{T}"]),
("{3}{G}{W}, {T}, Tap two untapped creatures you control, Sacrifice ~", ["{3}{G}{W}", "{T}", "Tap two untapped creatures you control", "Sacrifice ~"]),
("{T}, Tap two untapped green, white, or blue creatures you control, Sacrifice ~", ["{T}", "Tap two untapped green, white, or blue creatures you control", "Sacrifice ~"]),
("• ~ deals 2 damage to each creature, planeswalker, and battle.", ["• ~ deals 2 damage to each creature, planeswalker, and battle."]),
("• Counter target spell, activated ability, or triggered ability. Its controller draws a card.", ["• Counter target spell, activated ability, or triggered ability.", "Its controller draws a card."]),
("~ deals 2 damage to target player and each creature that player controls. Search your library and/or graveyard for a card named Chandra, Flame's Fury, reveal it, and put it into your hand. If you search your library this way, shuffle.", ["~ deals 2 damage to target player and each creature that player controls.", "Search your library and/or graveyard for a card named Chandra, Flame's Fury, reveal it, and put it into your hand.", "If you search your library this way, shuffle."]),
("~ is also a Cleric, Rogue, Warrior, and Wizard.", ["~ is also a Cleric, Rogue, Warrior, and Wizard."]),
("As ~ enters the battlefield, turn all other nontoken creatures face down.", ["As ~ enters the battlefield, turn all other nontoken creatures face down."]),
("Legendary creatures you control get +1/+0 and gain indestructible until end of turn.", ["Legendary creatures you control get +1/+0 and gain indestructible until end of turn."]),
("Legendary Humans you control have indestructible.", ["Legendary Humans you control have indestructible."]),
("Legendary spells you cast cost {1} less to cast.", ["Legendary spells you cast cost {1} less to cast."]),
("Other legendary creatures you control get +2/+2.", ["Other legendary creatures you control get +2/+2."]),
("Put nine +1/+1 counters on target land you control. It becomes a legendary 0/0 Elemental creature with haste named Vitu-Ghazi. It's still a land.", ["Put nine +1/+1 counters on target land you control.", "It becomes a legendary 0/0 Elemental creature with haste named Vitu-Ghazi.", "It's still a land."]),
):
    # print(expr)

    tree = parser.parse(expr)
    # if isinstance(tree, Tree):
    #     print(tree.pretty())
    # else:
    #     print(tree)

    result = transformer.transform(tree)
    # print(result)

    print(result == expected)

    print('')
