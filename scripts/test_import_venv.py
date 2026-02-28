import sys
import traceback

def main() -> None:
    print('python:', sys.executable)
    try:
        import rust_core
        print('rust_core import OK', getattr(rust_core, '__version__', 'no-version'))
        print('members:', [m for m in dir(rust_core) if not m.startswith('_')][:50])
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    print('done')


if __name__ == '__main__':
    main()
