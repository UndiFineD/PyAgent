import pefile
pyd = r'C:\Dev\PyAgent\\.venv3.13\\Lib\\site-packages\\rust_core\\rust_core.cp313-win_amd64.pyd'
pe = pefile.PE(pyd)
imports = []
for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
    imports.append(entry.dll.decode('utf-8'))
print('\n'.join(imports))
