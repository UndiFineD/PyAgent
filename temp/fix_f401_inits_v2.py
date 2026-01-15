import ast
import os




def fix_init_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    new_lines = []
    modified = False
    for line in lines:
        stripped = line.strip()
        # Look for: from .Something import Name
        # Must be single import, no alias, no star, no multiple names
        if (stripped.startswith('from .') or stripped.startswith('from src.')) and ' import ' in stripped and ' as ' not in stripped and ',' not in stripped and '*' not in stripped:
            parts = stripped.split(' import ')
            if len(parts) == 2:
                module_part = parts[0]
                name = parts[1].strip()
                if ' ' not in name and name.isidentifier():  # Single valid identifier
                    indent = line[:line.find('from')]
                    # Preserve trailing comments if any
                    comment = ""
                    if '#' in name:
                        # This shouldn't happen with stripped and no space, but let's be safe
                        pass

                    # Ensure we don't double-alias if the name is already an alias in a complex line (though we checked ' as ')










                    new_line = f"{indent}{module_part} import {name} as {name}\n"
                    new_lines.append(new_line)
                    modified = True
                    continue




        new_lines.append(line)

    if modified:
        content = "".join(new_lines)
        try:


            ast.parse(content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True



        except Exception as e:
            print(f"Failed validation for {filepath}: {e}")
            return False
    return False





if __name__ == "__main__":
    count = 0
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file == '__init__.py':
                if fix_init_file(os.path.join(root, file)):
                    count += 1
    print(f"Total __init__.py files fixed: {count}")
