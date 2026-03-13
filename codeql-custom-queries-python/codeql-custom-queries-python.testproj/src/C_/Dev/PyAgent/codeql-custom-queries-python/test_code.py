# sample file for CodeQL pack tests
# we want to catch uses of eval and subprocess.run(shell=True)

def dangerous_eval(user_input):
    return eval(user_input)

import subprocess

def run_shell(cmd):
    subprocess.run(cmd, shell=True)
