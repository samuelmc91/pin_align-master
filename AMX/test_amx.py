#!/usr/bin/python3
import os
import sys
import shutil
from datetime import datetime
import numpy as np

now = datetime.now()
root = os.getcwd()
results_dir = os.path.join(root, 'Results')

if not os.path.exists(results_dir):
    os.mkdir(results_dir)

img_dir = os.path.join(root, 'Images')

if not os.path.exists(img_dir):
    os.mkdir(img_dir)
    print('########### No Images ###########')
    sys.exit()
elif len(os.listdir(img_dir)) < 2:
    print('########### No Images ###########')
    sys.exit()

def reset_results(dir_path, dir_type):
    os.chdir(dir_path)
    temp_f_list = [f for f in os.listdir()]
    for f in temp_f_list:
        new_fname = f + '_' + dir_type
        mov_dir = os.path.join(results_dir, new_fname)
        shutil.move(f, mov_dir)
    os.chdir(root)
 
def test_amx():
    imgs = [f for f in os.listdir(img_dir) if f.split('.')[-1] == 'jpg']
    imgs.sort()
    user_choice = input('Enter all or the number of images to test: ')
    if user_choice == 'all':
        test_image_index = range(0, len(imgs)-1, 2)
    else:
        test_image_index = list(np.random.choice(np.arange(0,len(imgs),2), int(user_choice), replace=False))
    for i in test_image_index:
        run_img_0 = os.path.join(img_dir, imgs[i])
        run_img_90 = os.path.join(img_dir, imgs[i+1])

        img_name = os.path.basename(run_img_0).split('.')[0][:-6]

        old_out_dir = img_name + '_Old'
        old_out_dir = os.path.join(results_dir, old_out_dir)
        if os.path.exists(old_out_dir):
            pass
        else:
            os.mkdir(old_out_dir)
            shutil.copy(run_img_0, old_out_dir)
            shutil.copy(run_img_90, old_out_dir)

            os.chdir(old_out_dir)

            old_outputs = os.popen(f'bash {root}/pin_align-old/pin_align_amx.sh ' + os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()

            old_config = open('run_output.txt', 'w')
            old_config.writelines(old_outputs)

            old_config.close()
            os.chdir(img_dir)

        # New config file generated from the auto config GUI
        new_out_dir = img_name + '_New'
        new_out_dir = os.path.join(results_dir, new_out_dir)
        if os.path.exists(new_out_dir):
            pass
        else:
            os.mkdir(new_out_dir)
            shutil.copy(run_img_0, new_out_dir)
            shutil.copy(run_img_90, new_out_dir)

            os.chdir(new_out_dir)

            new_outputs = os.popen(f'bash {root}/pin_align_amx.sh ' + os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()

            new_config = open('run_output.txt', 'w')
            new_config.writelines(new_outputs)

            new_config.close()
            os.chdir(img_dir)
    os.chdir(root)

new_dir = os.path.join(root, 'New')
if not os.path.exists(new_dir):
    os.mkdir('New')

old_dir = os.path.join(root, 'Old')
if not os.path.exists(old_dir):
    os.mkdir('Old')
            
test_amx()

tmp_dir = 'config-results-' + now.strftime('%d-%b_%H-%M')
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

files = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, f))]
for f in files:
    base_file = os.path.basename(f)
    if f.split('_')[-1] == 'Old':
        shutil.move(f, old_dir)
    elif f.split('_')[-1] == 'New':
        shutil.move(f, new_dir)
    elif len(f.split('.')) > 1:
        pass
    else:
        print(f)

new_files = [os.path.join(new_dir, f) for f in os.listdir(new_dir) if os.path.isdir(os.path.join(new_dir, f))]
old_files = [os.path.join(old_dir, f) for f in os.listdir(old_dir) if os.path.isdir(os.path.join(old_dir, f))]

for file in new_files:
    fname = os.path.basename(file)[:-4]
    fpath = os.path.join(new_dir, fname)
    shutil.move(file, fpath)
    
for file in old_files:
    fname = os.path.basename(file)[:-4]
    fpath = os.path.join(old_dir, fname)
    shutil.move(file, fpath)
    
new_files = [os.path.join(new_dir, f) for f in os.listdir(new_dir) if os.path.isdir(os.path.join(new_dir, f))]
old_files = [os.path.join(old_dir, f) for f in os.listdir(old_dir) if os.path.isdir(os.path.join(old_dir, f))]

