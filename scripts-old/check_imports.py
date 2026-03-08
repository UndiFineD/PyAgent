import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

try:
    from src.core.base.lifecycle import base_agent
    print('base_agent imported successfully')
except Exception as e:
    print('import error', type(e), e)
