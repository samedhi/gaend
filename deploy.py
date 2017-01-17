#! /usr/bin/env python
import re
import subprocess

RM = 'rm -rf dist'
subprocess.check_output(RM.split(' '))

PORCELAIN = 'git status --porcelain'
clean = subprocess.check_output(PORCELAIN.split(' '))
assert clean == "", clean

with open('setup.py', 'r') as setup:
    c = setup.read()
    r = re.search("version='(\d+\.\d+\.\d+.dev)(\d+)", c)
    s = r.group(1)
    i = int(r.group(2))
    i_inc = i + 1
    setup_inc = re.sub("dev%s" % i, "dev%s" % i_inc, c)

with open('setup.py', 'w+') as setup:
    setup.write(setup_inc)

BUILD_WHEEL = 'python setup.py sdist bdist_wheel'
subprocess.check_output(BUILD_WHEEL.split(' '))

PIP_PUSH = 'twine upload dist/gaend-*'
subprocess.check_output(PIP_PUSH.split(' '))

COMMIT = 'git add setup.py; git commit -m "pip deploy version %s"' % (s + i_inc)
subprocess.check_output(COMMIT.split(' '))
