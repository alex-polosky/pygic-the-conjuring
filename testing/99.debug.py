import os
from lark import Lark, Tree, Transformer, UnexpectedCharacters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

grammar = r'''
%import common (DIGIT, WS_INLINE)
%ignore WS_INLINE

_A: "A" | "a"
_B: "B" | "b"
_C: "C" | "c"
_D: "D" | "d"
_E: "E" | "e"
_F: "F" | "f"
_G: "G" | "g"
_H: "H" | "h"
_I: "I" | "i"
_J: "J" | "j"
_K: "K" | "k"
_L: "L" | "l"
_M: "M" | "m"
_N: "N" | "n"
_O: "O" | "o"
_P: "P" | "p"
_Q: "Q" | "q"
_R: "R" | "r"
_S: "S" | "s"
_T: "T" | "t"
_U: "U" | "u"
_V: "V" | "v"
_W: "W" | "w"
_X: "X" | "x"
_Y: "Y" | "y"
_Z: "Z" | "z"

_PLURAL: "s"
_POSSESSIVE: "'s"

WHOLE: ("1".."9")
ZERO: "0"

COMMA       : ","
PLUS        : "+"
HYPHEN.8    : "—" | "-" | "−"
SELF        : "~" _POSSESSIVE?
COLON       : ":"
SEMICOLON   : ";"
PERIOD      : "."
DOT         : "•"
BAR         : "|"
PT          : "/"

_SUBTYPE_LAND: "Desert"
SUBTYPE_LAND.9: _SUBTYPE_LAND _PLURAL?

ENERGY_COST: "{E}"
TAP_COST   : "{T}"
UNTAP_COST : "{Q}"

MANA_COST: "{C}"
    | "{W}"
    | "{U}"
    | "{B}"
    | "{R}"
    | "{G}"
    | "{H}"
    | "{S}"
    | "{X}"
    | "{Y}"
    | "{Z}"
    | "{P}"
    | /\{\d{1,3}\}/
    | "{W/U}"
    | "{W/B}"
    | "{U/B}"
    | "{U/R}"
    | "{B/R}"
    | "{B/G}"
    | "{R/G}"
    | "{R/W}"
    | "{G/W}"
    | "{G/U}"
    | "{C/W}"
    | "{C/U}"
    | "{C/B}"
    | "{C/R}"
    | "{C/G}"
    | "{2/W}"
    | "{2/U}"
    | "{2/B}"
    | "{2/R}"
    | "{2/G}"
    | "{W/P}"
    | "{U/P}"
    | "{B/P}"
    | "{R/P}"
    | "{G/P}"
    | "{W/U/P}"
    | "{W/B/P}"
    | "{U/B/P}"
    | "{U/R/P}"
    | "{B/R/P}"
    | "{B/G/P}"
    | "{R/G/P}"
    | "{R/W/P}"
    | "{G/W/P}"
    | "{G/U/P}"
    | "{CHAOS}"

INVERT_TYPE.9: (_N"on" | _N"on-")

_CARD_TYPE: _A"rtifact"
    | _B"attle"
    | _C"onspiracy"
    | _C"reature"
    | _D"ungeon"
    | _E"nchantment"
    | _I"nstant"
    | _K"indred"
    | _L"and"
    | _P"henomenon"
    | _P"lane"
    | _P"laneswalker"
    | _S"cheme"
    | _S"orcery"
    | _V"anguard"
CARD_TYPE.8: _CARD_TYPE (_PLURAL| _POSSESSIVE)?

IMPLICIT: /(\w| |-)+/ "—"

ABILITY.7: _A"ctivate" | _A"ctivated" | _A"ctivates"
    | _C"ounter" | _C"ountered"
    | _S"acrifice" | _S"acrificed" | _S"acrifices"

MARKER.9: ("+1/+1"
    | "-1/-1"
    | _A"corn"
    | _A"egis"
    | _A"ge"
    | _W"inch"
    | _W"ind"
    | _W"ish") " counter" _PLURAL?

QUANTITY: _O"ne"
    | _T"wo"

A           : _A
AN          : _A"n"
AS          : _A"s"
PUT         : _P"ut" (_PLURAL | "ing")?
ON          : _O"n"
TARGET      : _T"arget" (_PLURAL | "ed")?
OPPONENT    : _O"pponent" (_PLURAL | _POSSESSIVE)?
CONTROL     : _C"ontrol" _PLURAL?
ONLY        : _O"nly"

start: (WHOLE
    |ZERO
    |COMMA
    |PLUS
    |HYPHEN
    |SELF
    |COLON
    |SEMICOLON
    |PERIOD
    |DOT
    |BAR
    |PT
    |SUBTYPE_LAND
    |ENERGY_COST
    |TAP_COST
    |UNTAP_COST
    |MANA_COST
    |INVERT_TYPE
    |CARD_TYPE
    |IMPLICIT
    |ABILITY
    |MARKER
    |QUANTITY
    |A
    |AN
    |AS
    |PUT
    |ON
    |TARGET
    |OPPONENT
    |CONTROL
    |ONLY)*
'''

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)

for expr in [
'{2}{B}{B}, {T}, Sacrifice a Desert: Put two -1/-1 counters on target creature an opponent controls. Activate only as a sorcery.',
'{2}{B}{B}, {T}, Sacrifice a Desert: Put two -1/-1 on target creature an opponent controls. Activate only as a sorcery.',
]:
    print(expr)

    try:
        tree = parser.parse(expr)
    except UnexpectedCharacters as ex:
        if ex.token_history:
            prior_token = ex.token_history[-1]
        else:
            prior_token = None
        try:
            end_pos = expr.index(' ', ex.pos_in_stream)
        except ValueError:
            end_pos = None
        word = expr[ex.pos_in_stream:end_pos]
        tree = (prior_token, word)

    # if isinstance(tree, Tree):
    #     print(tree.pretty())
    # else:
    #     print(tree)
    print(tree)

    print('')

pass
