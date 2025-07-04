import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark'), encoding='utf-8') as f:
#     grammar = f.read()
grammar = r'''
%import common (DIGIT, WS_INLINE)
%ignore WS_INLINE

%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z,_PLURAL,_POSSESSIVE)
%import primitives (WHOLE,ZERO,COMMA,PLUS,HYPHEN,SELF,COLON,PERIOD,DOT,BAR,PT)
%import words (QUANTITY,COUNT,MORE,THAN,TOP,BOTTOM)
%import words (ZONE)
%import words (THE,TO,AND,OR,AND_OR,NOT)
%import words (ARE,ARENT,CAN,CANT,COULD,COULDNT,DID,DIDNT,DOES,DOESNT,DO,DONT,HAD,HADNT,HAVE,HAVENT,HAS,HASNT,IS,ISNT,WAS,WASNT,WERE,WERENT,OPTIONAL)
%import words (AT,ON,UNTIL,TRIGGER,THEN)
%import words (A,AN,ANOTHER,ANY,EACH,ONLY,OTHER,THAT,THOSE,YOU,YOURE,YOUVE,YOUR,THEY,THEYRE,THEYVE,THERE,THEIR,NAMED)
%import words (CONTROL,CARD,SPELL,TOKEN,ABILITYW,TARGET,PLAYER,COMMANDER)
%import words (FROM,OF)
%import words (ATTACK,CHOOSE,PAY,PUT,TAP,UNTAP,DRAW,IN)
%import words (TAPPED,UNTAPPED)
%import words (LIFE,GAME,WIN,LOSE,COST)
%import types (CARD_TYPE,SUBTYPE_ARTIFACT,SUBTYPE_ENCHANTMENT,SUBTYPE_BASICLAND,SUBTYPE_LAND,SUBTYPE_PLANESWALKER,SUBTYPE_SPELL,SUBTYPE_CREATURE,SUBTYPE_PLANAR,SUBTYPE_DUNGEON,SUBTYPE_BATTLE,SUBTYPE_ROLE_TOKEN,SUPERTYPE)
%import types (COLOR,ENERGY_COST,TAP_COST,UNTAP_COST,MANA_COST,INVERT_TYPE,PW_COST)
%import types (cost,subtype,card_type)
%import abilities.ABILITY
%import counters.MARKER
%import keywords.KEYWORD


start: (ABILITY|MARKER|KEYWORD|WHOLE|ZERO|COMMA|PLUS|HYPHEN|SELF|COLON|PERIOD|DOT|BAR|PT|QUANTITY|COUNT|MORE|THAN|TOP|BOTTOM|ZONE|THE|TO|AND|OR|AND_OR|NOT|ARE|ARENT|CAN|CANT|COULD|COULDNT|DID|DIDNT|DOES|DOESNT|DO|DONT|HAD|HADNT|HAVE|HAVENT|HAS|HASNT|IS|ISNT|WAS|WASNT|WERE|WERENT|OPTIONAL|AT|ON|UNTIL|TRIGGER|THEN|A|AN|ANOTHER|ANY|EACH|ONLY|OTHER|THAT|THOSE|YOU|YOURE|YOUVE|YOUR|THEY|THEYRE|THEYVE|THERE|THEIR|NAMED|CONTROL|CARD|SPELL|TOKEN|ABILITYW|TARGET|PLAYER|COMMANDER|FROM|OF|ATTACK|CHOOSE|PAY|PUT|TAP|UNTAP|DRAW|IN|TAPPED|UNTAPPED|LIFE|GAME|WIN|LOSE|COST|CARD_TYPE|SUBTYPE_ARTIFACT|SUBTYPE_ENCHANTMENT|SUBTYPE_BASICLAND|SUBTYPE_LAND|SUBTYPE_PLANESWALKER|SUBTYPE_SPELL|SUBTYPE_CREATURE|SUBTYPE_PLANAR|SUBTYPE_DUNGEON|SUBTYPE_BATTLE|SUBTYPE_ROLE_TOKEN|SUPERTYPE|COLOR|ENERGY_COST|TAP_COST|UNTAP_COST|MANA_COST|INVERT_TYPE|PW_COST)*

// start: card_type* | (COMMA? cost)* COLON | KEYWORD | ABILITY | MARKER
'''

class Autobot(Transformer):
    pass

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)
transformer = Autobot()

# test it:
for expr in (
'Legendary blue enchantment',
'blue',
'+1:',
'+X:',
'-12:',
'-X:',
'−12:',
'[−12]:',
'0:',
'[0]:',
'Flying',
'Counter',
'Poison counters',
'+1/+1 counters',
'Enchant artifact, creature, or planeswalker',
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
