# Pygic the Conjuring

Yet Another Magic Engine in Python

## Why

This is something that I've wanted to accomplish for years now. Partially I wanted to really dig into creating grammars and figuring out how they work. Previously I've always used raw string handling / processing with regular expressions to write compilers and this time I want to figure out how to do it properly.

I also can't seem to find a good project where anyone's written a full grammar for Magic. There's a few repos out there that have a subset of it, but honestly I don't like what I've seen so far.

I want to make it as easy as possible to generate a JSON file for each card with it's information and the rules "engine" code so I don't have to hand-code ~35k cards.

Eventually I'll be tacking on an actual engine after getting everything to parse properly.

Also, it'd be cool to use the compiled MTG code to find combos or interactions. Who knows?

\- Lastly, it's just cool.

## Current metrics

- Some lines were not pre-processing properly

- e / motion / set / unlock / size / crime / megamorph / d20 / paired / upkeep / gifts / true / ability capitalization / Party! / daynight / tied / locks
  - Lines able to tokenize 28946 / 30209 : 95.82%
  - Recognized tokens 3535 / 4356 : 81.15%

#### Log

- Added level handling
  - Lines able to tokenize 28537 / 30209 : 94.47%
  - Recognized tokens 3476 / 4325 : 80.37%

- Tackled left/right/legends/band (mainly getting rogue quotes)
  - Lines able to tokenize 28404 / 30209 : 94.02%
  - Recognized tokens 3450 / 4302 : 80.20%

- Added `King Darien XLVIII` specific name rip
  - Lines able to tokenize 28369 / 30209 : 93.91%
  - Recognized tokens 3433 / 4301 : 79.82%

- `Planeswalk` and `Phyrexian` have been included with rules; they accounted for ~150 line mismatches.
  - Lines able to tokenize 28367 / 30209 : 93.90%
  - Recognized tokens 3433 / 4303 : 79.78%

- Initial tracking
  - Tokenizing 93.3% of all oracle text lines
  - Recognizing 79.1% of all tokens

## Scripts and doing things

### First scripts to run:

1. `pip install -r requirements.txt`
1. `python pull-magic-rules.py`
1. `python pull-scryfall-oracle.py`
1. `python extract-cards-per-set.py`
1. `python convert-json-to-bin.py`
1. `python generate-oracle-texts.py`

This will pull all data down necessary to run anything in this repo.

Additionally, it will convert the json representation to python dataclass objects, and output to a pickled file for faster loading.

Lastly, it generates a file with all of the unique lines of text found in the oracle. Some of these may not make sense on their own, as multiple cards have multiple lines of text.

### Need to update new abilities or keywords?

* `python extract-abilities.py`
* `python extract-keywords.py`

Note that the ouput of these are put into `data/out` and should be reviewed to combine with the grammar in `grammar`

### Want to find the funky card names with abilities or keywords?

* `python extract-card-name-abkws.py`

This is useful when parsing oracle text, as we can use these "bad card names" to ignore when replacing the card name reference with `~`.

It'll also print out a string you can use in scryfall if you want to look at them!

### Analyzing tokens

The current method to figuring out a cohesive grammar for MTG is to analyze the tokens, and group them based on what we think they go with.

To get started, run:

* `python analyze-token-recognition.py`

NOTE: the grammar takes a while to load.

The idea behind this is just to figure out what tokens we need to be able to tokenize each line of oracle text properly.

Once we've hit ~95% of tokens I'd be pretty comfortable starting to craft an actual grammar from these tokens

### Important grammar files

Most of the important stuff we directly edit is in `words.lark`

## Directory explain

- `data`
  - `bin` - pickle jar for scryfall cards
  - `json` - output for card renders (eventually)
  - `lib` - downloaded files end up here
  - `out` - output from scripts end up here
- `grammar`
  - `clause.[lark|py]` - used for testing clause's [TODO: Move]
  - `preprocess.[lark|py]` - strips out sub-text clauses (usually under quotes)
  - `*.lark` - main grammar files
- `models`
  - `scryfall.py` - scryfall api objects
- `testing` - will eventually be removing this; scraps of testing code go here
- `util` - I'd love to use `utils`, but I'm in love with `ipython` and that conflicts
  - `__init__.py` - current big file of stuff
- `analyze-token-recognition.py` - main file for analyzing tokens
- `convert-json-to-bin.py` - pickles downloaded oracle-cards to python objects
- `extract-abilities.py` - pull out abilities into a grammar
- `extract-card-name-abkws.py` - find card names with abilities / keywords in the name
- `extract-cards-per-set.py` - find what sets cards belong to
- `extract-keywords.py` - pull out keywords into a grammar
- `generate-oracle-texts.py` - generates massive text file for token / grammar processing testing
- `pull-magic-rules.py` - downloads the latest rules of MTG
- `pull-scryfall-oracle.py` - downloads the latest scryfall data

## TO-DOs

- ability / keyword extraction is busted - just need to point to magic rules and skip the first result
- increase token matching
- organize `words.lark` better
    - Most of the tokens are sorted properly, but there's a possibility they need to be moved around
- move script stuff into a `scripts` folder
- create a `src` folder to start working on the rules engine
- make the readme better?
