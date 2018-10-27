from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class Paint(Frame):
    def __init__(self, master, rockType, porosity):
        Frame.__init__(self, master, width=max([rockType.shape[1], porosity.shape[1], 500])+300, height=max([rockType.shape[0], porosity.shape[0], 400]))
        self.map_binary = lambda x: 2 if x == 255 else (0 if x <= 127 else 1)
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

        self.canvas = Canvas(self, width=self.rockType.shape[1]+300, height=self.rockType.shape[0])
        self.canvas.place(x=100, y=0)
        self.im = Image.frombytes('L', (self.rockType.shape[1], self.rockType.shape[0]), self.rockType.astype('b').tostring())
        # self.im = Image.fromarray(self.rockType)
        # print(self.im.mode)
        lut = []
        lut.extend([255, 56, 20]) #ff3814
        lut.extend([1, 159, 103]) #019f67
        lut.extend([0, 0, 0])  # black
        self.im.putpalette(lut)
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.canvas.create_text(600, 150, text="Legend:",justify=CENTER, font="Verdana 20")
        self.canvas.create_text(600, 190, text="sandstone:", justify=LEFT, font="Verdana 14")
        self.canvas.create_text(600, 210, text="shale:", justify=LEFT, font="Verdana 14")
        self.canvas.create_oval(680, 190, 680, 190, width=15, outline="#ff3814")
        self.canvas.create_oval(680, 210, 680, 210, width=15, outline="#019f67")
        self.master.update()
        print(44455567879)
