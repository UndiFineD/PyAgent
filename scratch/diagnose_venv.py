import sys
import os
import site

print("Python Executable:", sys.executable)
print("Sys Path:", sys.path)
print("User Site:", site.USER_SITE)
print("Enable User Site:", site.ENABLE_USER_SITE)

try:
    import pip
    print("Pip imported successfully:", pip.__file__)
except ImportError as e:
    print("Failed to import pip:", e)
except Exception as e:
    print("Error importing pip:", e)

# Check writability of site-packages
for path in sys.path:
    if 'site-packages' in path:
        is_writable = os.access(path, os.W_OK)
        print(f"Site-package path: {path} | Writable: {is_writable}")

        # Check for stale locks
        # pip sometimes leaves .lock files
        try:
            files = os.listdir(path)
            for f in files:
                if f.endswith('.lock'):
                    print(f"WARNING: Lock file found: {os.path.join(path, f)}")
        except Exception:
            pass
