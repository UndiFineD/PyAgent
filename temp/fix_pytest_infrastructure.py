from pathlib import Path




def fix_infrastructure_conftest():










    print("Fixing tests/unit/infrastructure/conftest.py...")
    path = Path("tests/unit/infrastructure/conftest.py")
    if not path.exists():
        print(f"File not found: {path}")




        return

    content = path.read_text(encoding="utf-8")

    # Update the path to execution_engine.py


    old_str = 'load_agent_module("backend/execution_engine.py")'
    new_str = 'load_agent_module("infrastructure/backend/execution_engine.py")'

    if old_str in content:
        content = content.replace(old_str, new_str)



        path.write_text(content, encoding="utf-8")
        print("Updated execution_engine.py path.")
    else:
        print("Path already updated or not found.")





if __name__ == "__main__":
    fix_infrastructure_conftest()
