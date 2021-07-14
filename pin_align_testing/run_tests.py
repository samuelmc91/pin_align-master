#!/usr/bin/python3
import os
import sys
from datetime import datetime

root = os.getcwd()
new_images_path = os.path.join(root, 'new_pins')
for folder in os.listdir(new_images_path):
    folder_path = os.path.join(new_images_path, folder)
    tmp_dir = os.path.join(root, folder + '_results')
    if os.path.exists(tmp_dir):
        os.system('rm -r ' + tmp_dir)
    os.system('mkdir ' + tmp_dir)
    os.system('cp {} {} {}'.format('*.py', '*.sh', tmp_dir))
    os.chdir(tmp_dir)
    python_fname = 'python_results_' + folder + '.txt'
    bash_fname = 'bash_results_' + folder + '.txt'

    images = sorted([f for f in os.listdir(folder_path) if f.split('.')[-1] == 'jpg'], key=str.lower)

    python_f = open(python_fname, 'w')
    bash_f = open(bash_fname, 'w')

    run_image_list = []
    for i in range(0, len(images) - 1, 2):
        os.system('cp {} {} {}'.format(os.path.join(folder_path, images[i]), os.path.join(folder_path, images[i + 1]), tmp_dir))
        run_image_list.append(images[i] + ' ' + images[i + 1])

    python_start = datetime.now()
    python_outputs = [os.popen('python3 ../pin_align_amx.py ' + f + ' -d').readlines() for f in run_image_list]
    python_stop = datetime.now()

    python_f.write('Total Runtime: {:.5f}\n\n'.format(float(str(python_stop - python_start).split(':')[-1])))

    python_px = []
    python_mm = []
    for output in python_outputs:
        header_line = '######## ' + output[0].split(':')[-1].strip().split('/')[-1] + ' ########\n\n'
        python_f.write(header_line)
        for line in output:
            if len(line.split('PX')) > 1:
                python_px.append(line.split('PX')[-1])
            elif len(line.split('mm')) > 1:
                python_mm.append(line.split('mm')[-1])
            python_f.write(line)
        python_f.write('\n')

    python_f.close()

    # sys.exit(0)

    bash_start = datetime.now()
    bash_outputs = [os.popen('bash ../pin_align_amx.sh ' + f).readlines() for f in run_image_list]
    bash_stop = datetime.now()

    bash_f.write('Total Runtime: {:.5f}\n\n'.format(float(str(bash_stop - bash_start).split(':')[-1])))

    bash_px = []
    bash_mm = []
    for output in bash_outputs:
        header_line = '######## ' + output[3].split(':')[-1].strip() + ' ########\n\n'
        bash_f.write(header_line)
        for line in output:
            if len(line.split('PX')) > 1:
                bash_px.append(line.split('PX')[-1])
            elif len(line.split('mm')) > 1:
                bash_mm.append(line.split('mm')[-1])
            bash_f.write(line)
        bash_f.write('\n')
    
    bash_f.close()

    print(len(bash_px), len(python_px))
    print(len(bash_mm), len(python_mm))
    os.system('rm {} {} {}'.format('*.py', '*.sh', '*.jpg'))
    os.chdir(root)
    # sys.exit(0)
    # os.system('rm -r samuel*')