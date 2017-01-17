#! /usr/bin/env python
import re
import subprocess

with open('setup.py', 'r') as setup:
    c = setup.read()
    r = re.search("version='\d+\.\d+\.\d+.dev(\d+)", c)
    i = int(r.group(1))
    i_inc = i + 1
    setup_inc = re.sub("dev%s" % i, "dev%s" % i_inc, c)

with open('setup.py', 'w+') as setup:
    setup.write(setup_inc)

BUILD_WHEEL = 'python setup.py sdist bdist_wheel'
subprocess.check_output(BUILD_WHEEL.split(' '))

PIP_PUSH = 'twine upload dist/gaend-*'
subprocess.check_output(PIP_PUSH.split(' '))
