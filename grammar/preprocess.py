import os
from lark import Lark, Token, Tree, Transformer

__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(__BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark')) as file:
    __grammar = file.read()

class Autobot(Transformer):
    def __init__(self, parser: Lark, visit_tokens = True):
        self._parser = parser
        super().__init__(visit_tokens)

    def start(self, args):
        innertexts = []
        subtexts = []
        text = ''
        for arg in args:
            if type(arg) is str:
                text += arg
            else:
                subtextkw = arg[0]
                sub_clause = arg[1][0]
                if type(sub_clause) is str:
                    period = '.' if sub_clause[-1] == '.' else ''
                    subtext = sub_clause
                else:
                    # Inner sub text!
                    # TODO: more stringent testing with inner nested clauses, but so far there's only 1 card with it
                    subtext = sub_clause[0][0]
                    period = '.' if subtext[-1] == '.' else ''
                    innertext_index = 0
                    while 'SUB_TEXT_' in subtext:
                        subtext_index_pos = subtext.index('SUB_TEXT_') + 9
                        subtext_index = subtext[subtext_index_pos]
                        subtext = subtext.replace('SUB_TEXT_' + subtext_index, f'INNER_TEXT_{len(innertexts) + innertext_index}')
                        innertext_index += 1
                    for innertext in sub_clause[1]:
                        innertexts.append(innertext)
                text += f'{subtextkw} SUB_TEXT_{len(subtexts)}{period}'
                subtexts.append(subtext)
        texts = [x.strip() for x in text.split('\n')]
        return [texts, subtexts, innertexts]

    def subtext_expr(self, args):
        return [x for x in args if x]

    def quoted(self, args):
        return [x for x in args if x]

    def dq_content(self, args):
        # As there may be single quotes contained in the subtext, we want to make sure to extract that information
        # The processor isn't smart enough to grab it in the first pass
        if not len(args) == 1:
            return args  # Throw error?
        inner_decepticon = self.transform(self._parser.parse(args[0]))
        return inner_decepticon

    def sq_content(self, args):
        # This should realistically only ever be 1 and a string
        return str(args[0])

    def single_quote(self, args):
        return [x for x in args if x]

    def double_quote(self, args):
        return [x for x in args if x]

    def TEXT(self, token):
        return str(token)

    def SUBTEXTKW(self, token):
        return str(token)

    def D_QUOTE(self, _):
        return None

    def S_QUOTE(self, _):
        return None


Parser = Lark(__grammar, parser='lalr', debug=True)  # TODO: set Debug progmatically
Transformer = Autobot(Parser)


def preprocess(oracle_text):
    tree = Parser.parse(oracle_text)
    result = Transformer.transform(tree)
    if type(result) == str:
        result = [[result], [], []]
    result = tuple([tuple(x) for x in result])
    return result


if __name__ == '__main__':
    # Determine: do we want the PP to handle figuring out SELF-REF?

    results = []

    for expr in (
# "Choose one \u2014\n\u2022 Burn Down the House deals 5 damage to each creature and each planeswalker.\n\u2022 Create 2 2/1 red Goblin creature tokens with \"{T}, Sacrifice this creature: Deal 2 damage to any target.\"\n\u2022 Create three 1/1 red Devil creature tokens with \"When this creature dies, it deals 1 damage to any target.\" They gain haste until end of turn.",
# "Activated abilities of nontoken Rebels cost an additional \"Sacrifice a land\" to activate.",
# "Whenever a nontoken creature enters the battlefield under your control, you may pay {2}. If you do, create a token that's a copy of that creature, except it has haste and \"At the beginning of the end step, sacrifice this permanent.\"",
# "Until end of turn, lands you control gain \"{T}: Add one mana of any color.\"",
# "{1}{W}: Until end of turn, target creature gains \"This creature can't attack or block unless its controller pays {1} for each Cleric on the battlefield.\"",
# "Enchant land\nEnchanted land has \"{T}, Discard a card: Gain control of target creature until end of turn.\"",
# "All Slivers have \"{T}: Target Sliver creature gets +X/+0 until end of turn, where X is the number of Slivers on the battlefield.\"",
# "Prevent all damage that would be dealt to Glittering Lion.\n{3}: Until end of turn, Glittering Lion loses \"Prevent all damage that would be dealt to Glittering Lion.\" Any player may activate this ability.",
# "Choose one \u2014\n\u2022 Burn Down the House deals 5 damage to each creature and each planeswalker.\n\u2022 Create three 1/1 red Devil creature tokens with \"When this creature dies, it deals 1 damage to any target.\" They gain haste until end of turn.",
# 'Whenever Totentanz, Swarm Piper or another nontoken creature you control dies, create a 1/1 black Rat creature token with "This creature can\'t block."',
# 'You get an emblem with "Islands you control have \'{T}: Draw a card.\'"',
# # ---
# '{1}, {T}: Add {W}{U}.',
# '{1}, Sacrifice Darigaaz\'s Attendant: Add {B}{R}{G}.',
# "Flying\nHexavus enters the battlefield with six +1/+1 counters on it.\n{1}, Remove a +1/+1 counter from Hexavus: Put a flying counter on another target creature.\n{1}, Remove a counter from another creature you control: Put a +1/+1 counter on Hexavus.",
# '{2}, {T}: Prevent all damage that would be dealt this turn by a source of your choice that shares a color with the exiled card.',
# '{4}{W}{W}: Creatures you control get +2/+2 and gain first strike and lifelink until end of turn.',
# "At the beginning of your upkeep, Nettletooth Djinn deals 1 damage to you.",
# "Skulk (This creature can't be blocked by creatures with greater power.)\nAt the beginning of your end step, each opponent dealt combat damage this game by a creature named Gollum, Obsessed Stalker loses life equal to the amount of life you gained this turn.",
# 'If an opponent would gain life, that player loses that much life instead.',
# 'If you\'ve cast another white spell this turn, you may cast this spell without paying its mana cost.',
# 'This creature can not block',
# 'This spell can\'t be countered.',
# 'Undying',
# 'Flying',
# 'When this creature dies, return it to the battlefield tapped under its owner\'s control.',
# 'Up to two target creatures each get +2/+0 until end of turn.',
# 'Up to two target creatures each get +1/+0 and gain first strike until end of turn.',
# 'Vigilance, protection from creatures',
# 'When Exiled Boggart dies, discard a card.',
# "Flash\nFlying\nWhen Kyodai, Soul of Kamigawa enters the battlefield, another target permanent gains indestructible for as long as you control Kyodai.\n{W}{U}{B}{R}{G}: Kyodai gets +5/+5 until end of turn.",
# "When an opponent casts a creature spell, if Opal Archangel is an enchantment, Opal Archangel becomes a 5/5 Angel creature with flying and vigilance.",
# 'When enchanted creature dies, return that card to the battlefield under your control with a +1/+1 counter on it.',
# 'Tap target land and gain 40 life.',
# "All Slivers have \"At the beginning of your upkeep, this permanent deals 1 damage to you.\"",
'−10: Create a colorless Equipment artifact token named Stoneforged Blade. It has indestructible, "Equipped creature gets +5/+5 and has double strike," and equip {0}.',
'As long as the top card of your graveyard is a creature card, this creature has the full text of that card and has the text "{2}: Discard a card."',
'The "legend rule" doesn\'t apply.',
    ):
        print(expr)

        tree = Parser.parse(expr)
        if isinstance(tree, Tree):
            print(tree.pretty())
        else:
            print(tree)

        result = Transformer.transform(tree)
        print(result)

        print('')

        results.append(result)

    print('---')
    for r in results:
        if type(r) is str:
            print(repr(r))
            continue
        for x in r:
            for y in x:
                print(repr(y))