new_files.sort()
old_files.sort()

new_files_name = [os.path.basename(f) for f in new_files]
old_files_name = [os.path.basename(f) for f in old_files]

new_files_name.sort()
old_files_name.sort()

for i in range(len(new_files_name)):
    if new_files_name[i] not in old_files_name:
        print(new_files_name[i])
        
for i in range(len(old_files_name)):
    if old_files_name[i] not in new_files_name:
        print(old_files_name[i])
        
pos_c_count = 0
pos_nc_count = 0
pos_e_count = 0

off_c_count = 0
off_nc_count = 0
off_e_count = 0
results_file = open(os.path.join(tmp_dir, 'results.txt'), 'w')
for i in range(len(new_files)):
    f_new = open(os.path.join(new_files[i], 'run_output.txt'), 'r').readlines()
    f_old = open(os.path.join(old_files[i], 'run_output.txt'), 'r').readlines()  
    try:
        pos_lines_new = f_new[-4].split('PX ')[-1]
        pos_lines_old = f_old[-4].split('PX ')[-1]
        
        xy_violation_new = f_new[-1]
        xy_violation_old = f_old[-1].split('CENTERING ')[-1]
        
        tilt_check_new = f_new[-3]
        tilt_check_old = f_old[-3]
        
        pin_check_new = f_new[-2]
        pin_check_old = f_old[-2]
        
        if (pos_lines_new == pos_lines_old):
            pos_c_count += 1
        elif (xy_violation_new == xy_violation_old) and (tilt_check_new == tilt_check_old) and (pin_check_new == pin_check_old):
            pos_c_count += 1
        else:       
            new_run_results = os.path.join(new_files[i], f_new[3].split(': ')[-1].split('/')[-1].strip())
            old_run_results = os.path.join(old_files[i], f_old[5].split(': ')[-1].split('/')[-1].strip())
            pos_nc_count += 1
            results_file.write('Position Incorrect in File: {}\n'.format(os.path.basename(new_files[i])))
            pos_diff_bname = os.path.basename(new_files[i])
            pos_diff_tmp_dir = os.path.join(tmp_dir, pos_diff_bname)
            os.mkdir(pos_diff_tmp_dir)
            pos_diff_old = os.path.join(pos_diff_tmp_dir, 'Old')
            # os.mkdir(pos_diff_old)
            pos_diff_new = os.path.join(pos_diff_tmp_dir, 'New')
            # os.mkdir(pos_diff_new)
            try:
                shutil.move(new_run_results, pos_diff_new)
                shutil.move(old_run_results, pos_diff_old)
            except Exception as e:
                print(new_run_results)
                print(e)
            pos_diff_fname = pos_diff_bname + '_diff_results.txt'
            pos_diff_fpath = os.path.join(pos_diff_tmp_dir, pos_diff_fname)
            pos_diff_f = open(pos_diff_fpath, 'w')
            pos_diff_f.write('New Config Output:\n\n')
            for nline in f_new:
                pos_diff_f.write(nline)
            pos_diff_f.write('\n\n#######################################################\n\n')
            pos_diff_f.write('Old Config Output:\n\n')
            for oline in f_old:
                pos_diff_f.write(oline)
            pos_diff_f.close()
    except Exception as e:
        pos_e_count += 1
        results_file.write('Position Error File: {}'.format(os.path.basename(new_files[i])))
        
    try:
        off_lines_new = f_new[-3:]
        off_lines_old = f_old[-3:]
        if off_lines_new == off_lines_old:
            off_c_count += 1
        else:
            off_nc_count += 1
    except Exception:
        off_e_count += 1
        results_file.write('Offset Error File: {}'.format(os.path.basename(new_files[i])))

results_file.write('\n')
results_file.write('Position Correct: {}\n'.format(pos_c_count))
results_file.write('Position Incorrect: {}\n'.format(pos_nc_count))
results_file.write('Position Error: {}\n'.format(pos_e_count))
results_file.write('\n')
results_file.write('Offset Correct: {}\n'.format(off_c_count))
results_file.write('Offset Incorrect: {}\n'.format(off_nc_count))
results_file.write('Offset Error: {}\n'.format(off_e_count))
results_file.close()
shutil.move(new_dir, os.path.join(tmp_dir, 'New'))
shutil.move(old_dir, os.path.join(tmp_dir, 'Old'))
os.rmdir(results_dir)