import os
from lark import Lark, Tree, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, f'{os.path.basename(__file__)[:-3]}.lark')) as file:
    grammar = file.read()

class CalcTransformer(Transformer):
    def NUMBER(self, token):
        return float(token)

    def expr(self, args):
        if len(args) == 1:
            return args[0]
        left, op, right = args
        match op:
            case '+':
                return left + right
            case '-':
                return left - right

    def term(self, args):
        if len(args) == 1:
            return args[0]
        left, op, right = args
        match op:
            case '*':
                return left * right
            case '/':
                return left / right

    def power(self, args):
        if len(args) == 1:
            return args[0]
        left, op, right = args
        match op:
            case '^' | '**':
                return left ** right

    def unary(self, args):
        if len(args) == 1:
            return args[0]
        op, right = args
        if op == '-':
            return 0 - right

    def factor(self, args):
        if len(args) == 1:
            return args[0]

    def start(self, args):
        return args[0]

parser = Lark(grammar, parser='lalr', debug=True)
transformer = CalcTransformer()

for expr in (
    '1',
    '9',
    '1 + 2',
    '1+2',
    '(2) + (4)',
    '1 + 2 * 3',
    '(1+2)/3',
    '2 ^ 3',
    '(1 + 1) ^ 3',
    '1 + 1 ^ 3',
    '2 * 1 ^ 3',
    '1 * 2 ^ 3',
    '(1 * 2) ^ 3',
    '-3',
    '-(2 * 3)^3',
    '-(2 * 3)^2',
    '-((2 * 3)^2)',
):
    print(expr)

    tree = parser.parse(expr)
    if isinstance(tree, Tree):
        print(tree.pretty())
    else:
        print(tree)

    result = transformer.transform(tree)
    print(result)

    correct_result = eval(expr.replace('^', '**'))
    print(correct_result)

    print('')

pass
