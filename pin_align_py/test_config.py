#!/usr/bin/python3
import os
import sys
import shutil
from datetime import datetime
import numpy as np
import time
import random

global beamline_dict

now = datetime.now()
root = os.path.abspath(os.pardir)
beamline_dict = {'AMX': {'beam_dir': None, 'img_dir': None, 'result_dir': None, 'img_list': []},
                 'FMX': {'beam_dir': None, 'img_dir': None, 'result_dir': None, 'img_list': []}}

def get_beam_info(beamline):
    global beamline_dict
    beam_dir = os.path.join(root, beamline)
    img_dir = os.path.join(beam_dir, 'Images')
    result_dir = os.path.join(beam_dir, 'Results')
    img_list = [os.path.join(img_dir,img) for img in os.listdir(img_dir) 
                                                if img.split('.')[-1] == 'jpg']
    img_list.sort()
    beamline_dict[beamline]['beam_dir'] = beam_dir
    beamline_dict[beamline]['img_dir'] = img_dir
    beamline_dict[beamline]['result_dir'] = result_dir
    beamline_dict[beamline]['img_list'] = img_list
    # beamline_dict[beamline] = beam_img_list
    # return img_list

def get_num_images(beamline):
    global beamline_dict
    if not beamline_dict[beamline]['img_list']:
        get_beam_info(beamline)
        return len(beamline_dict[beamline]['img_list'])
    else:
        return len(beamline_dict[beamline]['img_list'])

def get_index_list(beamline, randomize, user_choice):
    if not randomize:
        return list(range(0, (user_choice*2), 2))
    else:
        random_index_list = list(np.random.choice(np.arange(0, get_num_images(beamline),2),
                                int(user_choice), replace=False))
        random_index_list.sort()
        return random_index_list

