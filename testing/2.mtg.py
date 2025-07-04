import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark')) as f:
    grammar = f.read()

class MTGTransformer(Transformer):
    pass

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)
transformer = MTGTransformer()

for expr in (
'Choose one —',
'• Burn Down the House deals 5 damage to each creature and each planeswalker.',
'• Create 2 2/1 red Goblin creature tokens with SUB_TEXT_0.',
'• Create three 1/1 red Devil creature tokens with SUB_TEXT_1. They gain haste until end of turn.',
'{T}, Sacrifice this creature: Deal 2 damage to any target.',
'When this creature dies, it deals 1 damage to any target.',
'Activated abilities of nontoken Rebels cost an additional SUB_TEXT_0 to activate.',
'Sacrifice a land',
"Whenever a nontoken creature enters the battlefield under your control, you may pay {2}. If you do, create a token that's a copy of that creature, except it has haste and SUB_TEXT_0.",
'At the beginning of the end step, sacrifice this permanent.',
'Until end of turn, lands you control gain SUB_TEXT_0.',
'{T}: Add one mana of any color.',
'{1}{W}: Until end of turn, target creature gains SUB_TEXT_0.',
"This creature can't attack or block unless its controller pays {1} for each Cleric on the battlefield.",
'Enchant land',
'Enchanted land has SUB_TEXT_0.',
'{T}, Discard a card: Gain control of target creature until end of turn.',
'All Slivers have SUB_TEXT_0.',
'{T}: Target Sliver creature gets +X/+0 until end of turn, where X is the number of Slivers on the battlefield.',
'Prevent all damage that would be dealt to Glittering Lion.',
'{3}: Until end of turn, Glittering Lion loses SUB_TEXT_0. Any player may activate this ability.',
'Prevent all damage that would be dealt to Glittering Lion.',
'Choose one —',
'• Burn Down the House deals 5 damage to each creature and each planeswalker.',
'• Create three 1/1 red Devil creature tokens with SUB_TEXT_0. They gain haste until end of turn.',
'When this creature dies, it deals 1 damage to any target.',
'Whenever Totentanz, Swarm Piper or another nontoken creature you control dies, create a 1/1 black Rat creature token with SUB_TEXT_0.',
"This creature can't block.",
'You get an emblem with SUB_TEXT_0.',
'Islands you control have INNER_TEXT_0.',
'{T}: Draw a card.',
'{1}, {T}: Add {W}{U}.',
"{1}, Sacrifice Darigaaz's Attendant: Add {B}{R}{G}.",
'Flying\nHexavus enters the battlefield with six +1/+1 counters on it.\n{1}, Remove a +1/+1 counter from Hexavus: Put a flying counter on another target creature.\n{1}, Remove a counter from another creature you control: Put a +1/+1 counter on Hexavus.',
'{2}, {T}: Prevent all damage that would be dealt this turn by a source of your choice that shares a color with the exiled card.',
'{4}{W}{W}: Creatures you control get +2/+2 and gain first strike and lifelink until end of turn.',
'At the beginning of your upkeep, Nettletooth Djinn deals 1 damage to you.',
"Skulk (This creature can't be blocked by creatures with greater power.)\nAt the beginning of your end step, each opponent dealt combat damage this game by a creature named Gollum, Obsessed Stalker loses life equal to the amount of life you gained this turn.",
'If an opponent would gain life, that player loses that much life instead.',
"If you've cast another white spell this turn, you may cast this spell without paying its mana cost.",
'This creature can not block',
"This spell can't be countered.",
'Undying',
'Flying',
"When this creature dies, return it to the battlefield tapped under its owner's control.",
'Up to two target creatures each get +2/+0 until end of turn.',
'Up to two target creatures each get +1/+0 and gain first strike until end of turn.',
'Vigilance, protection from creatures',
'When Exiled Boggart dies, discard a card.',
'Flash\nFlying\nWhen Kyodai, Soul of Kamigawa enters the battlefield, another target permanent gains indestructible for as long as you control Kyodai.\n{W}{U}{B}{R}{G}: Kyodai gets +5/+5 until end of turn.',
'When an opponent casts a creature spell, if Opal Archangel is an enchantment, Opal Archangel becomes a 5/5 Angel creature with flying and vigilance.',
'When enchanted creature dies, return that card to the battlefield under your control with a +1/+1 counter on it.',
'Tap target land and gain 40 life.',
'All Slivers have SUB_TEXT_0.',
'At the beginning of your upkeep, this permanent deals 1 damage to you.',
):
    print(expr)

    tree = parser.parse(expr)
    if isinstance(tree, Tree):
        print(tree.pretty())
    else:
        print(tree)

    result = transformer.transform(tree)
    print(result)

    print('')

pass
