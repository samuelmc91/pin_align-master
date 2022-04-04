#!/usr/bin/python3
import os
import tkinter as tk
import sys
import re
import importlib
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import *
from PIL import Image
import time
############### Local Packages ###############
from image_canvas import Image_Canvas
import pin_align_config
from pin_align_config import *
from config_py_to_sh import convert_to_bash
############### Global Variables ###############
global display_help_image_tk
global display_help_image
global on_off_list
global auto_start_on_off
global filetypes
############### Rect & Edge ###############
on_off_list = [[False, False],  # Pin Tip
               [False, False],  # Pin Body
               [False, False],  # Pin Base
               [False, False],  # Tilt Check Top
               [False, False],  # Tilt Check Bottom
               [False, False],  # Pin Check Top
               [False, False],  # Pin Check Bottom
               [False, False],  # Small Box
               [False, False]]  # Big Box

filetypes = (
    ('All files', '*.*'),
    ('Image files', '*.jpg'),
    ('Python files', '*.py'),
    ('Bash files', '*.sh'),
    ('Text files', '*.txt')
)

file_root = os.getcwd()
config_file_path = os.path.join(file_root, 'pin_align_config.py')


def motion(event):
    x, y = event.x, event.y
    current_pos = 'X: {}\t Y: {}'.format(x, y)
    mouse_pos.config(text=current_pos)


def get_pin_crops():
    inputs = importlib.reload(pin_align_config)
    pin_crops = [[slice(inputs.DEFAULT_ROI_Y1, inputs.DEFAULT_ROI_Y2), inputs.PIN_TIP],
                 [slice(inputs.DEFAULT_ROI_Y1, inputs.DEFAULT_ROI_Y2),
                  inputs.PIN_BODY],
                 [slice(inputs.DEFAULT_ROI_Y1, inputs.DEFAULT_ROI_Y2),
                  inputs.PIN_BASE],
                 [inputs.TILT_CHECK_TOP, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.TILT_CHECK_BOTTOM, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.PIN_CHECK_TOP, inputs.PIN_BODY],
                 [inputs.PIN_CHECK_BOTTOM, inputs.PIN_BODY],
                 [inputs.SMALL_BOX_HEIGHT, inputs.SMALL_BOX_WIDTH],
                 [inputs.BIG_BOX_HEIGHT, inputs.BIG_BOX_WIDTH],
                 [inputs.X_CENTER, inputs.Y_CENTER],
                 [slice(inputs.PIN_TIP_X1, inputs.PIN_BASE_X2), slice(
                     inputs.DEFAULT_ROI_Y1, inputs.DEFAULT_ROI_Y2)],
                 [inputs.PIN_X1_OFFSET, None]]
    return pin_crops


def update_entry_boxes(x_center=None, y_center=None):
    update_config = importlib.reload(pin_align_config)
    if not x_center:
        x_center = update_config.X_CENTER
    if not y_center:
        y_center = update_config.Y_CENTER
    pin_x1_offset_in.delete(0, END)
    pin_x1_offset_in.insert(END, update_config.PIN_X1_OFFSET)
    default_pixels_per_mm_in.delete(0, END)
    default_pixels_per_mm_in.insert(END, update_config.DEFAULT_PIXELS_PER_MM)
    default_width_in.delete(0, END)
    default_width_in.insert(END, update_config.DEFAULT_WIDTH)
    x_center_in.delete(0, END)
    x_center_in.insert(END, x_center)
    y_center_in.delete(0, END)
    y_center_in.insert(END, y_center)
    default_height_in.delete(0, END)
    default_height_in.insert(END, update_config.DEFAULT_HEIGHT)
    min_x_in.delete(0, END)
    min_x_in.insert(END, update_config.MIN_X)
    min_y_in.delete(0, END)
    min_y_in.insert(END, update_config.MIN_Y)
    min_z_in.delete(0, END)
    min_z_in.insert(END, update_config.MIN_Z)
    max_x_in.delete(0, END)
    max_x_in.insert(END, update_config.MAX_X)
    max_y_in.delete(0, END)
    max_y_in.insert(END, update_config.MAX_Y)
    max_z_in.delete(0, END)
    max_z_in.insert(END, update_config.MAX_Z)


def save_config(new_filepath):
    new_filepath = os.path.join(
        os.path.abspath(os.pardir), new_filepath + '.sh')
    convert_to_bash(new_filepath)
    print(new_filepath)
    return


def save_config_as():
    global filetypes
    filename = fd.asksaveasfilename(initialdir=os.path.abspath(os.pardir), title='Save Config', defaultextension='.sh',
                                    filetypes=filetypes)
    if filename:
        convert_to_bash(filename)
    return


