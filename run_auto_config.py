#!/usr/bin/python3

import os
import sys
import time

run_start = set(time.ctime(time.time()).split(' '))

root = os.getcwd()
img = os.path.join(root, sys.argv[1])
run_dir = os.path.join(root, 'pin_align_py')
os.chdir(run_dir)

run_script = 'pin_align_auto_config.py'
config_file = 'pin_align_config.sh'

os.system('python3 {} {}'.format(run_script, img))