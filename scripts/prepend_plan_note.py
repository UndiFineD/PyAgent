import glob

prefix = (
    "# Async Runtime Rollout\n"
    "> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.\n"
    "> See 2026-03-10-async-runtime-plan.md for details.\n\n"
)

for path in glob.glob('docs/project/**/plan.md', recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(prefix + text)
