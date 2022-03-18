import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import importlib
import pin_align_auto_config
# from pin_align_auto_config import *

class Window_Menu():
    def __init__(self, root):
        self.root = root
        self.menubar = Menu(self.root, relief='sunken')

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="Change Image", command=self.donothing)
        self.filemenu.add_command(label="Change Configuration", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(label="Save as...", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        
        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

        self.viewmenu.add_command(label="Refresh", command=pin_align_auto_config.update_entry_boxes)
        self.viewmenu.add_separator()
        self.viewmenu.add_command(label="Manual", command=self.donothing)
        self.viewmenu.add_command(label="Clear", command=self.donothing)
        self.viewmenu.add_command(label="Small Box", command=self.donothing)
        self.viewmenu.add_command(label="Big Box", command=self.donothing)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.donothing)

        self.root.config(menu=self.menubar)

    # def update_entry_boxes(self):
    #     update_config = importlib.reload(pin_align_auto_config.pin_align_config)

    #     pin_align_auto_config.pin_x1_offset_in.delete(0, END)
    #     pin_align_auto_config.pin_x1_offset_in.insert(END, update_config.PIN_X1_OFFSET)
    #     pin_align_auto_config.default_pixels_per_mm_in.delete(0, END)
    #     pin_align_auto_config.default_pixels_per_mm_in.insert(END, update_config.DEFAULT_PIXELS_PER_MM)
    #     pin_align_auto_config.default_width_in.delete(0, END)
    #     pin_align_auto_config.default_width_in.insert(END, update_config.DEFAULT_WIDTH)
    #     pin_align_auto_config.x_center_in.delete(0, END)
    #     pin_align_auto_config.x_center_in.insert(END, update_config.X_CENTER)
    #     pin_align_auto_config.y_center_in.delete(0, END)
    #     pin_align_auto_config.y_center_in.insert(END, update_config.Y_CENTER)
    #     pin_align_auto_config.default_height_in.delete(0, END)
    #     pin_align_auto_config.default_height_in.insert(END, update_config.DEFAULT_HEIGHT)
    #     pin_align_auto_config.min_x_in.delete(0, END)
    #     pin_align_auto_config.min_x_in.insert(END, update_config.MIN_X)
    #     pin_align_auto_config.min_y_in.delete(0, END)
    #     pin_align_auto_config.min_y_in.insert(END, update_config.MIN_Y)
    #     pin_align_auto_config.min_z_in.delete(0, END)
    #     pin_align_auto_config.min_z_in.insert(END, update_config.MIN_Z)
    #     pin_align_auto_config.max_x_in.delete(0, END)
    #     pin_align_auto_config.max_x_in.insert(END, update_config.MAX_X)
    #     pin_align_auto_config.max_y_in.delete(0, END)
    #     pin_align_auto_config.max_y_in.insert(END, update_config.MAX_Y)
    #     pin_align_auto_config.max_z_in.delete(0, END)
    #     pin_align_auto_config.max_z_in.insert(END, update_config.MAX_Z)
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

if __name__ == '__main__':
    root = tk.Tk()
    root_menu = Window_Menu(root)
    w = 1920
    h = 1050

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Pin Align configuration')
    root.mainloop()