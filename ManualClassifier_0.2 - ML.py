# Standard libraries
import ast
import datetime
import math
import importlib
import json
import os
import re
import sys
import threading
import time
import tkinter as tk

from datetime import date
from multiprocessing.sharedctypes import Value
from idlelib.tooltip import Hovertip
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# Third party libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import win32com.client as win32
from PIL import Image, ImageTk
import traceback

# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)
# Personal libraries

import sys


import sys
sys.path.append(str(Path.cwd().parent))

from utils import image_processing

import importlib
importlib.reload(image_processing)

background_color = (0.98, 0.98, 0.98)  # gray background
accent_color = (0.02, 0.38, 0.71)  # blue accent


features_path = r'E:\1C Cursos\Data Science Part Time - The Bridge\DS\Proyecto\data\fotocasa\features.json'
with open (features_path) as keys:
    params = json.load(keys)


TODAY = date.today().strftime("%Y-%m-%d")
################## TKINTER FUNCTIONS ##################
def entry_field(frame, label_text: str, init_value, row: int, column : int = 0):
    """Creates a label and a entry field.
    Returns StringVar that holds the value.
    Which has to be accesed as val.get()"""

    # Define val
    value = tk.StringVar()
    value.set(init_value)

    if label_text != None:
        # Define label
        label = ttk.Label(frame, text=label_text, justify=tk.LEFT)
        label.grid(row=row, column=column, padx=5, pady=5, sticky="w")

    # Define entry
    entry = ttk.Entry(frame, textvariable=value, width="30")
    entry.grid(row=row, column=column+1, padx=5, pady=5)
    return value


def checkbutton(frame, label_text: str, init_value, onvalue, offavlue, row: int, column : int):
    """Creates a Checkbutton.
    Returns StringVar that holds the value.
    Which has to be accesed as val.get()"""

    # Define val
    value = tk.StringVar()
    value.set(init_value)

    # Define Checkbutton
    checkbutton = ttk.Checkbutton(frame, text=label_text, variable=value, onvalue=onvalue, offvalue=offavlue)
    checkbutton.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
    return value


def optionmenu(frame, values : list, init_value, row: int, column : int):
    """Creates an OptionMenu.
    Returns StringVar that holds the value.
    Which has to be accesed as val.get()"""

    # Define val
    value = tk.StringVar()
    value.set(init_value)

    # Define OptionMenu
    optionmenu = ttk.OptionMenu(frame, value, *values)
    optionmenu.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
    return value


def dynamic_label(frame, text, row, column):
    label = ttk.Label(frame, text=text, justify=tk.LEFT)
    label.grid(row=row, column=column, padx=5, pady=5, sticky=tk.EW)


################## DATA PROCESSING ##################
def set_value_if_null(val, default_null):
    val = default_null if val == None else val
    return val

def rename_img():
    global img2
    # del img2
    global image_base_name
    # Find what params are to be set
    current_features = []
    print(values)
    for feature_full_name, value in values.items():
        value['value'] = value['btn'].get()
        # print(value['btn'])
        # print(value['value'])
        if value['value'] == '1':
            current_features.append(feature_full_name)
    # print(current_features)
    # Rename file
    image_dir = image_path.parent
    old_filename = image_base_name
    if len(current_features)>0:
        str_features = "__"+"__".join(current_features)+'_.jpg'
    else:
        str_features = '.jpg'

    new_filename = old_filename + str_features
    new_path = Path(image_dir, new_filename)
    image_path.rename(new_path)
    get_row(1)

def filename_to_dict(image_path):
    global image_base_name
    image_filename_list = image_path.stem.split('__')
    image_base_name = image_filename_list[0]
    image_params = image_filename_list[1:]
    image_params_dict = {}
    for p in image_params:
        p = p.split('_')
        image_params_dict[p[0]] = p[1]
    return image_params_dict


