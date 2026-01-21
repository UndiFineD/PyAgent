import os
import re
from pathlib import Path

def to_snake_case(name):
    if "_" in name and name.islower(): return name
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return re.sub("_+", "_", s2).strip("_")

def run_fix():
    root = Path(os.getcwd()).resolve()
    dirs = ["src", "tests", "scripts", "rust_core"]

    # 1. Rename to snake_case
    for d in dirs:
        dp = root / d
        if not dp.exists(): continue
        for p in list(dp.rglob("*.py")):
            if p.name == "__init__.py": continue
            sn = to_snake_case(p.stem) + ".py"
            if p.name != sn:
                target = p.parent / sn
                if not target.exists(): p.rename(target)
                elif p.name.lower() == sn.lower():
                    tmp = p.parent / (p.name + ".tmp")
                    p.rename(tmp)
                    tmp.rename(target)

    # 2. Map
    # Map from (parent_abs_path_str, low_name) -> actual_name
    name_map = {}
    for d in dirs:
        dp = root / d
        if not dp.exists(): continue
        # Add root to map for dirs
        for p in dp.rglob("*"):
            parent = str(p.parent.resolve()).lower()
            name = p.stem if not p.is_dir() else p.name
            if name == "__init__": continue
            low = name.replace("_", "").replace("-", "").lower()
            name_map[(parent, low)] = name

    def resolve(mod_str, current_file):
        parts = mod_str.split(".")
        if mod_str.startswith("."):
            m = re.match(r"^(\.+)", mod_str)
            dots = len(m.group(1))
            rel = parts[dots-1:]
            if rel and rel[0].startswith("."): rel[0] = rel[0].lstrip(".")
            if rel and not rel[0]: rel.pop(0)

            curr = current_file.parent.resolve()
            for _ in range(dots - 1): curr = curr.parent

            res = []
            for p in rel:
                key = (str(curr).lower(), p.replace("_", "").replace("-", "").lower())
                if key in name_map:
                    real = name_map[key]
                    res.append(real)
                    curr = curr / (real if (curr/real).is_dir() else (real + ".py"))
                else: return None
            return "." * dots + ".".join(res)
        else:
            # Try to find which root it belongs to
            curr = None
            res = []
            start_idx = 0
            for i, p in enumerate(parts):
                # Check if it's one of our roots or in current curr
                if curr is None:
                    # Look for root/part
                    low = p.lower()
                    for d in dirs:
                        if d.lower() == low:
                            curr = root / d
                            res.append(d)
                            start_idx = i + 1
                            break
                    if curr: continue
                    else: return mod_str # External

                low = p.replace("_", "").replace("-", "").lower()
                key = (str(curr).lower(), low)
                if key in name_map:
                    real = name_map[key]
                    res.append(real)
                    curr = curr / real
                else:
                    res.extend(parts[i:])
                    break
            return ".".join(res)

    # 3. Fix
    for d in dirs:
        dp = root / d
        if not dp.exists(): continue
        for p in dp.rglob("*.py"):
            try:
                with open(p, "r", encoding="utf-8") as f: content = f.read()
                lines = content.splitlines()
                nl = []
                changed = False
                for line in lines:
                    ln = line
                    m = re.match(r"^(\s*from\s+)([\w\.]+)(\s+import\s+)(.*)$", line)
                    if m:
                        pre, mod, sep, names = m.groups()
                        cmod = resolve(mod, p)
                        # Fix names if they are submodules
                        nlist = []
                        nchanged = False
                        for np in names.split(","):
                            ns = np.strip()
                            ma = re.match(r"^([\w\.]+)(\s+as\s+[\w\.]+)?$", ns)
                            if ma:
                                nname, alias = ma.groups()
                                cfull = resolve(f"{mod}.{nname}", p)
                                if cfull and cfull != f"{mod}.{nname}":
                                    newn = cfull.split(".")[-1]
                                    nlist.append(np.replace(nname, newn))
                                    nchanged = True
                                else: nlist.append(np)
                            else: nlist.append(np)
                        if (cmod and cmod != mod) or nchanged:
                            ln = f"{pre}{cmod}{sep}{','.join(nlist)}"
                            changed = True
                    mi = re.match(r"^(\s*import\s+)([\w\.]+)(\s+as\s+.*)?$", line)
                    if mi:
                        pre, mod, suf = mi.groups()
                        cmod = resolve(mod, p)
                        if cmod and cmod != mod:
                            ln = f"{pre}{cmod}{suf if suf else ''}"
                            changed = True
                    nl.append(ln)

                text = "\n".join(nl) + ("\n" if content.endswith("\n") else "")
                def repl(m):
                    q, s = m.group(1), m.group(2)
                    if not s or len(s) < 3: return m.group(0)
                    is_p = "/" in s or "\\" in s
                    is_m = "." in s and not is_p
                    if not is_p and not is_m: return m.group(0)
                    norm = s.replace("/", ".").replace("\\", ".")
                    is_py = norm.endswith(".py")
                    if is_py: norm = norm[:-3]
                    curr = resolve(norm, p)
                    if not curr and not norm.startswith("src."):
                        res = resolve("src." + norm, p)
                        if res and res.startswith("src."): curr = res[4:]
                    if curr and (curr != norm or is_py):
                        f = curr.replace(".", "/" if "/" in s else "\\")
                        if is_py: f += ".py"
                        return f"{q}{f}{q}"
                    return m.group(0)
                final = re.sub(r"(['\"])([a-zA-Z0-9_\- \./\\]+)\1", repl, text)
                if final != content:
                    with open(p, "w", encoding="utf-8") as f: f.write(final)
                    print(f"Updated: {p.relative_to(root)}")
            except: continue

if __name__ == "__main__":
    run_fix()
