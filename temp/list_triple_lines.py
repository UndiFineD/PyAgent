'''List lines which are exactly a triple-quote on their own.'''

from pathlib import Path
from typing import List


def list_triple_lines(path: str, encoding: str = 'utf-8') -> List[int]:
    '''Return line numbers where a line equals exactly '"""'.'''
    p = Path(path).read_text(encoding=encoding)
    result: List[int] = []
    for i, line in enumerate(p.splitlines(), 1):
        if line.strip() == '"""':
            result.append(i)
    return result


if __name__ == '__main__':
    lines = list_triple_lines('src/core/base/logic/structures/bloom_filter.py')
    for ln in lines:
        print(ln, '"""')
