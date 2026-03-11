#!/usr/bin/env python3
import pathlib

path=pathlib.Path('src/infrastructure/fleet/mixins/FleetRoutingMixin.py')
lines=path.read_text().splitlines()
for idx in range(20,31):
    l=lines[idx-1]
    print(idx, repr(l))
    print(' chars', [ord(c) for c in l])
