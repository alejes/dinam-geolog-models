import numpy as np
import threading

from lib import filetools, texttools
from tkinter import *
from tkinter import filedialog, ttk
from window.frames.paint import Paint
from worker import *

import os


class Welcome(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.task_config = {}
        self.ready_button = None
        self.create_select_menu()

    def __save_load_file(self, lmbd, btn, name):
        def inner():
            result = lmbd()
            if result:
                btn.value = result.name
                btn.config(text=texttools.more(os.path.basename(btn.value), 15))
                self.task_config[name] = btn.value

        return inner

    def __switch_to_paint(self, buttons):
        def inner():
            for b in buttons:
                b.config(state='disabled')
            progress_grid = Label(self, text="Waiting results: ")
            progress_grid.grid(row=4, column=0, padx=6)

            pb = ttk.Progressbar(self, length=300, mode='determinate')

            pb.grid(row=4, columnspan=4, padx=6)
            pb.start()

            proc = run_paint(self.task_config)

            def waiter():
                while proc.is_alive():
                    time.sleep(0.1)

                self.master.withdraw()
                self.master = Toplevel(self)
                self.master.geometry("850x500+300+300")
                data1 = np.array(np.random.random((400, 500)) * 255, dtype=int)
                data2 = np.array(np.random.random((400, 500)) * 255, dtype=int)
                Paint(self.master, data1, data2)

            threading.Thread(target=waiter).start()

        return inner

    def create_select_menu(self):
        self.master.title("Process-Based geologic models")
        self.pack(fill=BOTH, expand=1)

        image_grid = Label(self, text="Image grid: ")
        image_grid.grid(row=0, column=0, padx=6)

        image_grid_btn = Button(self, text="Load image", width=20)
        image_grid_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select file",
                                                                       filetypes=(("jpeg files", filetools.get_file_types("jpeg")),
                                                                                    ("all files", "*.*"))), image_grid_btn, "image_grid"))
        image_grid_btn.grid(row=0, column=1)

        well_rock_btn = []
        well_porosity_btn = []

        for id, name in enumerate(['A', 'B']):
            label = Label(self, text="Well A: ")
            label.grid(row=1 + id, column=0, padx=6)
            rock_btn = Button(self, text="Load rock type", width=20)
            rock_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select rock type file",
                                                                        filetypes=(("data files",filetools.get_file_types("data")),
                                                                                    ("all files","*.*"))),rock_btn, "rock_" + name))
            rock_btn.grid(row=1 + id, column=1)
            well_rock_btn.append(rock_btn)

            porosity_btn = Button(self, text="Load porosity", width=20)
            porosity_btn.config(command=self.__save_load_file(lambda: filedialog.askopenfile(title="Select porosity file",
                                                                        filetypes=(("data files",filetools.get_file_types("data")),
                                                                                       ("all files","*.*"))),porosity_btn, "porisity_" + name))
            porosity_btn.grid(row=1 + id, column=2)
            well_porosity_btn.append(porosity_btn)

        calculate_btn = Button(self, text="Predict ", width=20)
        calculate_btn.config(command=self.__switch_to_paint(well_rock_btn + well_porosity_btn + [calculate_btn, image_grid_btn]))
        calculate_btn.grid(row=3, column=1)
