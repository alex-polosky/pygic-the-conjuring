import random

LINE_LIMIT = 500

with open('all-cards.txt') as f:
    text = f.read()
data = text.split('\n')

random.shuffle(data)
with open('all-cards.txt', 'w') as f:
    f.write('\n'.join(data))
with open('some-cards.txt', 'w') as f:
    f.write('\n'.join(data[:LINE_LIMIT]))

