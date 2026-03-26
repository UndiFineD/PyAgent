/**
 * Detect usage of eval() or subprocess.run with shell=True.
 * @name Unsafe execution patterns
 * @kind problem
 * @problem.severity warning
 * @id python/unsafe-exec
 */

import python

from Call c, string msg
where
  // flag calls to builtin eval
  (c.getFunc().(Name).getId() = "eval" and msg = "use of eval() should be avoided")
  or
  // flag subprocess.run(..., shell=True)
  (
    c.getFunc().(Attribute).getName() = "run" and
    exists(int i | c.getKeyword(i).getKey() = "shell") and
    msg = "subprocess.run with shell argument should be reviewed"
  )
select c, msg
