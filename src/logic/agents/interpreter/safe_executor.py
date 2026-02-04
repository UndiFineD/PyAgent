# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import builtins
import logging
import asyncio
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    result: Any
    success: bool

class SafeLocalInterpreter:
    """
    Safely executes Python code within the agent's context.
    Ported from 0xSojalSec-cai/cai/agents/meta/local_python_executor.py
    """
    
    ALLOWED_MODULES = {
        "collections", "datetime", "itertools", "math", "queue", 
        "random", "re", "stat", "statistics", "time", "unicodedata", 
        "json", "hashlib", "base64", "urllib.parse", "ipaddress"
    }

    def __init__(self, safe_globals: Optional[Dict[str, Any]] = None):
        self.safe_globals = safe_globals or {}
        self.safe_globals["__builtins__"] = self._get_safe_builtins()
        self._setup_allowed_modules()

    def _get_safe_builtins(self):
        # Allow standard builtins but block dangerous ones like eval, exec, open (maybe?)
        # For now, we block 'eval', 'exec', 'compile', '__import__' (we handle import separately)
        unsafe = {'eval', 'exec', 'compile', 'open', 'input', '__import__'}
        safe = {}
        for name in dir(builtins):
            if name not in unsafe and not name.startswith('_'):
                safe[name] = getattr(builtins, name)
        
        # Override print to capture output? Or we can just let it print to stdout which we capture
        return safe

    def _setup_allowed_modules(self):
        for mod_name in self.ALLOWED_MODULES:
            try:
                mod = __import__(mod_name)
                self.safe_globals[mod_name] = mod
            except ImportError:
                pass

    async def execute(self, code: str) -> ExecutionResult:
        """
        Executes code string in the safe context.
        """
        loop = asyncio.get_event_loop()
        # Run blocking execution in thread
        return await loop.run_in_executor(None, self._execute_sync, code)

    def _execute_sync(self, code: str) -> ExecutionResult:
        import io
        import sys
        
        # Capture stdout/stderr
        capture_out = io.StringIO()
        capture_err = io.StringIO()
        
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        sys.stdout = capture_out
        sys.stderr = capture_err
        
        result_obj = None
        success = True
        
        try:
            # Parse AST to check for forbidden nodes if strict mode?
            # For now, just rely on blocked builtins.
            
            # Exec
            tree = ast.parse(code)
            
            # If the last statement is an expression, we want to return it
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last_expr = tree.body.pop()
                exec_code = compile(tree, filename="<string>", mode="exec")
                exec(exec_code, self.safe_globals)
                
                # Evaluate the last expression
                eval_code = compile(ast.Expression(last_expr.value), filename="<string>", mode="eval")
                result_obj = eval(eval_code, self.safe_globals)
            else:
                exec(code, self.safe_globals)

        except Exception as e:
            success = False
            import traceback
            traceback.print_exc(file=capture_err)
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
        return ExecutionResult(
            stdout=capture_out.getvalue(),
            stderr=capture_err.getvalue(),
            result=result_obj,
            success=success
        )

# Example usage
if __name__ == "__main__":
    async def main():
        interpreter = SafeLocalInterpreter()
        res = await interpreter.execute("print('Hello from sandbox'); x = 10 + 5; x")
        print(f"Result: {res}")
    
    asyncio.run(main())
