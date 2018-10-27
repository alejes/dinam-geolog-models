from lib import filetools, texttools
from tkinter import *
from tkinter import filedialog

import os


class Paint(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_select_menu()

    def __save_load_file(self, lmbd, btn):
        def inner():
            result = lmbd()
            if result:
                btn.load_file = result.name
                btn.config(text=texttools.more(os.path.basename(btn.load_file), 15))

        return inner


    def create_select_menu(self):
        self.master.title("Paint results")
        self.pack(fill=BOTH, expand=1)

        image_grid = Label(self, text="Image *(D(*edogrid: ")
        image_grid.grid(row=0, column=0, padx=6)
