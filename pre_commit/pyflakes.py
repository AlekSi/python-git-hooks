import sys
import subprocess

import git_hooks


def run():
    files = filter(lambda f: f.endswith('.py'), git_hooks.pre_commit_changed_files())

    if files:
        bin = git_hooks.locate_python_tool('pyflakes')
        try:
            print bin, files
            subprocess.check_call([bin] + files)
            print
        except subprocess.CalledProcessError:
            sys.exit(1)
