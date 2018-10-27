from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class Paint(Frame):
    def __init__(self, master, rockType, porosity):
        Frame.__init__(self, master, width=500, height=400)
        self.map_binary = lambda x: 0 if x <= 127 else 1
        self.map_binary = np.vectorize(self.map_binary)
        self.rockType = self.map_binary(rockType)
        print(self.rockType)
        self.porosity = porosity
        self.grid()
        self.master.title("Paint results")
        self.pack()
        self.draw_rock_type()


    def draw_rock_type(self):
        image_grid = Label(self, text="Rock Type: ")
        image_grid.place(x=0, y=0)

        self.canvas = Canvas(self, width=self.rockType.shape[1] + 100, height=self.rockType.shape[0])
        self.canvas.place(x=100, y=0)
        self.im = Image.frombytes('L', (self.rockType.shape[1], self.rockType.shape[0]), self.rockType.astype('b').tostring())
        # self.im = Image.fromarray(self.rockType)
        print(self.im.mode)
        lut = []
        lut.extend([255, 56, 20]) #ff3814
        lut.extend([1, 159, 103]) #ff3814
        self.im.putpalette(lut)
        print(self.im.mode)
        print('pallete', self.im.getpalette())
        print(self.im.getcolors())
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.master.update()
        print(44455567879)
