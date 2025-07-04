import os
from lark import Lark, Tree

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, '0.calc.lark')) as file:
    grammar = file.read()

parser = Lark(grammar, parser='lalr', debug=True)

for expr in (
    '1',
    '9',
    '1 + 2',
    '1+2',
    '1 + 2 * 3',
    '(1+2)/3'
):
    result = parser.parse(expr)
    if isinstance(result, Tree):
        print(result.pretty())
    else:
        print(result)

pass
