from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagInfoScreen import TagInfoScreen
from sptag.nfc.TagUidExtractor import TagUidExtractor

from os import getcwd
from tkinter import Button, Label


class MainScreen:
    tag_uid_extractor = None

    _current_screen = None

    _register_tag_button = None
    _view_tag_button = None

    _window = None

    def _init_screen_elements(self):
        self._register_tag_button = Button(self._window,
                                           text="Register Tag",
                                           command=self.register_tag)
        self._view_tag_button = Button(self._window,
                                       text="View Tag",
                                       command=self.view_tag)

        self._register_tag_button.grid(row=0, column=0, pady=(50, 10))
        self._view_tag_button.grid(row=1, column=0, pady=(100, 50))

    def __init__(self, window):
        self.tag_uid_extractor = TagUidExtractor(getcwd() +
                                                 "/libNFCWrapper.so")
        self._window = window

        if self.tag_uid_extractor.init_device():
            self._init_screen_elements()
        else:
            self.error_label = Label(self._window,
                                     text="FATAL ERROR: Couldn't initialize " +
                                          "NFC reader/writer!")
            self.error_label.pack()

    def close_current_screen(self):
        self._register_tag_button.grid(row=0, column=0, pady=(100, 10))
        self._view_tag_button.grid(row=1, column=0, pady=(100, 10))

        self._current_screen = None

    def register_tag(self, part_info=None):
        self._register_tag_button.grid_forget()
        self._view_tag_button.grid_forget()

        print(part_info)

        self._current_screen = TagEditorScreen(self, self._window,
                                               part_info)

    def view_tag(self):
        self._register_tag_button.grid_forget()
        self._view_tag_button.grid_forget()

        self._current_screen = TagInfoScreen(self, self._window)
