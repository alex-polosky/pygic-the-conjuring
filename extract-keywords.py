import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

kw_search = r'702\.\d+\. (.*)'

# TODO: implement checking existing keyword defs to warn about new defs that we've found?

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, 'data', 'lib', 'keywords.txt'), encoding='utf-8') as f:
        text = f.read()

    with open(os.path.join(BASE_DIR, 'data', 'out', 'oracle-text.txt'), encoding='utf-8') as f:
        oracle = f.read()

    keywords = re.findall(kw_search, text)

    oracle_search = fr"\b({'|'.join(keywords)})(\w*)\b"

    kw_exts = set(re.findall(oracle_search, oracle, re.IGNORECASE))

    # found_exts = set([(kw[0].upper() + kw[1:], ext) for kw, ext in kw_exts if ext and kw[0].upper() + kw[1:] + ext not in keywords])
    found_exts = {}
    for kw, ext in kw_exts:
        kw = kw[0].upper() + kw[1:]
        full = kw + ext

        if not ext:
            continue

        if full in keywords:
            continue

        if full in (
            'Infection',
            'Devourer',
            'Fearless',
            'Unearthly',
            'Fears',
            'Enchantments',
            'Equipment',
            'Scavengers',
            'Storms',
            'Ascendant',
            'Enchantment',
        ):
            continue

        if kw not in found_exts:
            found_exts[kw] = set()
        found_exts[kw].add(ext)

    with open(os.path.join(BASE_DIR, 'data', 'out', 'keywords.lark'), 'w', encoding='utf-8') as f:
        f.write('%import primitives (_A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_X,_Y,_Z)\n\n')
        f.write('KEYWORDS: ')
        first_line = True
        for keyword in keywords:
            if not first_line:
                f.write('    | ')

            f.write(f'_{keyword[0]}"{keyword[1:]}"')

            if keyword in found_exts:
                for ext in found_exts[keyword]:
                    f.write(f' | _{keyword[0]}"{keyword[1:]}{ext}"')

            f.write('\n')

            if first_line:
                first_line = False
