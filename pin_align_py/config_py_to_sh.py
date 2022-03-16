#!/usr/bin/python3
import os
import re
import shutil

def change_config_file(config_file_path, line_text, new_value):
    lines = open(config_file_path, 'r').readlines()
    line_num = [num for num, f in enumerate(
        lines, 0) if re.findall(line_text, f)][0]
    lines[line_num] = line_text + str(new_value) + '\n'
    out = open(config_file_path, 'w')
    out.writelines(lines)
    out.close()

def convert_to_bash(config_file_path):
    python_config = open(config_file_path, 'r')
    motor_values = ['X_POS', 'Y_POS', 'Z_POS']
    bash_config_path = 'pin_align_config.sh'

    for p_line in python_config:
        if p_line.split('=')[0].strip() in motor_values:
            line_text = 'export ' + p_line.split('=')[0].strip()
            new_value = p_line.split('=')[-1].strip()
            if new_value == 'True':
                change_config_file(bash_config_path, line_text, '=1')
            elif new_value == 'False':
                change_config_file(bash_config_path, line_text, "")
        elif p_line.split('=')[0].strip() == 'DEFAULT_PIXELS_PER_MM':
            new_value = '="' + p_line.split('=')[-1].strip() + '"'
            change_config_file(bash_config_path, 'DEFAULT_PIXELS_PER_MM', new_value)
        elif len(p_line.split('=')) >= 2:
            bash_config = open(bash_config_path, 'r')
            for b_line in bash_config:
                if p_line.split('=')[0].strip() == b_line.split('=')[0].strip():
                    line_text = p_line.split('=')[0].strip()
                    new_value = p_line.split('=')[-1].strip()
                    try:
                        new_value = '=$(({}))'.format(int(new_value))
                        change_config_file(bash_config_path, line_text, new_value)
                    except Exception:
                        pass
            bash_config.close()
    python_config.close()
    shutil.copy(bash_config_path, os.path.abspath(os.pardir))
    
if __name__ == '__main__':
    convert_to_bash('pin_align_config.py')