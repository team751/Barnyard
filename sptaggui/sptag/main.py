import tkinter
import os

from sptag.gui.TagInfoScreen import TagInfoScreen
from sptag.nfc.TagUidExtractor import TagUidExtractor

def main():
    #window = tkinter.Tk()
    #tag_info_screen = TagInfoScreen(window)
    #tag_info_screen.start()

    #window.mainloop()

    _tag_uid_extractor = TagUidExtractor(os.getcwd() + "/libNFCWrapper.so")
    _tag_uid_extractor.init_device()
    print(str(_tag_uid_extractor.get_uid_from_next_tag()))

if __name__ == '__main__':
    main()