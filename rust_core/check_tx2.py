import os, sys, glob, shutil, tempfile, pathlib

sys.path.insert(0, os.path.join(os.getcwd(), 'target', 'debug'))
for path in glob.glob(os.path.join(os.getcwd(), 'target', 'debug', '*.dll')):
    shutil.copyfile(path, path[:-4] + '.pyd')
    sys.path.insert(0, os.getcwd())

import rust_core

# simulate test
base = pathlib.Path(tempfile.mkdtemp())
print('transaction path', base)

rust_core.begin_transaction(str(base))
with open(base / 'foo.txt', 'wb') as f:
    f.write(b'hello')
print('file exists after create?', (base / 'foo.txt').exists())

# simulate error
try:
    raise RuntimeError('oops')
except RuntimeError:
    pass

rust_core.rollback_transaction()
print('file exists after rollback?', (base / 'foo.txt').exists())
