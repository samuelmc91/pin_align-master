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

config_c_date = time.ctime(os.path.getmtime(config_file)).split(' ')

time_diff = [i for i, item in enumerate(config_c_date) if item not in run_start]
if len(time_diff) <= 1:
    os.system('cp {} {}'.format(config_file, root))