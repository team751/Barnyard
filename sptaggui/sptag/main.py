import tkinter
import os

from sptag.gui.TagInfoScreen import TagInfoScreen

def main():
    window = tkinter.Tk()
    tag_info_screen = TagInfoScreen(window)
    #tag_info_screen.start()

    window.mainloop()

if __name__ == '__main__':
    main()