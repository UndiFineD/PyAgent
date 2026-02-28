import os
import sys
import ctypes
from ctypes import WinError

pyd = r'C:\Dev\PyAgent\\.venv3.13\\Lib\\site-packages\\rust_core\\rust_core.cp313-win_amd64.pyd'
print('Python:', sys.executable)
print('Pyd:', pyd)
print('Exists pyd:', os.path.exists(pyd))
print('PATH snippet:', os.environ.get('PATH','')[:400])

# Try LoadLibrary directly
try:
    print('\nAttempting ctypes.WinDLL without extra search paths...')
    ctypes.WinDLL(pyd)
    print('WinDLL load succeeded')
except OSError as e:
    print('WinDLL load OSError:', e)
    try:
        print('WinError code:', e.winerror)
    except Exception:
        pass

# Try adding package dir to DLL search path (Python 3.8+)
try:
    pkg_dir = os.path.dirname(pyd)
    print('\nAdding DLL dir:', pkg_dir)
    add = os.add_dll_directory(pkg_dir)
    try:
        ctypes.WinDLL(pyd)
        print('WinDLL load succeeded after adding dll directory')
    except OSError as e:
        print('WinDLL load OSError after add_dll_directory:', e)
        try:
            print('WinError code:', e.winerror)
        except Exception:
            pass
    finally:
        # remove handle if possible
        try:
            add.close()
        except Exception:
            pass
except Exception as ex:
    print('add_dll_directory not available or failed:', ex)

# Try import normally (to show import error)
print('\nAttempting import rust_core...')
try:
    import importlib
    import rust_core
    print('Imported rust_core OK')
except Exception as e:
    print('Import failed:')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('Done')
