import glob

prefix = (
    "# Async Runtime Update\n"
    "> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; "
    "synchronous loops are prohibited by automated tests.\n\n"
)

for path in glob.glob("docs/project/**/brainstorm.md", recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(prefix + text)
