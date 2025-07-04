#!/usr/bin/env python3
import sys
import re

def convert_lark_to_ebnf(lark_text):
    lines = lark_text.splitlines()
    ebnf_lines = []
    in_rule = False

    rule_name = None
    rule_buffer = []

    def flush_rule():
        nonlocal rule_buffer, rule_name, in_rule
        if not rule_name:
            return
        # join alternatives, ensure proper formatting
        # add semicolon to last line
        if rule_buffer:
            rule_buffer[-1] = rule_buffer[-1].rstrip() + " ;"
        ebnf_lines.extend(rule_buffer)
        rule_buffer = []
        rule_name = None
        in_rule = False

    for raw in lines:
        line = raw.rstrip()
        # skip Lark-specific directives and blank lines
        if re.match(r'\s*%', line) or not line.strip():
            flush_rule()
            continue

        # rule start: optional '?', name, ':'
        m = re.match(r'\s*\??\s*([a-zA-Z_]\w*)\s*:\s*(.*)', line)
        if m:
            flush_rule()
            name, rhs = m.group(1), m.group(2).strip()
            ebnf_line = f"{name} = {rhs}"
            rule_name = name
            rule_buffer = [ebnf_line]
            in_rule = True
            continue

        # continuation line ('|' alternative)
        if in_rule and re.match(r'\s*\|', line):
            alt = line.lstrip()
            rule_buffer.append(f"    {alt}")
            continue

        # anything else, treat as standalone (e.g. token definitions)
        flush_rule()
        # convert token definitions: NAME : "..." or regex
        m_tok = re.match(r'\s*([A-Z][A-Z0-9_]*)\s*:\s*(.*)', line)
        if m_tok:
            name, pattern = m_tok.group(1), m_tok.group(2).strip()
            ebnf_lines.append(f"{name} = {pattern} ;")
        else:
            # pass through other lines unchanged
            ebnf_lines.append(line)

    flush_rule()
    return "\n".join(ebnf_lines)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <lark_grammar.lark>", file=sys.stderr)
        sys.exit(1)
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        lark_text = f.read()
    ebnf = convert_lark_to_ebnf(lark_text)
    print(ebnf)

if __name__ == "__main__":
    main()
