#!/usr/bin/env python3
"""
Simple script to analyze PyAgent improvement todo list structure.
"""

def analyze_todo_structure():
    """Analyze the todo list structure without complex file operations."""
    
    todo_file = r"c:\dev\PyAgent\docs\todo-tree-20260303-1743.txt"
    
    print("Analyzing PyAgent Improvement Todo List Structure")
    print("=" * 55)
    
    # Read the file and count items manually
    try:
        with open(todo_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Count checklist items
        lines = content.split('\n')
        total_items = 0
        completed_items = 0
        
        for line in lines:
            if '[ ]' in line:
                total_items += 1
            elif '[x]' in line:
                total_items += 1
                completed_items += 1
                
        print(f"Total checklist items: {total_items}")
        print(f"Completed items: {completed_items}")
        print(f"Remaining items: {total_items - completed_items}")
        print(f"Completion percentage: {(completed_items/total_items)*100:.1f}%")
        
        # Count files by looking for .improvements.md
        files = []
        for line in lines:
            if '.improvements.md' in line and '│' in line:
                # Simple heuristic to identify file lines
                if '│' in line and '.improvements.md' in line:
                    files.append(line.strip())
                    
        # Try a different approach - count lines with .improvements.md
        file_count = 0
        for line in lines:
            if '.improvements.md' in line and not line.startswith('├─') and not line.startswith('└─'):
                file_count += 1
                
        print(f"\nEstimated total improvement files: {file_count}")
        
    except Exception as e:
        print(f"Error analyzing todo list: {e}")

if __name__ == "__main__":
    analyze_todo_structure()