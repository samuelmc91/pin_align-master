#!/usr/bin/python3
import tkinter as tk
import os
import sys
from tkinter import *


if __name__ == '__main__':
    root = tk.Tk()
    w = 1920
    h = 1050

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Pin Align configuration')

    screen_canvas = Canvas(root, width=1280, height=1024, border=1, relief="sunken")
    screen_canvas.create_rectangle(1140, 915, 1270, 1040, fill='white')
    screen_canvas.pack(side="left", fill="both", expand=False)

    # If X_POS:
    screen_canvas.create_line(1200, 980, 1150, 980, arrow=tk.LAST, fill='red')  # X Arrow 1
    # else:
    screen_canvas.create_line(1210, 980, 1260, 980, arrow=tk.LAST, fill='red')  # X Arrow 2
    
    # if Y_POS:
    screen_canvas.create_line(1205, 975, 1205, 925, arrow=tk.LAST, fill='green')  # Y Arrow 1
    # else:
    screen_canvas.create_line(1205, 980, 1205, 1030, arrow=tk.LAST, fill='green')  # Y Arrow 2

    screen_canvas.create_oval(1200, 975, 1210, 985, fill='black')

    root.mainloop()