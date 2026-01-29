"""Inspect context around the last triple-quote occurrence in a file.

Prints surrounding text and nearby triple-quote locations for debugging parse errors.
"""

from pathlib import Path
from typing import List


def inspect_last_triple(path: str, context_chars: int = 200, encoding: str = 'utf-8') -> None:
    """Print context around the last triple-quote occurrence."""
    p = Path(path).read_text(encoding=encoding)
    idxs: List[int] = []
    i = 0
    while True:
        idx = p.find('"""', i)
        if idx == -1:
            break
        idxs.append(idx)
        i = idx + 3

    if not idxs:
        print('No triple-quote occurrences found')
        return

    last = idxs[-1]
    print('last idx', last)
    print('around last:\n---')
    print(p[last - context_chars : last + context_chars])
    print('\nall three around last two:')
    for i in range(-4, 1):
        j = idxs[-1 + i]
        print(i, j, 'line', p.count('\n', 0, j) + 1)
        print(p[j - 40 : j + 40].replace('\n', '\\n'))


if __name__ == '__main__':
    inspect_last_triple('src/core/base/logic/structures/bloom_filter.py')
