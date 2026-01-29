'''Utility script to locate triple-quote occurrences in a file.

This script is used during linting to detect unmatched triple-quote
occurrences (""") and report their positions and line numbers.
'''

from pathlib import Path
from typing import List


def find_triple_indices(path: str, encoding: str = "utf-8") -> List[int]:
    """Return a list of start indices of all triple-quote occurrences."""
    p = Path(path).read_text(encoding=encoding)
    indices: List[int] = []
    i = 0
    while True:
        idx = p.find('"""', i)
        if idx == -1:
            break
        indices.append(idx)
        i = idx + 3
    return indices


def main() -> None:
    """Run the triple-quote index finder and print results."""
    path = 'src/core/base/logic/structures/bloom_filter.py'
    indices = find_triple_indices(path)

    print('Found', len(indices), 'occurrences')
    p = Path(path).read_text(encoding='utf-8')
    for i, idx in enumerate(indices):
        line_no = p.count('\n', 0, idx) + 1
        print(i, 'pos', idx, 'line', line_no)

    if len(indices) % 2 != 0:
        print('Odd number of triple quotes, last one may be unmatched')
        last_idx = indices[-1]
        print('Last at line', p.count('\n', 0, last_idx) + 1)
    else:
        print('Even number of triple quotes, all likely matched')


if __name__ == '__main__':
    main()
