# Common library for Git Hooks

from collections import defaultdict
import os
import os.path
import subprocess
import sys

__pre_commit_changed_files = None


def locate_python_tool(tool):
    env = os.getenv('VIRTUAL_ENV')
    if env:
        bin = '%s/bin/%s' % (env, tool)
        if os.path.isfile(bin):
            return bin

    return tool


def pre_commit_check_whitespace():
    try:
        subprocess.check_call(['git', 'diff', '--cached', '--check'])
    except subprocess.CalledProcessError:
        sys.exit(1)


def pre_commit_changed_files(types='ACMR'):
    """Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), Type changed (T),
       Unmerged (U), Unknown (X), pairing Broken (B)."""

    global __pre_commit_changed_files
    if __pre_commit_changed_files is None:
        __pre_commit_changed_files = defaultdict(set)
        out = subprocess.check_output(['git', 'diff', '--cached', '--name-status']).strip().split('\n')
        for s in out:
            status, f = s.split('\t')
            __pre_commit_changed_files[status.strip()].add(f.strip())

    res = set()
    for t in types:
        res |= __pre_commit_changed_files[t]
    return res
