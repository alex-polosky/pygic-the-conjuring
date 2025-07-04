import os
from hypothesis import given, strategies as st
from hypothesis.extra.lark import from_lark
from lark import Lark

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load your Lark grammar (EBNF .lark file)
# fn = os.path.join(BASE_DIR, 'grammar', 'clause.lark')
fn = os.path.join(BASE_DIR, 'grammar.lark')
with open(fn) as f:
    Parser = Lark(f.read(), parser='lalr')


@given(from_lark(Parser))
def test_with_random_input(s):
    # s is a randomly-generated text matching your grammar
    tree = Parser.parse(s)
    # …do whatever you like with tree…
    print(s)


@given(from_lark(Parser).filter(str.isascii))
def test_ascii_only(s: str):
    # any s that slips through will be pure ASCII
    with open(os.path.join(BASE_DIR, 'data', '__grammar-gen.txt'), 'w'):
        f.write(s + '\n')

if __name__ == '__main__':
    test_ascii_only()
