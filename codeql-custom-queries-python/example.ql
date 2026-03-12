/**
 * Detect usage of eval() or subprocess.run with shell=True.
 * @name Unsafe execution patterns
 * @kind problem
 * @problem.severity warning
 * @id python/unsafe-exec
 */

import python

// flag calls to builtin eval
from Call c
where c.getTarget().getName() = "eval"
select c, "use of eval() should be avoided"

// flag subprocess.run(..., shell=True)
from Call c, NamedArgument na
where c.getTarget().getQualifiedName() = "subprocess.run" and
      na.getCall() = c and
      na.getName() = "shell" and
      na.getValue() instanceof Literal and
      na.getValue().(Literal).getValue() = "True"
select c, "subprocess.run with shell=True is unsafe"
