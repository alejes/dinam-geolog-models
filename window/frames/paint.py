from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class Paint(Frame):
    def __init__(self, master, rockType, porosity):
        Frame.__init__(self, master, width=max([rockType.shape[1], porosity.shape[1], 500])+300, height=max([rockType.shape[0] + porosity.shape[0], 400]))
        print(rockType)
        self.map_binary = lambda x: 2 if x == 255 else (0 if x <= 127 else 1)
        self.map_binary = np.vectorize(self.map_binary)
        self.rockType = self.map_binary(rockType)
        print(self.rockType)
        self.porosity = porosity
        self.grid()
        self.master.title("Paint results")
        self.pack()
        self.draw_rock_type()
        self.draw_porosity(self.rockType.shape[0] + 25)

    def draw_rock_type(self):
        image_grid = Label(self, text="Rock Type: ")
        image_grid.place(x=0, y=0)

        self.canvas = Canvas(self, width=self.rockType.shape[1]+300, height=self.rockType.shape[0])
        self.canvas.place(x=100, y=0)
        self.im = Image.frombytes('L', (self.rockType.shape[1], self.rockType.shape[0]), self.rockType.astype('b').tostring())
        # self.im = Image.open("porosity_4.png")
        # self.im = Image.fromarray(self.rockType)
        print(self.im.mode)
        lut = []
        lut.extend([255, 56, 20]) #ff3814
        lut.extend([1, 159, 103]) #019f67
        lut.extend([0, 0, 0])  # black
        self.im.putpalette(lut)
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.canvas.create_text(self.rockType.shape[1]+60, 150, text="Legend:",justify=CENTER, font="Verdana 20")
        self.canvas.create_text(self.rockType.shape[1]+60, 190, text="sandstone:", justify=LEFT, font="Verdana 14")
        self.canvas.create_text(self.rockType.shape[1]+60, 210, text="shale:", justify=LEFT, font="Verdana 14")
        self.canvas.create_oval(self.rockType.shape[1]+130, 190, self.rockType.shape[1]+130, 190, width=15, outline="#ff3814")
        self.canvas.create_oval(self.rockType.shape[1]+130, 210, self.rockType.shape[1]+130, 210, width=15, outline="#019f67")
        self.master.update()

    def draw_porosity(self, start):
        image_grid = Label(self, text="Porosity: ")
        image_grid.place(x=0, y=start)

        self.canvasPorosity = Canvas(self, width=self.porosity.shape[1] + 300, height=self.porosity.shape[0])
        self.canvasPorosity.place(x=100, y=start)

        self.imPorosity = Image.open("porosity_4.png")
        # self.imPorosity = Image.frombytes('L', (self.porosity.shape[1], self.porosity.shape[0]),
        #                           self.porosity.astype('b').tostring())
        # self.im = Image.fromarray(self.rockType)
        # print(self.im.mode)
        # lut = []
        #
        # def to_hex(d):
        #     z=hex(d)[2:]
        #     if len(z) == 1:
        #         z = '0' + z
        #     return z
        #
        # for g in range(0, 254):
        #     lut.extend([100, g, 100])
        #
        # lut.extend([255, 255, 255])
        # self.imPorosity.putpalette(lut)
        self.photoPorosity = ImageTk.PhotoImage(image=self.imPorosity)
        self.canvasPorosity.create_image(0, 0, image=self.photoPorosity, anchor=NW)
        # self.canvasPorosity.create_text(self.porosity.shape[1] + 60, 150, text="Legend:", justify=CENTER, font="Verdana 20")
        # for g in range(0, 254):
        #     self.canvasPorosity.create_oval(self.porosity.shape[1] + 130, g * 2, self.porosity.shape[1] + 130 - 10, g*2, width=1,
        #                             outline="#" + to_hex(100) + to_hex(g) + to_hex(100))

        self.master.update()