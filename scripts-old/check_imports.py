import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

try:
    print('base_agent imported successfully')
except Exception as e:
    print('import error', type(e), e)
