import json
import sys

def parse_expr(s: str, idx: int) -> str | int:
    idx = skip_space(s, idx)

    if s[idx] == '(':
        idx += 1
        l = []
        while True:
            idx = skip_space(s, idx)
            if idx >= len(s):
                raise Exception('Unbalanced parenthesis')
            if s[idx] == ')':
                idx += 1
                break

            v, idx = parse_expr(s, idx)
            l.append(v)

        return l, idx

    elif s[idx] == ')':
        raise Exception('Bad parenthesis')
    else:
        start = idx
        while idx < len(s) and (not s[idx].isspace()) and s[idx] not in '()':
            idx += 1
        if idx == start:
            raise Exception('Empty program')
        return parse_atom(s[start:idx]), idx

def skip_space(s: str, idx: int) -> int:
    while idx < len(s) and s[idx].isspace():
        idx += 1
    return idx

def parse_atom(s: str) -> str:
    # TODO: implementation incomplete.
    try:
        return ['val', json.loads(s)]
    except json.JSONDecodeError:
        return s

def tpl_parse(s: str) -> str:
    l, idx = parse_expr(s, 0)
    idx = skip_space(s, idx)
    if idx < len(s):
        raise Exception('Trailing garbage')
    return l

def tpl_eval(node) -> None:
    if len(node) == 0:
        raise ValueError('Empty list')

    if len(node) == 2 and node[0] == 'val':
        return node[1]

    import operator

    bin_ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            'eq': operator.eq,
            'ne': operator.ne,
            'ge': operator.ge,
            'gt': operator.gt,
            'le': operator.le,
            'lt': operator.lt,
            'and': operator.and_,
            'or': operator.or_,
    }

    if len(node) == 3 and node[0] in bin_ops:
        op = bin_ops[node[0]]
        return op(tpl_eval(node[1]), tpl_eval(node[2]))

    una_ops = {
            '-':   operator.neg,
            'not': operator.not_,
    }

    if len(node) == 2 and node[0] in una_ops:
        op = una_ops[node[0]]
        return op(tpl_eval(node[1]))

    if len(node) == 4 and node[0] == '?':
        _, cond, yes, no = node

        if tpl_eval(cond):
            return tpl_eval(yes)
        else:
            return tpl_eval(no)

    if node[0] == 'print':
        # We `return` so that ValueError is not triggered.
        # `*` unpacks
        return print(*(tpl_eval(val) for val in node[1:]))

    raise ValueError('Unknown expression')
