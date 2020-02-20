import kivy
kivy.require("1.11.0")

from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagInfoScreen import TagInfoScreen
from sptag.nfc.TagUidExtractor import TagUidExtractor

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from os import getcwd

class MainScreen(Screen):
    tag_uid_extractor = None

    _box_layout

    _register_tag_button = None
    _view_tag_button = None

    _window = None

    def _init_screen_elements(self):
        self._register_tag_button = Button(text="Register Tag")
                                           
        self._view_tag_button = Button(text="View Tag")

		self._register_tag_button.bind(on_press=self.register_tag)
		self._view_tag_button.bind(on_press=self.view_tag)

        self.add_widget(self._register_tag_button)
        self.add_widget(self._view_tag_button)

    def __init__(self):
   		super().__init__("Main Screen")
   		
        self.tag_uid_extractor = TagUidExtractor(getcwd() +
                                                 "/libNFCWrapper.so")

        if self.tag_uid_extractor.init_device():
            self._init_screen_elements()
        else:
            self.error_label = Label(text="FATAL ERROR: Couldn't initialize " +
                                          "NFC reader/writer!")
            self.add_widget(self.error_label)

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
