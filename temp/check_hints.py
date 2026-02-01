#!/usr/bin/env python3
import ast

with open('src/core/base/logic/structures/uva_buffer_pool.py', 'r') as f:
    content = f.read()

tree = ast.parse(content)

def check_function(node):
    if isinstance(node, ast.FunctionDef):
        has_return_hint = node.returns is not None
        param_hints = []
        for arg in node.args.args:
            if arg.arg != 'self':
                param_hints.append((arg.arg, arg.annotation is not None))
        
        missing_params = [name for name, has_hint in param_hints if not has_hint]
        
        if not has_return_hint or missing_params:
            print(f'Function {node.name}: return_hint={has_return_hint}, missing_param_hints={missing_params}')

for node in ast.walk(tree):
    check_function(node)