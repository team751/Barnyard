import tkinter
import os

from sptag.gui.MainScreen import MainScreen

def main():
    window = tkinter.Tk()
    tag_info_screen = MainScreen(window)

    window.title("Barnyard")

    window.mainloop()


if __name__ == '__main__':
    main()