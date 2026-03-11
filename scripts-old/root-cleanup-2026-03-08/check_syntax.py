import os
import py_compile

errors=[]
for root,dirs,files in os.walk('src'):
    for f in files:
        if f.endswith('.py'):
            path=os.path.join(root,f)
            try:
                py_compile.compile(path, doraise=True)
            except Exception as e:
                errors.append((path,str(e)))
print('done',len(errors),'errors')
for p,e in errors[:20]:
    print(p, '->', e)
