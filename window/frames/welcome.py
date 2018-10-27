import threading
from functools import wraps

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
        self.create_select_menu()

    @staticmethod
    def __save_load_file(lmbd, btn):
        def inner():
            result = lmbd()
            if result:
                btn.load_file = result.name
                btn.config(text=texttools.more(os.path.basename(btn.load_file), 15))

        return inner

    def __switch_to_paint(self, buttons):
        def inner():
            for b in buttons:
                b.config(state='disabled')
            progress_grid = Label(self, text="Waiting results: ")
            progress_grid.grid(row=4, column=0, padx=6)

            pb = ttk.Progressbar(self, length=300, mode='determinate')
            # self.pack()
            # self.pack(fill=BOTH, expand=1)

            pb.grid(row=4, columnspan=4, padx=6)
            pb.start()

            proc = run_paint()
            def waiter():
                while proc.is_alive():
                    time.sleep(0.1)

                self.master.withdraw()
                self.master = Toplevel(self)
                self.master.geometry("850x500+300+300")
                myGUI = Paint(self.master)

            threading.Thread(target=waiter).start()
            # proc.join()

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
        calculate_btn.config(command=self.__switch_to_paint(well_rock_btn + well_porosity_btn + [calculate_btn, image_grid_btn]))
        calculate_btn.grid(row=3, column=1)
