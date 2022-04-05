#!/usr/bin/python3
import os
import shutil
from datetime import datetime
import random
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import time


class Test_Config:
    def __init__(self, beamline, root):
        self.beamline = beamline
        # self.root = os.path.abspath(os.pardir)
        self.root = root

        self.beam_dir = os.path.join(self.root, self.beamline)
        self.img_dir = os.path.join(self.beam_dir, 'Images')
        self.result_dir = os.path.join(self.beam_dir, 'Results')
        self.img_list = [os.path.join(self.img_dir, img) for img in os.listdir(self.img_dir)
                         if img.split('.')[-1] == 'jpg']
        self.img_list.sort()
        self.num_imgs = len(self.img_list)

        self.pos_c_count = 0
        self.pos_nc_count = 0
        self.pos_e_count = 0

        self.test_count = 0
        self.skipped_tests = 0

    def get_num_images(self):
        return self.num_imgs

    def get_index_list(self, randomize, user_choice):
        if randomize == 'False':
            return list(range(0, (user_choice*2), 2))
        else:
            random_index_list = list(np.random.choice(np.arange(0, self.num_imgs, 2),
                                     int(user_choice), replace=False))
            random_index_list.sort()
            return random_index_list

    def run_test(self, img_index):
        if (self.test_count == 0) and (self.skipped_tests == 0):
            now = datetime.now()
            self.pos_c_count = 0
            self.pos_nc_count = 0
            self.pos_e_count = 0
            if not os.path.exists(self.result_dir):
                os.mkdir(self.result_dir)
            # Remove after testing
            else:
                shutil.rmtree(self.result_dir)
                os.mkdir(self.result_dir)
            self.tmp_dir = 'config-results-' + now.strftime('%d-%b_%H-%M')
            if not os.path.exists(os.path.join(self.beam_dir, self.tmp_dir)):
                self.tmp_dir = os.path.join(self.beam_dir, self.tmp_dir)
            else:
                self.tmp_dir += '-' + str(random.randint(111, 999))
                self.tmp_dir = os.path.join(self.beam_dir, self.tmp_dir)
            os.mkdir(self.tmp_dir)
            self.results_file = open(os.path.join(
                self.tmp_dir, 'results.txt'), 'x')

        run_img_0 = os.path.join(self.img_dir, self.img_list[img_index])
        run_img_90 = os.path.join(self.img_dir, self.img_list[img_index+1])
        img_name = os.path.basename(run_img_0).split('.')[0][:-6]

        old_out_dir = img_name + '_Old'
        old_out_dir = os.path.join(self.result_dir, old_out_dir)
        # If the image has already been tested it skips.
        if os.path.exists(old_out_dir):
            self.skipped_tests += 1
            return
        else:
            os.mkdir(old_out_dir)
            shutil.copy(run_img_0, old_out_dir)
            shutil.copy(run_img_90, old_out_dir)
            os.chdir(old_out_dir)
            old_outputs = os.popen(f'bash {self.beam_dir}/pin_align-old/pin_align_{self.beamline.lower()}.sh ' +
                                   os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()
            old_config = open('run_output.txt', 'w')
            old_config.writelines(old_outputs)
            old_config.close()
            os.chdir(self.beam_dir)

        new_out_dir = img_name + '_New'
        new_out_dir = os.path.join(self.result_dir, new_out_dir)

        if os.path.exists(new_out_dir):
            try:
                new_outputs = open(os.path.join(
                    new_out_dir, 'run_output.txt'), 'r')
            except Exception:
                self.skipped_tests += 1
                return
        else:
            os.mkdir(new_out_dir)
            shutil.copy(run_img_0, new_out_dir)
            shutil.copy(run_img_90, new_out_dir)
            os.chdir(new_out_dir)
            new_outputs = os.popen(f'bash {self.beam_dir}/pin_align_{self.beamline.lower()}.sh ' +
                                   os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()
            new_config = open('run_output.txt', 'w')
            new_config.writelines(new_outputs)
            new_config.close()
            os.chdir(self.beam_dir)

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
                self.pos_c_count += 1
            elif (xy_violation_new == xy_violation_old) and (tilt_check_new == tilt_check_old) and (pin_check_new == pin_check_old):
                self.pos_c_count += 1
            else:
                # run_results = TMP directory created by pin align
                new_run_results = os.path.join(
                    new_out_dir, new_outputs[4].split(': ')[-1].split('/')[-1].strip())
                old_run_results = os.path.join(
                    old_out_dir, old_outputs[5].split(': ')[-1].split('/')[-1].strip())
                self.pos_nc_count += 1
                self.results_file.write(
                    'Position Incorrect in File: {}\n'.format(img_name))
                pos_diff_tmp_dir = os.path.join(self.tmp_dir, img_name)
                os.mkdir(pos_diff_tmp_dir)
                pos_difold_outputs = os.path.join(pos_diff_tmp_dir, 'Old')
                # os.mkdir(pos_difold_outputs)
                pos_difnew_outputs = os.path.join(pos_diff_tmp_dir, 'New')
                # os.mkdir(pos_difnew_outputs)
                try:
                    shutil.move(new_run_results, pos_difnew_outputs)
                    shutil.move(old_run_results, pos_difold_outputs)
                except Exception as e:
                    print(new_run_results)
                    print(e)
                shutil.copy(run_img_0, pos_diff_tmp_dir)
                shutil.copy(run_img_90, pos_diff_tmp_dir)
                pos_diff_fname = img_name + '_diff_results.txt'
                pos_diff_fpath = os.path.join(pos_diff_tmp_dir, pos_diff_fname)
                pos_diff_f = open(pos_diff_fpath, 'w')
                pos_diff_f.write('New Config Output:\n\n')
                for nline in new_outputs:
                    pos_diff_f.write(nline)
                pos_diff_f.write(
                    '\n\n#######################################################\n\n')
                pos_diff_f.write('Old Config Output:\n\n')
                for oline in old_outputs:
                    pos_diff_f.write(oline)
                pos_diff_f.close()
        except Exception as e:
            self.pos_e_count += 1
            self.results_file.write('Position Error File: {}'.format(img_name))
        self.test_count += 1
        return self.test_count

    def write_testing_results(self):
        self.results_file.write('\n')
        self.results_file.write(
            'Position Correct: {}\n'.format(self.pos_c_count))
        self.results_file.write(
            'Position Incorrect: {}\n'.format(self.pos_nc_count))
        self.results_file.write(
            'Position Error: {}\n'.format(self.pos_e_count))
        self.results_file.close()
        result_mv_path = os.path.join(self.tmp_dir, 'Results')
        shutil.move(self.result_dir, result_mv_path)
        os.chdir(self.beam_dir)


if __name__ == "__main__":
    global running_tests
    running_tests = False
    beam_dir_base = os.getcwd()
    print(beam_dir_base)

    def disable_event():
        pass

    def exit_and_cancel():
        global running_tests
        user_confirm = messagebox.askokcancel(
            'Confirm', 'Are you sure you want to cancel?')
        if user_confirm and not running_tests:
            sys.exit()
        elif user_confirm:
            running_tests = False
            return
        else:
            running_tests = True

    def dir_enter_event(event=None):
        beamline_dir = os.path.join(beam_dir_base, beam_dir_in.get().upper())
        if not os.path.exists(beamline_dir) or not beam_dir_in.get():
            messagebox.showerror('Error', 'Directory DOES NOT Exist!')
            return
        else:
            beamline_data = Test_Config(beam_dir_in.get().upper(), beam_dir_base)
            test_number_in.set(beamline_data.num_imgs // 2)
            test_number_box.focus()
            test_number_box.icursor(END)

    def start_button_click(event=None):
        global running_tests
        os.chdir(beam_dir_base)
        running_tests = True
        beamline_dir = os.path.join(beam_dir_base, beam_dir_in.get().upper())
        if not os.path.exists(beamline_dir) or not beam_dir_in.get():
            messagebox.showerror('Error', 'Directory DOES NOT Exist!')
            return
        pb = ttk.Progressbar(root, orient=HORIZONTAL, length=265,
                             maximum=test_number_in.get(), mode='determinate')
        canvas.create_window(150, 115, window=pb)
        beamline_data = Test_Config(beam_dir_in.get().upper(), beam_dir_base)
        test_index_list = beamline_data.get_index_list(
            random_choice_in.get(), test_number_in.get())
        for i in test_index_list:
            if not running_tests:
                break
            cancel_button.config(command=lambda: exit_and_cancel())
            pb.step()
            canvas.update()
            beamline_data.run_test(i)
        beamline_data.write_testing_results()
        messagebox.showinfo('Finished', 'Finished Testing!')
        pb.destroy()

    root = tk.Tk()
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()

    w = 300
    h = 175

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Testing')
    # root.protocol('WM_DELETE_WINDOW', disable_event)
    root.resizable(0, 0)
    
    canvas = Canvas(root, width=300, height=175, border=1)
    canvas.pack()

    beam_dir_label = Label(root, text='Directory (Ex: AMX): ')
    beam_dir_in = StringVar()
    beam_dir_box = Entry(
        root, width=11, textvariable=beam_dir_in, justify='center')
    canvas.create_window(73, 15, window=beam_dir_label)
    canvas.create_window(200, 15, window=beam_dir_box)

    test_number_label = Label(root, text='Number of Tests: ')
    test_number_in = IntVar()
    test_number_box = Entry(
        root, width=11, text=test_number_in, justify='center')
    canvas.create_window(63, 50, window=test_number_label)
    canvas.create_window(200, 50, window=test_number_box)

    randomize_label = Label(root, text='Randomize Tests?: ')
    random_choice_in = tk.StringVar()
    random_choice_box = ttk.Combobox(
        root, width=10, textvariable=random_choice_in, justify='center')
    random_choice_box['values'] = ['True', 'False']
    random_choice_box['state'] = 'readonly'
    random_choice_box.set('False')
    canvas.create_window(68, 85, window=randomize_label)
    canvas.create_window(200, 85, window=random_choice_box)

    start_button = Button(canvas, text='Start',
                          command=lambda: start_button_click())
    canvas.create_window(45, 155, window=start_button)
    cancel_button = Button(canvas, text='Cancel',
                           command=lambda: exit_and_cancel())
    canvas.create_window(152, 155, window=cancel_button)
    exit_button = Button(canvas, text='Exit', command=sys.exit)
    canvas.create_window(255, 155, window=exit_button)
    beam_dir_box.focus()
    beam_dir_box.bind('<Return>', dir_enter_event)
    test_number_box.bind('<Return>', start_button_click)
    random_choice_box.bind('<Return>', start_button_click)
    root.mainloop()
