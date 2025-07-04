import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ab_search = r'701\.\d+\. (.*)'

# TODO: implement checking existing keyword defs to warn about new defs that we've found?

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, 'rules', 'abilities.txt'), encoding='utf-8') as f:
        text = f.read()

    with open(os.path.join(BASE_DIR, 'data', 'oracle_only.sorted.txt'), encoding='utf-8') as f:
        oracle = f.read()

    abilities = re.findall(ab_search, text)

    oracle_search = fr"\b({'|'.join(abilities)})(\w*)\b"

    ab_exts = set(re.findall(oracle_search, oracle, re.IGNORECASE))

    # found_exts = set([(ab[0].upper() + ab[1:], ext) for ab, ext in ab_exts if ext and ab[0].upper() + ab[1:] + ext not in abilities])

    found_exts = {}
    for ab, ext in ab_exts:
        ab = ab[0].upper() + ab[1:]
        full = ab + ext

        if not ext:
            continue

        if full in abilities:
            continue

        if full in (
            'Counters',
            'Player',
            'Fighting',
            'Planeswalker',
            'Planeswalkers',
        ):
            continue

        if ab not in found_exts:
            found_exts[ab] = set()
        found_exts[ab].add(ext)

    with open(os.path.join(BASE_DIR, 'testing', 'abilities.lark'), 'w', encoding='utf-8') as f:
        f.write('%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z)\n\n')
        f.write('ABILITY: ')
        first_line = True
        for keyword in abilities:
            if not first_line:
                f.write('    | ')

            f.write(f'_{keyword[0]}"{keyword[1:]}"')

            if keyword in found_exts:
                for ext in found_exts[keyword]:
                    f.write(f' | _{keyword[0]}"{keyword[1:]}{ext}"')

            f.write('\n')

            if first_line:
                first_line = False
