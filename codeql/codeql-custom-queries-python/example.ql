/**
 * Detect usage of eval().
 * @name Unsafe execution patterns
 * @kind problem
 * @problem.severity warning
 * @id python/unsafe-exec
 */

import python

from Call c
where c.getFunc().(Name).getId() = "eval"
select c, "Use of eval() detected — consider a safer alternative."
