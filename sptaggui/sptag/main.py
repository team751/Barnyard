import tkinter
import os

from sptag.gui.TagInfoScreen import TagInfoScreen
#from sptag.gui.TagEditorScreen import TagEditorScreen

def main():
    window = tkinter.Tk()
    tag_info_screen = TagInfoScreen(window)
    tag_info_screen.start()
    #tag_editor_screen = TagEditorScreen(window)

    window.mainloop()

if __name__ == '__main__':
    main()
