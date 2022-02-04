#!/usr/bin/python3

import os
import sys

root = os.path.join(os.getcwd(), 'pin_align_py')
run_script = os.path.join(root, 'pin_align_auto_config.py')

img = sys.argv[1]

os.system('python3 {} {}'.format(run_script, img))