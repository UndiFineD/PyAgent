import numpy, pkgutil, importlib

print("version", numpy.__version__)
print("path", numpy.random.__path__)
print(list(pkgutil.iter_modules(numpy.random.__path__)))

try:
    importlib.import_module('numpy.random._generator')
    print('import succeeded')
except Exception as e:
    print('import failed', e)
