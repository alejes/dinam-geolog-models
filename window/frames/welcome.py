from lib import filetools, texttools
from tkinter import *
from tkinter import filedialog

import os


class Welcome(Frame):
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
        self.master.title("Process-Based geologic models")
        self.pack(fill=BOTH, expand=1)

        image_grid = Label(self, text="Image grid: ")
        image_grid.grid(row=0, column=0, padx=6)

        image_grid_btn = Button(self, text="Load image", width=20)
        image_grid_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select file",
                                                                       filetypes=(("jpeg files", filetools.get_file_types("jpeg")),
                                                                                    ("all files", "*.*"))), image_grid_btn))
        image_grid_btn.grid(row=0, column=1)

        well_rock_btn = []
        well_porosity_btn = []

        for id, name in enumerate(['A', 'B']):
            label = Label(self, text="Well A: ")
            label.grid(row=1 + id, column=0, padx=6)
            rock_btn = Button(self, text="Load rock type", width=20)
            rock_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select rock type file",
                                                                        filetypes=(("data files",filetools.get_file_types("data")),
                                                                                    ("all files","*.*"))),rock_btn))
            rock_btn.grid(row=1 + id, column=1)
            well_rock_btn.append(rock_btn)

            porosity_btn = Button(self, text="Load porosity", width=20)
            porosity_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select porosity file",
                                                                        filetypes=(("data files",filetools.get_file_types("data")),
                                                                                       ("all files","*.*"))),
                                                                        porosity_btn))
            porosity_btn.grid(row=1 + id, column=2)
            well_porosity_btn.append(porosity_btn)

        calculate_btn = Button(self, text="Predict ", width=20)
        calculate_btn.grid(row=3, column=1)
