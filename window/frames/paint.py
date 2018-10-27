from tkinter import *
from tkinter import ttk


class Paint(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_select_menu()

    def create_select_menu(self):
        self.master.title("Paint results")

        progress_grid = Label(self, text="Waiting results: ")
        progress_grid.grid(row=0, column=0, padx=6)

        pb = ttk.Progressbar(self, length=300, mode='determinate')
        self.pack()
        pb.grid(row=0, column=1, padx=6)
        # self.pack(fill=BOTH, expand=1)
        pb.start(25)
