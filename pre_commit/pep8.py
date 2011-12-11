import sys
import subprocess

import git_hooks

ARGS = '--repeat --statistics --ignore=E501'.split(' ')


def run():
    files = filter(lambda f: f.endswith('.py'), git_hooks.pre_commit_changed_files())

    if files:
        bin = git_hooks.locate_python_tool('pep8')
        try:
            print bin, ARGS, files
            subprocess.check_call([bin] + ARGS + files)
            print
        except subprocess.CalledProcessError:
            sys.exit(1)
