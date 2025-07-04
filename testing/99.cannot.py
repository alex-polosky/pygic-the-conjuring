import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark'), encoding='utf-8') as f:
#     grammar = f.read()
grammar = r'''
%import common.WS_INLINE
%ignore WS_INLINE

CAN: "can"
NOT: "not"
CANT: "can't" | CAN NOT | CAN WS_INLINE NOT
// CANT: "can't"
// cant_rule: CANT | CAN NOT

start: (CAN | CANT)*
// start: (CAN | cant_rule)*
'''

class Autobot(Transformer):
    pass

parser = Lark(grammar, import_paths=[BASE_DIR], parser='lalr', debug=True)
transformer = Autobot()

# test it:
for expr, expected in (
('can', ''),
('can\'t', ''),
('cannot', ''),
('can not', ''),
('can can', ''),
('can can can\'t', ''),
('can can can\'t can not', ''),
('can can can\'t can not cannot', ''),
('can can can\'t can not cannot can can\'t', ''),
):
    print(expr)

    tree = parser.parse(expr)
    if isinstance(tree, Tree):
        print(tree.pretty())
    else:
        print(tree)

    result = transformer.transform(tree)
    # print(result)

    # print(result == expected)

    print('')
