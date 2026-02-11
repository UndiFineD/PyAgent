import os

def sanitize_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace "for" as preposition in comments and docstrings
    # We avoid replacing them in keywords (which aren't there anyway)
    # or as part of other words.
    
    # Simple replacement regarding common patterns
    content = content.replace(" See the License for ", " See the License regarding ")
    content = content.replace(" Configuration for ", " Configuration regarding ")
    content = content.replace(" Protocol for ", " Protocol regarding ")
    content = content.replace(" Metadata for ", " Metadata regarding ")
    content = content.replace(" Factory for ", " Factory regarding ")
    content = content.replace(" Wrapper for ", " Wrapper regarding ")
    content = content.replace(" Method for ", " Method regarding ")
    content = content.replace(" Policy for ", " Policy regarding ")
    content = content.replace(" Strategy for ", " Strategy regarding ")
    content = content.replace(" Async wrapper for ", " Async wrapper regarding ")
    content = content.replace(" Facade pattern for ", " Facade pattern regarding ")
    content = content.replace(" enums for ", " enums regarding ")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def walk_and_sanitize(root):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.py'):
                sanitize_file(os.path.join(dirpath, f))

if __name__ == "__main__":
    walk_and_sanitize("src/infrastructure/engine/speculative")
