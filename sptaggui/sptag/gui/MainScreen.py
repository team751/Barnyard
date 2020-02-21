import kivy
kivy.require("1.11.0")

from sptag.nfc.TagUidExtractor import TagUidExtractor


from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from os import getcwd


class MainScreen(Screen):
    tag_uid_extractor = None

    _box_layout = None
    _register_tag_button = None
    _signal_sender = None
    _view_tag_button = None

    _window = None

    def _init_screen_elements(self):
        self._register_tag_button = Button(text="Register Tag")
        self._view_tag_button = Button(text="View Tag")

        self._register_tag_button.bind(on_press=self.register_tag)
        self._view_tag_button.bind(on_press=self.view_tag)

        self._box_layout.add_widget(self._register_tag_button)
        self._box_layout.add_widget(self._view_tag_button)

    def __init__(self, signal_sender):
        super().__init__(name="Main Screen")

        self._signal_sender = signal_sender

        self._box_layout = BoxLayout(orientation="vertical")

        self.tag_uid_extractor = TagUidExtractor(getcwd() +
                                                 "/libNFCWrapper.so")

        self.add_widget(self._box_layout)

        if self.tag_uid_extractor.init_device():
            self._init_screen_elements()
        else:
            self.error_label = Label(text="FATAL ERROR: Couldn't initialize " +
                                          "NFC reader/writer!")
            self._box_layout.add_widget(self.error_label)

    def register_tag(self, part_info=None):
        print(part_info)

        self._signal_sender.switch_scene("register_tag")

    def view_tag(self):
        self._signal_sender.switch_scene("view_tag")