def crop_button_left_click(event, image_in_canvas, button_choice):
    global on_off_list
    pin_crops = get_pin_crops()
    Y1 = pin_crops[button_choice][0].start
    Y2 = pin_crops[button_choice][0].stop
    X1 = pin_crops[button_choice][1].start
    X2 = pin_crops[button_choice][1].stop

    if not on_off_list[button_choice][0]:
        new_rect = image_in_canvas.create_crop_rect(X1, Y1, X2, Y2)
        on_off_list[button_choice][0] = new_rect
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))
    elif on_off_list[button_choice][0]:
        image_in_canvas.delete_crop_rect(on_off_list[button_choice][0])
        on_off_list[button_choice][0] = False

    x1_value_in.delete(0, 'end')
    y1_value_in.delete(0, 'end')

    x2_value_in.delete(0, 'end')
    y2_value_in.delete(0, 'end')

    x1_value_in.insert(END, str(X1))
    y1_value_in.insert(END, str(Y1))

    x2_value_in.insert(END, str(X2))
    y2_value_in.insert(END, str(Y2))
    return pin_crops


def crop_button_right_click(event, image_in_canvas, button_choice):
    global on_off_list
    pin_crops = get_pin_crops()

    X = pin_crops[0][1].start
    Y = pin_crops[0][0].start

    X1 = pin_crops[button_choice][1].start - X
    X2 = pin_crops[button_choice][1].stop - X

    Y1 = pin_crops[button_choice][0].start - Y
    Y2 = Y1 + (pin_crops[button_choice][0].stop -
               pin_crops[button_choice][0].start)

    TOP = pin_crops[button_choice][0].start
    LEFT = pin_crops[button_choice][1].start

    if not on_off_list[button_choice][1]:
        new_edge_crop = image_in_canvas.create_crop_edge(
            X1, X2, Y1, Y2, TOP, LEFT)
        on_off_list[button_choice][1] = new_edge_crop
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))
    elif on_off_list[button_choice][1]:
        image_in_canvas.delete_crop_edge(on_off_list[button_choice][1])
        on_off_list[button_choice][1] = False


def clear_image_canvas(image_in_canvas):
    global on_off_list
    on_off_list = image_in_canvas.clear_canvas(on_off_list)


