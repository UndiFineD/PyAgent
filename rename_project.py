import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace("DebVisor", "PyAgent").replace("debvisor", "pyagent")
        
        if content != new_content:
            print(f"Updating {filepath}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception as e:
        print(f"Skipping {filepath}: {e}")

def main():
    start_dirs = ["src", "tests", "docs"]
    for d in start_dirs:
        if os.path.exists(d):
            for root, _, files in os.walk(d):
                for file in files:
                    if file.endswith((".py", ".md", ".txt", ".json")):
                        replace_in_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