def test_config(beamline, randomize, user_choice):
    global beamline_dict
    global pos_c_count
    global pos_nc_count
    global pos_e_count

    pos_c_count = 0
    pos_nc_count = 0
    pos_e_count = 0
    if not beamline_dict[beamline]['img_list']:
        get_beam_info(beamline)
    run_index_list = get_index_list(beamline, randomize, user_choice)
    beam_dir = beamline_dict[beamline]['beam_dir']
    img_dir = beamline_dict[beamline]['img_dir']
    result_dir = beamline_dict[beamline]['result_dir']
    img_list = beamline_dict[beamline]['img_list']
    
    os.chdir(beam_dir)
    
    if not os.path.exists(result_dir):
        os.mkdir('Results')
    
    tmp_dir = 'config-results-' + now.strftime('%d-%b_%H-%M')
    if not os.path.exists(os.path.join(beam_dir, tmp_dir)):
        tmp_dir = os.path.join(beam_dir, tmp_dir)
    else:
        tmp_dir += '-' + str(random.randint(111, 999))
        tmp_dir = os.path.join(beam_dir, tmp_dir)
    os.mkdir(tmp_dir)
    results_file = open(os.path.join(tmp_dir, 'results.txt'), 'x')
    for i in run_index_list:
        run_img_0 = os.path.join(img_dir, img_list[i])
        run_img_90 = os.path.join(img_dir, img_list[i+1])

        img_name = os.path.basename(run_img_0).split('.')[0][:-6]

        old_out_dir = img_name + '_Old'
        old_out_dir = os.path.join(result_dir, old_out_dir)
        if os.path.exists(old_out_dir):
            continue
        else:
            os.mkdir(old_out_dir)
            shutil.copy(run_img_0, old_out_dir)
            shutil.copy(run_img_90, old_out_dir)

            os.chdir(old_out_dir)

            old_outputs = os.popen(f'bash {beam_dir}/pin_align-old/pin_align_{beamline.lower()}.sh ' + 
                                     os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()

            old_config = open('run_output.txt', 'w')
            old_config.writelines(old_outputs)

            old_config.close()
            os.chdir(img_dir)

        # New config file generated from the auto config GUI
        new_out_dir = img_name + '_New'
        new_out_dir = os.path.join(result_dir, new_out_dir)
        if os.path.exists(new_out_dir):
            continue
        else:
            os.mkdir(new_out_dir)
            shutil.copy(run_img_0, new_out_dir)
            shutil.copy(run_img_90, new_out_dir)

            os.chdir(new_out_dir)

            new_outputs = os.popen(f'bash {beam_dir}/pin_align_{beamline.lower()}.sh ' + 
                                     os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()

            new_config = open('run_output.txt', 'w')
            new_config.writelines(new_outputs)

            new_config.close()
            os.chdir(img_dir)
        process_result(new_outputs, old_outputs, new_out_dir, old_out_dir, tmp_dir, img_name, results_file)
    results_file.write('\n')
    results_file.write('Position Correct: {}\n'.format(pos_c_count))
    results_file.write('Position Incorrect: {}\n'.format(pos_nc_count))
    results_file.write('Position Error: {}\n'.format(pos_e_count))
    results_file.close()
    shutil.rmtree(result_dir)
    os.chdir(beam_dir)

def process_result(new_outputs, old_outputs, new_out_dir, old_out_dir, tmp_dir, img_name, results_file):
    global pos_c_count
    global pos_nc_count
    global pos_e_count
    try:
        pos_lines_new = new_outputs[-4].split('PX ')[-1]
        pos_lines_old = old_outputs[-4].split('PX ')[-1]
        
        xy_violation_new = new_outputs[-1]
        xy_violation_old = old_outputs[-1].split('CENTERING ')[-1]
        
        tilt_check_new = new_outputs[-3]
        tilt_check_old = old_outputs[-3]
        
        pin_check_new = new_outputs[-2]
        pin_check_old = old_outputs[-2]
        
        if (pos_lines_new == pos_lines_old):
            pos_c_count += 1
        elif (xy_violation_new == xy_violation_old) and (tilt_check_new == tilt_check_old) and (pin_check_new == pin_check_old):
            pos_c_count += 1
        else:
            # run_results = TMP directory created by pin align
            new_run_results = os.path.join(new_out_dir, new_outputs[3].split(': ')[-1].split('/')[-1].strip())
            old_run_results = os.path.join(old_out_dir, old_outputs[5].split(': ')[-1].split('/')[-1].strip())
            pos_nc_count += 1
            results_file.write('Position Incorrect in File: {}\n'.format(img_name))
            pos_diff_tmp_dir = os.path.join(tmp_dir, img_name)
            os.mkdir(pos_diff_tmp_dir)
            pos_difold_outputs = os.path.join(pos_diff_tmp_dir, 'Old')
            os.mkdir(pos_difold_outputs)
            pos_difnew_outputs = os.path.join(pos_diff_tmp_dir, 'New')
            os.mkdir(pos_difnew_outputs)
            try:
                shutil.move(new_run_results, pos_difnew_outputs)
                shutil.move(old_run_results, pos_difold_outputs)
            except Exception as e:
                print(new_run_results)
                print(e)
            pos_diff_fname = pos_diff_bname + '_diff_results.txt'
            pos_diff_fpath = os.path.join(pos_diff_tmp_dir, pos_diff_fname)
            pos_diff_f = open(pos_diff_fpath, 'w')
            pos_diff_f.write('New Config Output:\n\n')
            for nline in new_outputs:
                pos_diff_f.write(nline)
            pos_diff_f.write('\n\n#######################################################\n\n')
            pos_diff_f.write('Old Config Output:\n\n')
            for oline in old_outputs:
                pos_diff_f.write(oline)
            pos_diff_f.close()
    except Exception as e:
        pos_e_count += 1
        results_file.write('Position Error File: {}'.format(img_name))
    return

if __name__ == "__main__":
    test_config('AMX', False, 100)
    