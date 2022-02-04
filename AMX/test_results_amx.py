import os
import shutil
import sys
from distutils.dir_util import copy_tree
from datetime import datetime

now = datetime.now()
root = os.getcwd()
tmp_dir = 'config-results-' + now.strftime('%H-%M')
os.mkdir(tmp_dir)
results_dir = os.path.join(root, 'Results')

def reset_results(dir_path, dir_type):
    os.chdir(dir_path)
    temp_f_list = [f for f in os.listdir()]
    for f in temp_f_list:
        new_fname = f + '_' + dir_type
        mov_dir = os.path.join(results_dir, new_fname)
        shutil.move(f, mov_dir)
    os.chdir(root)

new_dir = os.path.join(root, 'New')
if not os.path.exists(new_dir):
    os.mkdir('New')

old_dir = os.path.join(root, 'Old')
if not os.path.exists(old_dir):
    os.mkdir('Old')    
    
try:
    if sys.argv[1] == '1':
        reset_results(new_dir, 'New')
        reset_results(old_dir, 'Old')
        print('##### Reset Done #####')
        sys.exit()
    if sys.argv[1] == '2':
        reset_results(new_dir, 'New')
        reset_results(old_dir, 'Old')
except Exception as e:
    pass

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
    os.rename(file, fpath)
    
for file in old_files:
    fname = os.path.basename(file)[:-4]
    fpath = os.path.join(old_dir, fname)
    os.rename(file, fpath)
    
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
results_file = open('results.txt', 'w')
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
            new_run_results = f_new[3].split(': ')[-1].split('/')
            old_run_results = f_old[5].split(': ')[-1].split('/')
            shutil.move(new_run_results)
            pos_nc_count += 1
            results_file.write('Position Incorrect in File: {}\n'.format(os.path.basename(new_files[i])))
            pos_diff_bname = os.path.basename(new_files[i])
            pos_diff_tmp_dir = os.path.join(tmp_dir, pos_diff_bname)
            os.mkdir(pos_diff_tmp_dir)
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