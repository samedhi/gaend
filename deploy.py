#! /usr/bin/env python
import re

with open('setup.py', 'r') as setup:
    c = setup.read()
    r = re.search("version='\d+\.\d+\.\d+.dev(\d+)", c)
    i = int(r.group(1))
    i_inc = i + 1
    setup_inc = re.sub("dev%s" % i, "dev%s" % i_inc, c)

with open('setup.py', 'w+') as setup:
    setup.write(setup_inc)
