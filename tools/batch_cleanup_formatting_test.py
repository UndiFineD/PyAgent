import json
import os
import sys

def fix_file(file_path, errors):
    try:
        if not os.path.isabs(file_path):
            # Try to resolve relative to cwd
            file_path = os.path.abspath(file_path)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False

    # Sort errors by line number descending
    unique_errors = {}
    for err in errors:
        # err format: "File:Line:Col: Code Msg"
        # Example: C:\DEV\PyAgent\src\maintenance\evolution\code_improver.py:48:51: E261 at least two spaces before inline comment
        parts = err.split(':')
        if len(parts) < 4:
            continue
        try:
            # parts[0] is drive letter? C
            # parts[1] is path...
            # This splitting is fragile on Windows absolute paths.
            # "C:\DEV\..." -> ['C', '\DEV\...', 'Line', 'Col', ' Code Msg']
            # Better strategy: rsplit from right?
            # Or assume standard flake8 output format: path:line:col: code msg
            
            # Find the last 3 colons
            # path:line:col: msg
            
            last_colon = err.rfind(':') # Separates code from msg usually? No. E261 msg
            # Actually standard output is: path:line:col: code msg
            # code msg contains spaces.
            # Let's find the COLON that separates line/col.
            
            # Heuristic: extract numbers.
            p = err.split(':')
            # Look for the sequence where p[i] is int, p[i+1] is int.
            # On windows: C, \path\to\file, line, col, msg
            # index 0: C
            # index 1: \path...
            # index 2: line? No. path could have :? (streams?)
            
            # Simple approach: parsing from right.
            # code_msg = p[-1]
            # col = p[-2]
            # line = p[-3]
            # path = ":".join(p[:-3])
            
            msg_part = p[-1]
            col_str = p[-2]
            line_str = p[-3]
            code = msg_part.strip().split(' ')[0]
            
            line_no = int(line_str)
            col_no = int(col_str)
            msg = msg_part
            
        except (ValueError, IndexError):
            # Try index +1 shift if msg contains colon?
            # E.g. "E302: expected..." (rare)
            continue
            
        key = (line_no, code)
        # Keep msg for logic
        unique_errors[key] = (line_no, col_no, code, msg)

    sorted_errors = sorted(unique_errors.values(), key=lambda x: x[0], reverse=True)
    
    modified = False
    
    for line_no, col_no, code, msg in sorted_errors:
        idx = line_no - 1
        if idx < 0 or idx >= len(lines):
            continue
            
        current_line = lines[idx]
        
        if code == 'E302': # expected 2 blank lines found X
            count = 1
            if 'found 0' in msg:
                count = 2
            # Insert before
            lines.insert(idx, '\n' * count)
            modified = True
            
        elif code == 'E305': # expected 2 blank lines after class/fn
            count = 1
            if 'found 0' in msg:
                count = 2
            lines.insert(idx, '\n' * count)
            modified = True
            
        elif code == 'E301': # expected 1 blank line found 0
            lines.insert(idx, '\n')
            modified = True
            
        elif code == 'E261': # at least two spaces before inline comment
            # col_no is 1-based index of '#'
            char_idx = col_no - 1
            if char_idx < len(current_line) and current_line[char_idx] == '#':
                # Check char before
                if char_idx > 0:
                    if current_line[char_idx-1] != ' ':
                        # No space. Add 2.
                        lines[idx] = current_line[:char_idx] + '  ' + current_line[char_idx:]
                        modified = True
                    elif char_idx > 1 and current_line[char_idx-2] != ' ':
                        # Only 1 space. Add 1.
                        # Insert at char_idx (before #)
                        lines[idx] = current_line[:char_idx] + ' ' + current_line[char_idx:]
                        modified = True
        
        elif code == 'E303': # too many blank lines
            # Report is usually on the line AFTER the blanks.
            # We want to reduce preceding blank lines to 2 (max for PEP8).
            # Look backwards from idx-1
            cursor = idx - 1
            blank_indices = []
            while cursor >= 0 and not lines[cursor].strip():
                blank_indices.append(cursor)
                cursor -= 1
            
            # If we found blanks
            if len(blank_indices) > 2:
                # We have more than 2 blank lines.
                # Remove the excess.
                # Indices sort descending e.g. [10, 9, 8].
                # We want to keep 2.
                # So remove from 0 to len-2.
                # E.g. 3 blanks: [10, 9, 8]. Remove [10]. Keep 9, 8.
                # Actually, typically we want 2 blank lines for top-level, 1 for methods.
                # Safe bet: reduce to 2 if > 2.
                
                # Careful: modifying list while iterating or using indices that shift.
                # We are processing errors sorted by line number descending.
                # But here we are modifying lines *before* the current line.
                # This might affect indices of *other* errors if they are further down?
                # No, other errors are further UP (since we sort descending).
                # Wait. We sort errors by line_no DESC.
                # So we process line 100 before line 50.
                # If we delete lines 98, 99... line 50 is unaffected.
                # BUT line 100+ would be affected. But we already processed them?
                # Yes.
                # So deleting preceding lines is safe for *future* iterations (which are lower line numbers).
                
                # Remove lines.
                lines_to_remove = len(blank_indices) - 2
                if lines_to_remove > 0:
                    # Remove the *first* ones encountered in loop (closest to current line)?
                    # Or the *last* ones (furthest)?
                    # Doesn't matter, they are all blank.
                    # Remove from blank_indices[0]...
                    for i in range(lines_to_remove):
                        del lines[blank_indices[i]]
                    modified = True

        elif code == 'E265': # block comment should start with '# '
            # col_no points to '#'
            char_idx = col_no - 1
            if char_idx < len(current_line) and current_line[char_idx] == '#':
                # Check next char
                if char_idx + 1 < len(current_line) and current_line[char_idx+1] != ' ' and current_line[char_idx+1] != '!':
                    # Insert space
                    lines[idx] = current_line[:char_idx+1] + ' ' + current_line[char_idx+1:]
                    modified = True

        elif code == 'W291': # trailing whitespace
            lines[idx] = current_line.rstrip() + '\n'
            modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    return False

def main():
    json_path = r'temp/lint_results.json'
    if not os.path.exists(json_path):
        print("No lint results found.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    remaining_data = []
    
    for entry in data:
        file_path = entry['file']
        flake8_out = entry.get('flake8', {})
        stdout = flake8_out.get('stdout', '')
        
        if not stdout:
            continue
            
        errors = stdout.split('\n')
        errors = [e.strip() for e in errors if e.strip()]
        
        target_codes = ['E302', 'E305', 'E301', 'E261', 'W291', 'E303', 'E265']
        
        fixable = [e for e in errors if any(c in e for c in target_codes)]
        others = [e for e in errors if not any(c in e for c in target_codes)]
        
        if fixable:
            print(f"Fixing {len(fixable)} errors in {file_path}...")
            if fix_file(file_path, fixable):
                if not others:
                    # All fixed, do not add to remaining_data
                    continue
                else:
                    # Update stdout with remaining errors only
                    entry['flake8']['stdout'] = '\n'.join(others)
            else:
                # Failed to fix, keep original
                pass
        
        remaining_data.append(entry)

    with open(json_path, 'w') as f:
        json.dump(remaining_data, f, indent=2)

if __name__ == '__main__':
    main()
