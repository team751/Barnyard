import _thread

from tkinter import Label

from sptag.nfc.TagUidExtractor import TagUidExtractor


class TagInfoScreen():
    _nfc_tap_label = None
    _tag_uid_extractor = None
    _window = None

    def _get_next_nfc_tag_uid(self):
        while True:
            nextUid = self._tag_uid_extractor.get_uid_from_next_tag()

            if nextUid != -1:
                pass
            

    def _init_screen_elements(self):
        self.nfc_tap_label = Label(self.window, text="Please tap an NFC tag")

        self.nfc_tap_label.pack()

    def __init__(self, window):
        self.window = window

        self._init_screen_elements()

        self._tag_uid_extractor = TagUidExtractor("libnfcwrapper.so")

        if self._tag_uid_extractor.init_device():
            _thread.start_new_thread(self._get_next_nfc_tag_uid, None)
        else:
            print("ERROR: Couldn't initialize NFC reader/writer!")