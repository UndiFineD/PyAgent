import os
import re

def fix_header(lines):
    shebang = None
    future_annotations = False
    version_import = False
    version_assignment = False
    docstring_start = -1
    docstring_end = -1
    
    # Track which lines to keep in the "middle"
    middle_lines = []
    rest_lines = []
    
    header_done = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if not header_done:
            if line.startswith("#!"):
                shebang = line
                i += 1
                continue
            
            if re.match(r"^from\s+__future__\s+import\s+annotations", line.strip()):
                future_annotations = True
                i += 1
                continue
            
            if re.match(r"^from\s+src\.core\.base\.version\s+import\s+VERSION", line.strip()):
                version_import = True
                i += 1
                continue
            
            if re.match(r"^__version__\s*=\s*VERSION", line.strip()):
                version_assignment = True
                i += 1
                continue
            
            # If we hit something else, it might be a docstring or other imports
            # But we only care about collecting everything until we are past the version assignment
            # Actually, a better way is to identify what we MUST have and where, 
            # and just strip them from their current positions and re-insert them.
        
        i += 1

    # Let's try a different approach:
    # 1. Extract Shebang if present.
    # 2. Extract 'from __future__ import annotations' if present.
    # 3. Extract 'from src.core.base.version import VERSION' if present.
    # 4. Extract '__version__ = VERSION' if present.
    # 5. Keep everything else in its relative order.
    
    new_lines = []
    _shebang = None
    _future = None
    _v_import = None
    _v_assign = None
    
    remaining = []
    
    # First pass to find and remove
    found_future = False
    found_v_import = False
    found_v_assign = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#!") and not _shebang:
            _shebang = line
            continue
        if re.match(r"^from\s+__future__\s+import\s+annotations", stripped):
            _future = line
            found_future = True
            continue
        if re.match(r"^from\s+src\.core\.base\.version\s+import\s+VERSION", stripped):
            _v_import = line
            found_v_import = True
            continue
        if re.match(r"^__version__\s*=\s*VERSION", stripped):
            _v_assign = line
            found_v_assign = True
            continue
        remaining.append(line)

    # Clean up leading blank lines in remaining
    while remaining and not remaining[0].strip():
        remaining.pop(0)
    
    # 2. 'from __future__ import annotations' - MUST BE THE FIRST NON-COMMENT/NON-SHEBANG LINE.
    # If it didn't exist, we should probably add it as per requirement "ensure the header follows this CORRECT order"
    # and "Fix the roughly 150 files".
    if not _future:
        _future = "from __future__ import annotations\n"
    
    if not _v_import:
        _v_import = "from src.core.base.version import VERSION\n"
    
    if not _v_assign:
        _v_assign = "__version__ = VERSION\n"

    # Reconstruct
    if _shebang:
        new_lines.append(_shebang)
    
    new_lines.append(_future)
    
    # Docstring might be at the start of remaining
    # If the user says "Docstring OR OTHER IMPORTS" should be after future annotations
    
    inserted_version = False
    
    # We need to find where to put the version lines.
    # Requirement:
    # 3. Docstring ("""...""") - OR OTHER IMPORTS.
    # 4. 'from src.core.base.version import VERSION'
    # 5. '__version__ = VERSION'
    
    # Wait, if there is a docstring, it usually comes BEFORE imports but AFTER future imports.
    # The requirement says: 3. Docstring OR OTHER IMPORTS. 4. VERSION import. 5. VERSION assign.
    
    # So basically:
    # Shebang
    # Future
    # [Docstring]
    # [Other Imports]
    # Version Import
    # Version Assign
    # [Rest of code]
    
    # Let's find where the "other imports" end or where the code begins.
    # Actually, the requirement is quite specific about the order of 4 and 5 being relative to 2 and 3.
    
    # Let's put 4 and 5 after all other imports if we want to be safe, or just after the docstring.
    # Usually, version is at the top.
    
    # Let's see how many of 'remaining' are docstring/imports.
    
    idx = 0
    # Skip docstring if it's at the beginning
    if idx < len(remaining) and (remaining[idx].strip().startswith('"""') or remaining[idx].strip().startswith("'''")):
        start_quote = remaining[idx].strip()[:3]
        new_lines.append(remaining[idx])
        if remaining[idx].strip().count(start_quote) == 1:
            idx += 1
            while idx < len(remaining) and start_quote not in remaining[idx]:
                new_lines.append(remaining[idx])
                idx += 1
            if idx < len(remaining):
                new_lines.append(remaining[idx])
                idx += 1
        else:
            idx += 1
            
    # Now we might have other imports.
    # The user says 4 and 5 should follow 3 (docstring or other imports).
    # If I put 4 and 5 after EVERYTHING that is an import, it might be too far down.
    # But usually VERSION is defined before other logic.
    
    # Let's just put all imports first, then version.
    while idx < len(remaining) and (remaining[idx].strip().startswith("import ") or remaining[idx].strip().startswith("from ") or not remaining[idx].strip() or remaining[idx].strip().startswith("#")):
        # If it's a blank line or comment, we keep it with imports
        new_lines.append(remaining[idx])
        idx += 1
    
    # Now insert version lines if not already there
    # Check if they are already in new_lines (unlikely if we stripped them)
    new_lines.append("\n")
    new_lines.append(_v_import)
    new_lines.append(_v_assign)
    new_lines.append("\n")
    
    # Add the rest
    while idx < len(remaining):
        new_lines.append(remaining[idx])
        idx += 1
        
    return new_lines

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}")
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                if not lines:
                    continue
                    
                new_lines = fix_header(lines)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

if __name__ == "__main__":
    process_directory(r"c:\DEV\PyAgent\src\observability")
