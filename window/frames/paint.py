from tkinter import *


class Paint(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_select_menu()


    def create_select_menu(self):
        self.master.title("Paint results")
        self.pack(fill=BOTH, expand=1)

        image_grid = Label(self, text="Image *(D(*edogrid: ")
        image_grid.grid(row=0, column=0, padx=6)
