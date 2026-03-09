import yaml

def test_ci_runs_pytest():
    data = yaml.safe_load(open('.github/workflows/ci.yml'))
    steps = data['jobs']['test']['steps']
    assert any('pytest' in (step.get('run') or '') for step in steps)
