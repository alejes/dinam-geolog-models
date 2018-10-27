from tkinter import *
from window.frames.welcome import Welcome


def main():
    root = Tk()
    root.geometry("850x500+300+300")
    app = Welcome(root)
    root.mainloop()


if __name__ == '__main__':
    main()