def auto_start_button_left(event, image_in_canvas):
    global help_image_window
    global auto_start_on_off
    clear_image_canvas(image_in_canvas)
    if not auto_start_on_off:
        auto_start_on_off = True
        pin_crops = get_pin_crops()
        filename = os.path.join(os.getcwd(), 'display_help_image.jpg')

        current_crop_title.config(
            text='Points should be as shown', font=('helvetica', 14))
        help_image = image_in_canvas.get_help_image(filename)
        help_image_label = tk.Label(root, image=help_image)
        help_image_window = info_canvas_top.create_window(
            310, 250, window=help_image_label)

        pin_tip_button.unbind("<Button-1>")
        pin_body_button.unbind("<Button-1>")
        pin_cap_button.unbind("<Button-1>")
        tilt_check_top_button.unbind("<Button-1>")
        tilt_check_bottom_button.unbind("<Button-1>")
        pin_check_top_button.unbind("<Button-1>")
        pin_check_bottom_button.unbind("<Button-1>")

        pin_tip_button.unbind("<Button-3>")
        pin_body_button.unbind("<Button-3>")
        pin_cap_button.unbind("<Button-3>")
        tilt_check_top_button.unbind("<Button-3>")
        tilt_check_bottom_button.unbind("<Button-3>")
        pin_check_top_button.unbind("<Button-3>")
        pin_check_bottom_button.unbind("<Button-3>")

        pin_tip_button.config(bg='red')
        pin_body_button.config(bg='red')
        pin_cap_button.config(bg='red')
        tilt_check_top_button.config(bg='red')
        tilt_check_bottom_button.config(bg='red')
        pin_check_top_button.config(bg='red')
        pin_check_bottom_button.config(bg='red')

        image_in_canvas.auto_crop_start(y1_value_label, x1_value_label, x2_value_label, y2_value_label,
                                        x1_value_in, y1_value_in, x2_value_in, y2_value_in)
    else:
        image_in_canvas.auto_crop_stop(
            y1_value_label, x1_value_label, x2_value_label, y2_value_label)
        clear_image_canvas(image_in_canvas)
        info_canvas_top.delete(help_image_window)
        auto_start_on_off = False
        pin_tip_button.bind("<Button-1>", lambda event,
                            arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 0))
        pin_body_button.bind("<Button-1>", lambda event,
                             arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 1))
        pin_cap_button.bind("<Button-1>", lambda event,
                            arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 2))
        tilt_check_top_button.bind(
            "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 3))
        tilt_check_bottom_button.bind(
            "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 4))
        pin_check_top_button.bind("<Button-1>", lambda event,
                                  arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 5))
        pin_check_bottom_button.bind(
            "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 6))

        pin_tip_button.bind("<Button-3>", lambda event,
                            arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 0))
        pin_body_button.bind("<Button-3>", lambda event,
                             arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 1))
        pin_cap_button.bind("<Button-3>", lambda event,
                            arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 2))
        tilt_check_top_button.bind(
            "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 3))
        tilt_check_bottom_button.bind(
            "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 4))
        pin_check_top_button.bind("<Button-3>", lambda event,
                                  arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 5))
        pin_check_bottom_button.bind(
            "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 6))

        pin_tip_button.config(bg='green')
        pin_body_button.config(bg='green')
        pin_cap_button.config(bg='green')
        tilt_check_top_button.config(bg='green')
        tilt_check_bottom_button.config(bg='green')
        pin_check_top_button.config(bg='green')
        pin_check_bottom_button.config(bg='green')


def change_config_file(config_file_path, line_text, new_value):
    old_config = open(config_file_path, 'r')
    lines = old_config.readlines()
    old_config.close()
    line_num = [num for num, f in enumerate(
        lines, 0) if re.findall(line_text, f)][0]
    # print(int(lines[line_num].split(' = ')[-1]))
    try:
        if int(lines[line_num].split(' = ')[-1]) == int(new_value):
            return
    except Exception:
        pass
    lines[line_num] = line_text + ' = ' + str(new_value) + '\n'
    out = open(config_file_path, 'w')
    out.writelines(lines)
    out.close()


def select_files():
    global filetypes
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.path.abspath(os.pardir),
        filetypes=filetypes)
    return filename

def about_button():
    about_message = """
    Scripts for detecting pin alignment issues from top view camera\n
    Designed by Edwin Lazo, Jean Jakoncic, Herbert J. Bernstein
    Copyright 29 Jan 2019, Herbert J. Bernstein as a copyleft for the GPL and LGPL\n
    Revised 14 Feb 2019, Herbert J. Bernstein, Edwin Lazo
    \t-improve base tilt detection & use pgm instead of jpg
    Revised 12 Mar 2019, Edwin Lazo, Herbert J. Bernstein
    \t-Extended configuration after camera realignment
    Revised 4 Apr 2022, Samuel Clark, Edwin Lazo, Herbert J. Bernstein
    \t-Extended pin align functionality with graphical user interface (GUI)
    \tfor easy configuration and beamline integration\n
    YOU MAY REDISTRIBUTE THE PIN_ALIGN PACKAGE UNDER THE TERMS OF THE GPL
    ALTERNATIVELY YOU MAY REDISTRIBUTE THE PIN_ALIGN API UNDER THE TERMS OF THE LGPL"""
    about_window = tk.Toplevel()
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()

    w = 665
    h = 250

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    about_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    about_window.title('About')
    # root.protocol('WM_DELETE_WINDOW', disable_event)
    about_window.resizable(0, 0)
    about_canvas = Canvas(about_window, width=w, height=h, border=1, bg='white')
    about_canvas.pack()
    about_label = Label(about_canvas, text=about_message, justify='left', bg='white')
    about_label.config(font=('helvetica', 10))
    about_label.pack()
    about_ok = Button(about_canvas, text='OK', command=about_window.destroy)
    about_ok.pack()
    about_window.mainloop()

def switch_gui_config(config_file_path):
    change_var_list = ['DEFAULT_PIXELS_PER_MM', 'PIN_X1_OFFSET', 'X_CENTER', 'Y_CENTER', 'DEFAULT_HEIGHT',
                       'DEFAULT_WIDTH', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z']
    filename = select_files()
    if filename:
        clear_image_canvas(image_in_canvas)
        for line in open(filename, 'r').readlines():
            new_line_var = line.split('=')[0].strip()
            if new_line_var in change_var_list:
                new_line_val = line.split('=$((')[-1].replace('))', '').strip()
                if new_line_var == change_var_list[0]:
                    new_line_val = line.split('=')[-1].replace('"', '').strip()
                    
                    default_pixels_per_mm_in.delete(0, END)
                    default_pixels_per_mm_in.insert(END, new_line_val)
                if new_line_var == change_var_list[1]:
                    
                    pin_x1_offset_in.delete(0, END)
                    pin_x1_offset_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[2]:
                    
                    x_center_in.delete(0, END)
                    x_center_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[3]:
                    
                    y_center_in.delete(0, END)
                    y_center_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[4]:
                    
                    default_height_in.delete(0, END)
                    default_height_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[5]:
                    
                    default_width_in.delete(0, END)
                    default_width_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[6]:
                    
                    min_x_in.delete(0, END)
                    min_x_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[7]:
                    
                    max_x_in.delete(0, END)
                    max_x_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[8]:
                    
                    min_y_in.delete(0, END)
                    min_y_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[9]:
                    
                    max_y_in.delete(0, END)
                    max_y_in.insert(END, new_line_val)
                elif new_line_var == change_var_list[10]:
                    
                    min_z_in.delete(0, END)
                    min_z_in.insert(END, new_line_val)
                else:
                    
                    max_z_in.delete(0, END)
                    max_z_in.insert(END, new_line_val)
            elif new_line_var == 'export X_POS':
                new_line_val = line.split('=')[-1].strip()
                
                if new_line_val.isnumeric():
                    x_pos_box.current(0)
                else:
                    x_pos_box.current(1)
            elif new_line_var == 'export Y_POS':
                new_line_val = line.split('=')[-1].strip()
                
                if new_line_val.isnumeric():
                    y_pos_box.current(0)
                else:
                    y_pos_box.current(1)
            elif new_line_var == 'export Z_POS':
                new_line_val = line.split('=')[-1].strip()
                
                if new_line_val.isnumeric():
                    z_pos_box.current(0)
                else:
                    z_pos_box.current(1)
        auto_submit_button_left('<Button-1>', image_in_canvas)


def switch_gui_image():
    filename = select_files()
    if filename:
        os.execv(sys.argv[0], [sys.argv[0], filename])
    pass


def auto_submit_button_left(event, image_in_canvas):
    global help_image_window
    global auto_start_on_off

    submit_config_update = importlib.reload(pin_align_config)
    rtl = False
    ltr = False
    # A "minor" change has no impact that a visual aid would help in making that change.
    minor_entry_change = False

    config_x_cent = submit_config_update.X_CENTER
    config_y_cent = submit_config_update.Y_CENTER
    config_default_width = submit_config_update.DEFAULT_WIDTH
    config_default_height = submit_config_update.DEFAULT_HEIGHT
    config_x1_offset = submit_config_update.PIN_X1_OFFSET

    image_in_canvas.auto_crop_stop(
        y1_value_label, x1_value_label, x2_value_label, y2_value_label)

    ### LOOKING FOR CHANGES TO MIN VALUES ###
    if int(min_x_in.get()) != submit_config_update.MIN_X:
        change_config_file(config_file_path, 'MIN_X', str(min_x_in.get()))
        minor_entry_change = True
    if int(min_y_in.get()) != submit_config_update.MIN_Y:
        change_config_file(config_file_path, 'MIN_Y', str(min_y_in.get()))
        minor_entry_change = True
    if int(min_z_in.get()) != submit_config_update.MIN_Z:
        change_config_file(config_file_path, 'MIN_Z', str(min_z_in.get()))
        minor_entry_change = True
    ### LOOKING FOR CHANGES TO MAX VALUES ###
    if int(max_x_in.get()) != submit_config_update.MAX_X:
        change_config_file(config_file_path, 'MAX_X', str(max_x_in.get()))
        minor_entry_change = True
    if int(max_y_in.get()) != submit_config_update.MAX_Y:
        change_config_file(config_file_path, 'MAX_Y', str(max_y_in.get()))
        minor_entry_change = True
    if int(max_z_in.get()) != submit_config_update.MAX_Z:
        change_config_file(config_file_path, 'MAX_Z', str(max_z_in.get()))
        minor_entry_change = True
    ### LOOKING FOR CHANGES TO DEFAULT PIXELS PER MM ###
    if int(default_pixels_per_mm_in.get()) != submit_config_update.DEFAULT_PIXELS_PER_MM:
        change_config_file(
            config_file_path, 'DEFAULT_PIXELS_PER_MM', str(default_pixels_per_mm_in.get()))
        minor_entry_change = True
    ### LOOKING FOR CHANGES TO X, Y, Z POSITIVE DIRECTION ###
    if str(x_pos_in.get()) != str(submit_config_update.X_POS):
        change_config_file(config_file_path, 'X_POS',
                           str(x_pos_in.get()))
        minor_entry_change = True
        image_in_canvas.show_xyz_dir(
            x_pos_in.get(), y_pos_in.get(), z_pos_in.get(), True)
    if str(y_pos_in.get()) != str(submit_config_update.Y_POS):
        change_config_file(config_file_path, 'Y_POS',
                           str(y_pos_in.get()))
        minor_entry_change = True
        image_in_canvas.show_xyz_dir(
            x_pos_in.get(), y_pos_in.get(), z_pos_in.get(), True)
    if (z_pos_in.get()) != str(submit_config_update.Z_POS):
        change_config_file(config_file_path, 'Z_POS',
                           str(z_pos_in.get()))
        minor_entry_change = True
        image_in_canvas.show_xyz_dir(
            x_pos_in.get(), y_pos_in.get(), z_pos_in.get(), True)

    if minor_entry_change:
        convert_to_bash(config_file_path)
    if X_POS:
        # The cap is on the right and the pin goes to the left
        rtl = True
    else:
        ltr = True

    if rtl:
        if auto_start_on_off:
            clear_image_canvas(image_in_canvas)
            info_canvas_top.delete(help_image_window)
            auto_start_on_off = False
            pin_tip_button.bind("<Button-1>", lambda event,
                                arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 0))
            pin_body_button.bind("<Button-1>", lambda event,
                                 arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 1))
            pin_cap_button.bind("<Button-1>", lambda event,
                                arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 2))
            tilt_check_top_button.bind(
                "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 3))
            tilt_check_bottom_button.bind(
                "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 4))
            pin_check_top_button.bind("<Button-1>", lambda event,
                                      arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 5))
            pin_check_bottom_button.bind(
                "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 6))

            pin_tip_button.bind("<Button-3>", lambda event,
                                arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 0))
            pin_body_button.bind("<Button-3>", lambda event,
                                 arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 1))
            pin_cap_button.bind("<Button-3>", lambda event,
                                arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 2))
            tilt_check_top_button.bind(
                "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 3))
            tilt_check_bottom_button.bind(
                "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 4))
            pin_check_top_button.bind("<Button-3>", lambda event,
                                      arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 5))
            pin_check_bottom_button.bind(
                "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 6))

            pin_tip_button.config(bg='green')
            pin_body_button.config(bg='green')
            pin_cap_button.config(bg='green')
            tilt_check_top_button.config(bg='green')
            tilt_check_bottom_button.config(bg='green')
            pin_check_top_button.config(bg='green')
            pin_check_bottom_button.config(bg='green')

            X, Y = image_in_canvas.center_pin_image(
                int(x1_value_in.get()), int(y1_value_in.get()))
            if not X or not Y:
                messagebox.showerror(
                    'NO PIN', 'CANNOT FIND PIN TIP NEAR GREEN POINT, PLEASE TRY AGAIN!')
                auto_start_button_left(event, image_in_canvas)
                return
            change_config_file(
                config_file_path, 'X_CENTER', str(X))
            change_config_file(
                config_file_path, 'Y_CENTER', str(Y))
            A = int(x2_value_in.get())
            B = Y

            # X1 = X - int(pin_x1_offset_in.get())
            X1 = (X - int(pin_x1_offset_in.get())) + \
                (int(min_x_in.get()) * int(default_pixels_per_mm_in.get()))
            X2 = A + 5
            height = int(default_height_in.get())
            width = X2 - X1
            line = image_in_canvas.draw_new_line(X, Y, A, B)
            change_config_file(config_file_path, 'DEFAULT_HEIGHT', str(height))
            change_config_file(config_file_path, 'DEFAULT_WIDTH', str(width))
        elif (submit_config_update.X_CENTER != int(x_center_in.get()) or
              submit_config_update.Y_CENTER != int(y_center_in.get()) or
              submit_config_update.DEFAULT_WIDTH != int(default_width_in.get()) or
              submit_config_update.DEFAULT_HEIGHT != int(default_height_in.get()) or
              submit_config_update.PIN_X1_OFFSET != int(pin_x1_offset_in.get())):
            clear_image_canvas(image_in_canvas)
            X, Y = int(x_center_in.get()), int(y_center_in.get())
            height = int(default_height_in.get())

            # X1 = X - int(pin_x1_offset_in.get())
            X1 = (X - int(pin_x1_offset_in.get())) + \
                (int(min_x_in.get()) * int(default_pixels_per_mm_in.get()))
            X2 = X1 + int(default_width_in.get())
            width = X2 - X1
            line = image_in_canvas.draw_new_line(X1, Y, X2, Y)
            change_config_file(
                config_file_path, 'X_CENTER', str(x_center_in.get()))
            change_config_file(
                config_file_path, 'Y_CENTER', str(y_center_in.get()))
            change_config_file(config_file_path, 'DEFAULT_HEIGHT', str(height))
            change_config_file(config_file_path, 'DEFAULT_WIDTH', str(width))
        elif minor_entry_change:
            return
        else:
            messagebox.showwarning('NO CHANGES', 'NO CHANGES WERE DETECTED')
            return
        change_config_file(config_file_path, 'PIN_X1_OFFSET',
                           pin_x1_offset_in.get())
        Y1 = Y - (height // 2)
        Y2 = Y + (height // 2)

        change_config_file(config_file_path, 'DEFAULT_ROI_Y1', Y1)
        change_config_file(config_file_path, 'DEFAULT_ROI_Y2', Y2)

        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))

        big_box = image_in_canvas.create_big_box(X1, Y1, X2, Y2)
        change_config_file(config_file_path, 'BIG_BOX_X1', X1)
        change_config_file(config_file_path, 'BIG_BOX_X2', X2)
        change_config_file(config_file_path, 'BIG_BOX_Y1', Y1)
        change_config_file(config_file_path, 'BIG_BOX_Y2', Y2)

        small_box = image_in_canvas.create_small_box(X, Y)
        change_config_file(config_file_path, 'BOX_X_IN', X)
        change_config_file(config_file_path, 'BOX_Y_IN', Y)

        bbo = (X2 - X1) // 3

        Xt = X1 + bbo
        change_config_file(config_file_path, 'PIN_TIP_X1', X1)
        change_config_file(config_file_path, 'PIN_TIP_X2', Xt)

        Xb = Xt + bbo
        change_config_file(config_file_path, 'PIN_BODY_X1', Xt)
        change_config_file(config_file_path, 'PIN_BODY_X2', Xb)

        Xc = Xb
        change_config_file(config_file_path, 'PIN_BASE_X1', Xc)
        change_config_file(config_file_path, 'PIN_BASE_X2', X2)

        Y_offset = ((Y2 - Y1) // 2) - 50
        # X1 Tilt check
        X_tc = X2 - 50
        change_config_file(config_file_path, 'TILT_CHECK_X1', X_tc)
        change_config_file(config_file_path, 'TILT_CHECK_X2', X2)

        Y1t_tc = Y1 + 15
        Y2t_tc = Y1 + Y_offset
        change_config_file(config_file_path, 'TILT_CHECK_TOP_Y1', Y1t_tc)
        change_config_file(config_file_path, 'TILT_CHECK_TOP_Y2', Y2t_tc)

        Y1b_tc = Y2 - Y_offset
        Y2b_tc = Y2 - 15
        change_config_file(
            config_file_path, 'TILT_CHECK_BOTTOM_Y1', Y1b_tc)
        change_config_file(
            config_file_path, 'TILT_CHECK_BOTTOM_Y2', Y2b_tc)

        # Y top Pin check
        Yt_pc = Y1 + Y_offset
        change_config_file(config_file_path, 'PIN_CHECK_TOP_Y1', Y1)
        change_config_file(config_file_path, 'PIN_CHECK_TOP_Y2', Yt_pc)

        Yb_pc = Y2 - Y_offset
        change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y1', Yb_pc)
        change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y2', Y2)

        new_crop = image_in_canvas.get_image(X1, X2, Y1, Y2)
        current_crop_label.config(image=new_crop)
        current_crop_title.config(
            text='Current Crop', font=('helvetica', 14))
        convert_to_bash(config_file_path)
        update_entry_boxes()
    elif ltr:
        print("##### TODO #####")
    else:
        print('pass')


def donothing(button):
    print(f'##### {button} Working #####')
    pass


if __name__ == '__main__':
    root = tk.Tk()
    auto_start_on_off = False

    root.bind('<Motion>', motion)
    # Tool Bar is added to the canvas here to avoid formatting issues
    # Tool Bar code continues on line 413
    toolbar = tk.Frame(root)
    toolbar.pack(side="top", fill="x")
    # root_menu = window_menu_bar.Window_Menu(root)
    w = 1920
    h = 1050

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Pin Align configuration')

    ########################### Image Canvas ############################
    image_in_canvas = Image_Canvas(root)
    # root_menu = window_menu_bar.Window_Menu(root)
    ########################### Toolbar Canvas ############################
    menubar = Menu(root, relief='raised')

    filemenu = Menu(menubar, tearoff=1)
    menubar.add_cascade(label="File", menu=filemenu)

    filemenu.add_command(
        label="Save", command=lambda: convert_to_bash(config_file_path))
    filemenu.add_command(label="Save as...", command=save_config_as)
    filemenu.add_command(label="Change Image", command=switch_gui_image)
    filemenu.add_command(label="Change Configuration",
                         command=lambda: switch_gui_config(config_file_path))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    viewmenu = Menu(menubar, tearoff=1)
    menubar.add_cascade(label="View", menu=viewmenu)

    viewmenu.add_command(label="Refresh", command=update_entry_boxes)
    viewmenu.add_command(
        label="Manual", command=image_in_canvas.start_self_crop)
    viewmenu.add_command(
        label="Clear", command=lambda: clear_image_canvas(image_in_canvas))
    viewmenu.add_command(label="Zoom", command=lambda: donothing('zoom'))
    viewmenu.add_separator()

    bbmenu = Menu(viewmenu, tearoff=0)
    viewmenu.add_cascade(label='Big Box', menu=bbmenu)
    bbmenu.add_command(label="Edges", command=lambda: crop_button_right_click(
        "<Button-3>", image_in_canvas, 8))
    bbmenu.add_command(label="Outline", command=lambda: crop_button_left_click(
        "<Button-1>", image_in_canvas, 8))

    sbmenu = Menu(viewmenu, tearoff=0)
    viewmenu.add_cascade(label='Small Box', menu=sbmenu)
    sbmenu.add_command(label="Edges", command=lambda: crop_button_right_click(
        "<Button-3>", image_in_canvas, 7))
    sbmenu.add_command(label="Outline", command=lambda: crop_button_left_click(
        "<Button-1>", image_in_canvas, 7))

    helpmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpmenu)

    helpmenu.add_command(label="X,Y,Z Direction", command=lambda:
                         image_in_canvas.show_xyz_dir(x_pos_in.get(),
                                                      y_pos_in.get(),
                                                      z_pos_in.get(),
                                                      False))
    # helpmenu.add_command(label="Help Index",
    #                      command=lambda: donothing('help index'))
    helpmenu.add_command(label="About...", command=about_button)

    root.config(menu=menubar)

    ############################ Info Canvas Top ############################
    info_canvas_top = tk.Canvas(root, width=600, height=500,
                                border=1, relief="sunken")

    style = ttk.Style()
    # Makes all TK combo boxes read only with a white background.
    # Remove 'readonly' to allow user input in combo boxes
    # Remove 'white' to return to default background
    style.map('TCombobox', fieldbackground=[('readonly', 'white')])

    pin_x1_offset_label = tk.Label(root, text='Set X1 Offset')
    pin_x1_offset_label.config(font=('helvetica', 10))
    pin_x1_offset_in = tk.Entry(root, justify='center', width=15)
    pin_x1_offset_in.insert(END, str(PIN_X1_OFFSET))
    info_canvas_top.create_window(90, 315, window=pin_x1_offset_label)
    info_canvas_top.create_window(90, 335, window=pin_x1_offset_in)

    pixel_per_mm_label = tk.Label(root, text='Set Pixel per MM')
    pixel_per_mm_label.config(font=('helvetica', 10))
    default_pixels_per_mm_in = tk.Entry(root, justify='center', width=15)
    default_pixels_per_mm_in.insert(END, str(DEFAULT_PIXELS_PER_MM))
    info_canvas_top.create_window(310, 315, window=pixel_per_mm_label)
    info_canvas_top.create_window(310, 335, window=default_pixels_per_mm_in)

    default_width_label = tk.Label(root, text='Total Width')
    default_width_label.config(font=('helvetica', 10))
    default_width_in = tk.Entry(root, justify='center', width=15)
    default_width_in.insert(END, str(DEFAULT_WIDTH))
    info_canvas_top.create_window(520, 315, window=default_width_label)
    info_canvas_top.create_window(520, 335, window=default_width_in)

    x_center_label = tk.Label(root, text='X Center Point')
    x_center_label.config(font=('helvetica', 10))
    x_center_in = tk.Entry(root, justify='center', width=15)
    x_center_in.insert(END, str(X_CENTER))
    info_canvas_top.create_window(90, 390, window=x_center_label)
    info_canvas_top.create_window(90, 410, window=x_center_in)

    y_center_label = tk.Label(root, text='Y Center Point')
    y_center_label.config(font=('helvetica', 10))
    y_center_in = tk.Entry(root, justify='center', width=15)
    y_center_in.insert(END, str(Y_CENTER))
    info_canvas_top.create_window(310, 390, window=y_center_label)
    info_canvas_top.create_window(310, 410, window=y_center_in)

    default_height_label = tk.Label(root, text='ROI Height')
    default_height_label.config(font=('helvetica', 10))
    default_height_in = tk.Entry(root, justify='center', width=15)
    default_height_in.insert(END, str(DEFAULT_HEIGHT))
    info_canvas_top.create_window(520, 390, window=default_height_label)
    info_canvas_top.create_window(520, 410, window=default_height_in)

    x_pos_label = tk.Label(root, text='X Positive')
    x_pos_label.config(font=('helvetica', 10))
    x_pos_in = tk.StringVar()
    x_pos_box = ttk.Combobox(
        root, width=15, height=10, textvariable=x_pos_in, justify='center')
    x_pos_box['values'] = ['True', 'False']
    x_pos_box['state'] = 'readonly'
    x_pos_box.set(str(X_POS))
    info_canvas_top.create_window(90, 465, window=x_pos_label)
    info_canvas_top.create_window(90, 485, window=x_pos_box)

    y_pos_label = tk.Label(root, text='Y Positive')
    y_pos_label.config(font=('helvetica', 10))
    y_pos_in = tk.StringVar()
    y_pos_box = ttk.Combobox(
        root, width=15, height=10, textvariable=y_pos_in, justify='center')
    y_pos_box['values'] = ['True', 'False']
    y_pos_box['state'] = 'readonly'
    y_pos_box.set(str(Y_POS))
    info_canvas_top.create_window(310, 465, window=y_pos_label)
    info_canvas_top.create_window(310, 485, window=y_pos_box)

    z_pos_label = tk.Label(root, text='Z Positive')
    z_pos_label.config(font=('helvetica', 10))
    z_pos_in = tk.StringVar()
    z_pos_box = ttk.Combobox(
        root, width=15, height=10, textvariable=z_pos_in, justify='center')
    z_pos_box['values'] = ['True', 'False']
    z_pos_box['state'] = 'readonly'
    z_pos_box.set(str(Z_POS))
    info_canvas_top.create_window(520, 465, window=z_pos_label)
    info_canvas_top.create_window(520, 485, window=z_pos_box)

    current_crop_title = tk.Label(root, text='Current Crop')
    current_crop_title.config(font=('helvetica', 14))
    info_canvas_top.create_window(310, 25, window=current_crop_title)

    whole_crop = image_in_canvas.get_image(
        BIG_BOX_X1, BIG_BOX_X2, BIG_BOX_Y1, BIG_BOX_Y2)
    current_crop_label = tk.Label(root)
    info_canvas_top.create_window(310, 160, window=current_crop_label)
    current_crop_label.config(image=whole_crop)
    info_canvas_top.pack(side="top", fill="both", expand=True)
    info_canvas_top.create_line(0, 295, 600, 295, fill='black', width=1)

    ############################ Min Labels & Entry ############################

    min_x_label = tk.Label(root, text='Min X')
    min_x_label.config(font=('helvetica', 14))
    min_x_in = tk.Entry(root, justify='center', width=10)
    min_x_in.insert(END, str(MIN_X))
    info_canvas_top.create_window(55, 55, window=min_x_label)
    info_canvas_top.create_window(55, 75, window=min_x_in)

    min_y_label = tk.Label(root, text='Min Y')
    min_y_label.config(font=('helvetica', 14))
    min_y_in = tk.Entry(root, justify='center', width=10)
    min_y_in.insert(END, str(MIN_Y))
    info_canvas_top.create_window(55, 135, window=min_y_label)
    info_canvas_top.create_window(55, 155, window=min_y_in)

    min_z_label = tk.Label(root, text='Min Z')
    min_z_label.config(font=('helvetica', 14))
    min_z_in = tk.Entry(root, justify='center', width=10)
    min_z_in.insert(END, str(MIN_Z))
    info_canvas_top.create_window(55, 225, window=min_z_label)
    info_canvas_top.create_window(55, 245, window=min_z_in)

    ############################ Max Labels & Entry ############################

    max_x_label = tk.Label(root, text='Max X')
    max_x_label.config(font=('helvetica', 14))
    max_x_in = tk.Entry(root, justify='center', width=10)
    max_x_in.insert(END, str(MAX_X))
    info_canvas_top.create_window(555, 55, window=max_x_label)
    info_canvas_top.create_window(555, 75, window=max_x_in)

    max_y_label = tk.Label(root, text='Max Y')
    max_y_label.config(font=('helvetica', 14))
    max_y_in = tk.Entry(root, justify='center', width=10)
    max_y_in.insert(END, str(MAX_Y))
    info_canvas_top.create_window(555, 135, window=max_y_label)
    info_canvas_top.create_window(555, 155, window=max_y_in)

    max_z_label = tk.Label(root, text='Max Z')
    max_z_label.config(font=('helvetica', 14))
    max_z_in = tk.Entry(root, justify='center', width=10)
    max_z_in.insert(END, str(MAX_Z))
    info_canvas_top.create_window(555, 225, window=max_z_label)
    info_canvas_top.create_window(555, 245, window=max_z_in)

    ############################ Info Canvas Bottom ############################
    info_canvas_bottom = tk.Canvas(root, width=600, height=500,
                                   border=1, relief="sunken")

    info_canvas_bottom.pack(side="bottom", fill="both", expand=True)

    info_canvas_bottom.create_line(0, 250, 600, 250, fill='black', width=1)

    info_bottom_title = tk.Label(text='Select Crop Position')
    info_bottom_title.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(300, 15, window=info_bottom_title)

    auto_start_button = tk.Button(
        text='Start', bg='green', fg='white', font=10)

    auto_submit_button = tk.Button(
        text='Submit', bg='green', fg='white', font=10)

    auto_start_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_start_button_left(event, image_in_canvas))
    auto_submit_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_submit_button_left(event, image_in_canvas))

    quit_button = tk.Button(
        text='Quit', command=lambda: root.destroy(), bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(105, 475, window=auto_start_button)
    info_canvas_bottom.create_window(305, 475, window=auto_submit_button)
    info_canvas_bottom.create_window(505, 475, window=quit_button)

    pin_tip_button = tk.Button(text='Pin Tip', bg='green', fg='white', font=10)
    pin_body_button = tk.Button(
        text='Pin Body', bg='green', fg='white', font=10)
    pin_cap_button = tk.Button(text='Pin Cap', bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(105, 75, window=pin_tip_button)
    info_canvas_bottom.create_window(305, 75, window=pin_body_button)
    info_canvas_bottom.create_window(505, 75, window=pin_cap_button)

    tilt_check_top_button = tk.Button(
        text='Tilt Check Top', bg='green', fg='white', font=10)
    tilt_check_bottom_button = tk.Button(
        text='Tilt Check Bottom', bg='green', fg='white', font=10)
    pin_check_top_button = tk.Button(
        text='Pin Check Top', bg='green', fg='white', font=10)
    pin_check_bottom_button = tk.Button(
        text='Pin Check Bottom', bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(200, 145, window=pin_check_top_button)
    info_canvas_bottom.create_window(200, 185, window=pin_check_bottom_button)
    info_canvas_bottom.create_window(430, 145, window=tilt_check_top_button)
    info_canvas_bottom.create_window(430, 185, window=tilt_check_bottom_button)

    pin_tip_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-1>", lambda event,
                         arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-1>", lambda event,
                              arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left_click(event, image_in_canvas, 6))

    pin_tip_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-3>", lambda event,
                         arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-3>", lambda event,
                              arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right_click(event, image_in_canvas, 6))

    ############################ Y1 / X1 Settings ############################
    y1_value_label = tk.Label(root, text='Y1')
    y1_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(450, 310, window=y1_value_label)

    x1_value_label = tk.Label(root, text='X1')
    x1_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(150, 310, window=x1_value_label)

    y1_value_in = tk.Entry(root, justify='center')
    y1_value_in.insert(END, '0')

    info_canvas_bottom.create_window(450, 345, window=y1_value_in)
    x1_value_in = tk.Entry(root, justify='center')
    x1_value_in.insert(END, '0')

    info_canvas_bottom.create_window(150, 345, window=x1_value_in)

    ############################ X2 / Y2 Settings ############################
    x2_value_label = tk.Label(root, text='X2')
    x2_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(150, 395, window=x2_value_label)

    y2_value_label = tk.Label(root, text='Y2')
    y2_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(450, 395, window=y2_value_label)

    x2_value_in = tk.Entry(root, justify='center')
    x2_value_in.insert(END, '0')

    info_canvas_bottom.create_window(150, 420, window=x2_value_in)

    y2_value_in = tk.Entry(root, justify='center')
    y2_value_in.insert(END, '0')

    info_canvas_bottom.create_window(450, 420, window=y2_value_in)

    ############################ Misc Settings ############################

    mouse_pos = Label(root, text='0')
    info_canvas_bottom.create_window(310, 275, window=mouse_pos)
    root.mainloop()
