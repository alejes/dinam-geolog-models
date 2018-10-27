from tkinter import *
from lib.similarity import *


def main():
    s = Similarity(5)
    lines = s.calculate([1.0], [0.5], [1.0], [0.5])
    print(lines)


if __name__ == '__main__':
    main()