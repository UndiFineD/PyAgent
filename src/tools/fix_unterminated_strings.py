#!/usr/bin/env python3
"""
Conservative fixer for unterminated/imbalanced string literals.

Usage:
  python tools/fix_unterminated_strings.py --target src [--dry-run] [--apply] [--backup] [--verbose]

This script is intentionally conservative:
- First tries to compile each file.
- On SyntaxError related to unterminated strings, it attempts small, low-risk fixes:
  - Balance unmatched triple-quotes by appending the missing triple-quote at EOF.
  - Try joining a small window of lines (<=5) around the error to balance single/double quotes.
- Always creates a `.bak` copy when `--apply --backup` are used.
"""
import argparse
import os
import sys
import traceback


def compile_source(src: str):
    try:
        compile(src, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        return False, e


def conservative_fix(content: str, err: SyntaxError, verbose: bool = False):
    # 1) Try to fix unmatched triple quotes by appending closing triple if odd count
    fixed = content
    changed = False
    for tq in ('"""', "'''"):
        if fixed.count(tq) % 2 == 1:
            if verbose:
                print(f"Detected odd count of {tq!r}, appending closing {tq!r} at EOF")
            fixed = fixed + '\n' + tq + '\n'
            changed = True
    success, new_err = compile_source(fixed)
    if success:
        return fixed, changed

    # 2) Conservative join-window around error line to try to balance single/double quotes
    lines = content.splitlines(True)
    lineno = getattr(err, 'lineno', None) or 1
    idx = max(0, lineno - 1)
    max_join = 5
    for window in range(1, max_join + 1):
        if idx + window > len(lines):
            break
        chunk = ''.join(lines[idx: idx + window])
        # If chunk has even counts for both quote types, try joining
        if chunk.count('"') % 2 == 0 and chunk.count("'") % 2 == 0:
            continue
        joined = ' '.join(l.rstrip('\n') for l in lines[idx: idx + window]) + '\n'
        new_lines = lines[:idx] + [joined] + lines[idx + window:]
        candidate = ''.join(new_lines)
        success2, err2 = compile_source(candidate)
        if success2:
            if verbose:
                print(f"Balanced quotes by joining lines {idx+1}-{idx+window}")
            return candidate, True

    # If nothing worked, return original and indicate no change
    return content, False


def process_file(path: str, apply: bool, backup: bool, verbose: bool):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if verbose:
            print(f"Could not read {path}: {e}")
        return False, 'read-failed'

    ok, err = compile_source(content)
    if ok:
        if verbose:
            print(f"OK: {path}")
        return False, 'ok'

    # Only attempt fixes for string-related syntax errors
    msg = str(err)
    if 'unterminated string literal' not in msg and 'EOL while scanning string literal' not in msg and 'EOF while scanning triple-quoted string literal' not in msg:
        if verbose:
            print(f"Skipping non-string SyntaxError in {path}: {msg}")
        return False, 'skip-non-string'

    fixed_content, changed = conservative_fix(content, err, verbose=verbose)
    if not changed:
        if verbose:
            print(f"No safe fix found for {path} (SyntaxError: {msg})")
        return False, 'no-fix'

    if apply:
        if backup:
            bak = path + '.bak'
            try:
                with open(bak, 'w', encoding='utf-8') as f:
                    f.write(content)
                if verbose:
                    print(f"Backup written to {bak}")
            except Exception as e:
                print(f"Failed to write backup for {path}: {e}")
                return False, 'bak-fail'
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            if verbose:
                print(f"Patched: {path}")
            return True, 'patched'
        except Exception as e:
            if verbose:
                print(f"Failed to write patched content for {path}: {e}")
            return False, 'write-fail'
    else:
        if verbose:
            print(f"Would patch: {path}")
        return True, 'would-patch'


def walk_and_fix(target_dir: str, apply: bool, backup: bool, verbose: bool):
    stats = {'checked': 0, 'ok': 0, 'would_patch': 0, 'patched': 0, 'skipped': 0, 'errors': 0}
    for root, dirs, files in os.walk(target_dir):
        # skip virtual envs and caches
        if any(p in root for p in ('site-packages', '__pycache__', '.venv', 'venv')):
            continue
        for fname in files:
            if not fname.endswith('.py'):
                continue
            path = os.path.join(root, fname)
            stats['checked'] += 1
            try:
                did_change, reason = process_file(path, apply=apply, backup=backup, verbose=verbose)
                if reason == 'ok':
                    stats['ok'] += 1
                elif reason in ('would-patch', 'no-fix') and did_change:
                    stats['would_patch'] += 1
                elif reason == 'patched' and did_change:
                    stats['patched'] += 1
                elif reason.startswith('skip'):
                    stats['skipped'] += 1
                else:
                    # read-failed, bak-fail, write-fail
                    stats['errors'] += 1
            except Exception:
                stats['errors'] += 1
                if verbose:
                    traceback.print_exc()
    return stats


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--target', default='src')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--backup', action='store_true')
    p.add_argument('--verbose', action='store_true')
    args = p.parse_args()

    if args.dry_run and args.apply:
        print('Use either --dry-run or --apply, not both')
        sys.exit(2)

    apply = args.apply
    backup = args.backup if apply else False
    verbose = args.verbose

    target = args.target
    if not os.path.isdir(target):
        print(f"Target directory not found: {target}")
        sys.exit(2)

    if verbose:
        mode = 'apply' if apply else 'dry-run'
        print(f"Running conservative string fixer on {target} (mode={mode})")

    stats = walk_and_fix(target, apply=apply, backup=backup, verbose=verbose)

    print('Summary:')
    print(f"  Checked: {stats['checked']}")
    print(f"  OK: {stats['ok']}")
    print(f"  Would patch: {stats['would_patch']}")
    print(f"  Patched: {stats['patched']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")


if __name__ == '__main__':
    main()
