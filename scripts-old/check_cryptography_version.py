import pkg_resources

try:
    print(pkg_resources.get_distribution('cryptography').version)
except Exception:
    print('not installed')
