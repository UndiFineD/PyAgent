"""Script to automatically generate PyO3 module registration code."""
import re
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'src/inference.rs'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all functions marked with #[pyfunction]
# Allow intermediate attributes
funcs = re.findall(r'#\[pyfunction\].*?pub fn ([a-z0-9_]+)', content, re.DOTALL)

# Find all classes marked with #[pyclass]
classes = re.findall(r'#\[pyclass\].*?pub struct ([A-Za-z0-9_]+)', content, re.DOTALL)

print("pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {")
for func in sorted(set(funcs)):
    print(f"    m.add_function(wrap_pyfunction!({func}, m)?)?;")

for cls in sorted(set(classes)):
    print(f"    m.add_class::<{cls}>()?;")
print("    Ok(())")
print("}")
