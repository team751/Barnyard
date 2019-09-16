import tkinter
import os

from gui.MainScreen import MainScreen

def main():
    window = tkinter.Tk()

    window.title("Barnyard")

    tag_info_screen = MainScreen(window)

    window.mainloop()

if __name__ == '__main__':
    main()
