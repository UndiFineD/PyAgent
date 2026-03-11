import os

for root, dirs, files in os.walk('src'):
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                txt = fh.read()
                if '@py_assert0' in txt:
                    print(path)
        except Exception:
            pass
