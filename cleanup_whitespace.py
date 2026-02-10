import sys

def cleanup_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Remove trailing whitespace and handle blank lines with whitespace
        new_lines.append(line.rstrip() + '\n')
    
    # Ensure there's exactly one newline at the end of the file
    content = "".join(new_lines).rstrip() + '\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    cleanup_file(sys.argv[1])