def get_row(increase):
    global img_num
    img_num += increase
    global values
    global label_names
    global feature_full_name
    global image_path
    image_path = filepaths[img_num]
    values = {}
    label_names = {}

    image_params_dict = filename_to_dict(image_path)
    print('*********************************************')
    # print(image_path, image_params_dict, type(image_params_dict))
    print(image_path)

    for col, (param_type, param_values) in enumerate(params.items()):
        label_names[param_type] = tk.Label(checkbuttons_frame, text=param_type)
        label_names[param_type].grid(row=0, column=col)
        for row, feature_name in enumerate(param_values):
            row += 1
            feature_full_name = f'{param_type}_{feature_name}'
            val = 0
            if image_params_dict.get(param_type) == feature_name:
                val = 1
            
            print(param_type, feature_name, val)
            values[feature_full_name] = {'value':val}
            values[feature_full_name]['btn'] = checkbutton(checkbuttons_frame, feature_name, val, 1, 0, row, col)
    # print(img_num, increase)
    # print(filepaths[img_num])

    # Show image
    global image
    global img2
    global label

    img0 = image_processing.process_img(image_path, (800, 800))

    # img0 = Image.open(image_path)
    # img0.thumbnail((1920, 1080))
    img2=ImageTk.PhotoImage(img0)


    label.configure(image=img2)
    label.image=img2
    root.update_idletasks()
    print('--------------------------------------------------')
    # image = Image.open(image_path)


##### Initialize list of images and get last image not processed
base_folder = Path(r'E:\1C Cursos\Data Science Part Time - The Bridge\DS\Proyecto\data\fotocasa\AUTO')
folder_paths = [Path(base_folder, f) for f in os.listdir(base_folder) if os.path.isdir(Path(base_folder, f))]
filepaths = [Path(base_folder, folder_path, f) for folder_path in folder_paths  for f in os.listdir(Path(base_folder, folder_path)) if os.path.isfile(Path(base_folder, folder_path, f))]
reversed_filepaths = filepaths.copy()
reversed_filepaths.reverse()
img_num = 0
for reversed_row, filepath in enumerate(reversed_filepaths):
    if 'quality' in filepath.name:
        img_num = len(filepaths) - reversed_row-1
        # print(reversed_row, filepath)
        # print(filepaths[img_num])
        break
print(img_num)
##### End initialization

""" Crear ventana en tkinter """
theme_type = "light"
root = tk.Tk()
root.title("Manual Classifier 0.1")
root.geometry("800x800")
root.tk.call("source", r"sun-valley-ttk-theme-master\sun-valley.tcl")
root.tk.call("set_theme", "light")

""" Crear menu """
menu_frame = ttk.Frame(root)
menu_frame.pack(side=tk.TOP, fill=tk.X)
menu = tk.Menu(menu_frame)
root.config(menu=menu)
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Inicio", menu=submenu)
submenu.add_command(label="Opción 1")
submenu.add_separator()
submenu.add_command(label="Opción")

""" Crear ventana inicial """
main_frame = ttk.Frame(root)
main_frame.pack(side=tk.TOP, padx=5, pady=5)

data_frame = ttk.Frame(main_frame)
data_frame.pack(side=tk.TOP, padx=5, pady=5)
# data_frame.place(x=20, y=20)

nav_frame = ttk.Frame(data_frame)
nav_frame.pack(side=tk.TOP, padx=5, pady=5)
btn_frame = ttk.Frame(data_frame)
btn_frame.pack(side=tk.TOP, padx=5, pady=5)

btn_left = ttk.Button(nav_frame, text = '◀', command=lambda : get_row(increase = -1))
btn_rename = ttk.Button(nav_frame, text = 'Rename', command=rename_img)
btn_right = ttk.Button(nav_frame, text = '▶', command=lambda : get_row(increase = 1))
btn_left.grid(row=0, column=0, sticky=tk.W, pady=5)
btn_rename.grid(row=0, column=1, sticky=tk.E, pady=5)
btn_right.grid(row=0, column=2, sticky=tk.E, pady=5)

# Checkbuttons
checkbuttons_frame = ttk.Frame(btn_frame)
checkbuttons_frame.grid(row=9, column=1, sticky=tk.EW)
#Create a Label widget

image_frame = ttk.Frame(main_frame)
image_frame.pack(side=tk.TOP, padx=5, pady=5)
# image_frame.place(x=200, y=20)
img1=ImageTk.PhotoImage(Image.open(filepaths[img_num]))
label = tk.Label(image_frame, image=img1)
label.pack()

root.mainloop()
