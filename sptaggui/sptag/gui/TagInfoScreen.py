import _thread

import kivy
kivy.require("1.9.1")

from os import getcwd
from tempfile import gettempdir
from urllib.request import urlretrieve

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label

from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier


class TagInfoScreen(Screen):
    _back_button = None
    _box_layout = None
    _main_screen = None
    _nfc_tap_label = None
    _part_info_list = []
    _part_info_label_list = []
    _part_info_button_list = []
    _part_info_image = None
    _uid_sheet_info_modifier = None
    _window = None
    _first_time = False

    def _generate_image_label(self, image_url, part_uid):
        if image_url == "locallystored":
            image_file_name = "/home/pi/Pictures/Barnyard-2/" + part_uid + \
                              ".jpg"
        else:
            image_file_name = gettempdir() + "/temp_" + str(part_uid) + ".png"

            urlretrieve(image_url, image_file_name)

        self._part_info_label_list.append(Image(source=image_file_name))

    def display_part(self, part_info, uid):
        self._part_info_label_list.clear()
        
        self._part_info_list.append(part_info)

        if part_info is None:
            self._part_info_label_list.append(Label(text="Couldn't find UID in database!"))
            self._part_info_label_list.append(Label(text="UID Scanned =" + uid))
        else:
            self._part_info_label_list.append(Label(text="UID:" + part_info.uid))
            self._part_info_label_list.append(Label(text="Name:" + part_info.name))
            self._part_info_label_list.append(Label(text="Description:" +
                                                     part_info.description))
            self._part_info_label_list.append(Label(text="Location:" +
                                                     part_info.location))
            self._first_time = True
            _edit_button = None
            _edit_button = Button(text="Edit " + part_info.name,
                                  on_click=lambda name=part_info.name:
                                  self.edit_part(name))
            self._part_info_label_list.append(_edit_button)
            self._part_info_button_list.append(_edit_button)
 
            self._generate_image_label(part_info.image_url, part_info.uid)

        for part_info_label in self._part_info_label_list:
            # all objects part of this list should be a Label
            #assert part_info_label is Label

            self._box_layout.add_widget(part_info_label)

    def edit_part(self, part_name):
        for part_info in self._part_info_list:
            if part_info.name == part_name:
                self.go_back()
                self._main_screen.register_tag(part_info)

    def _get_next_nfc_tag_uid(self, a, b):
        while True:
            next_uid = self._main_screen.tag_uid_extractor.get_uid_from_next_tag()

            if next_uid is not None:
                print("id=" + next_uid)
                
                self.display_part(self._uid_sheet_info_modifier.
                                  get_part_info(next_uid), next_uid)
                break
            
    def go_back(self, instance):
        self._main_screen.switch_screen("main_screen")

    def _init_screen_elements(self):
        self._back_button = Button(text="Back",
                                   on_press=self.go_back)
        self._nfc_tap_label = Label(text="Please tap an NFC tag")

        self._box_layout.add_widget(self._back_button)
        self._box_layout.add_widget(self._nfc_tap_label)

    def __init__(self, main_screen):
        super().__init__(name="Tag Info Screen")

        self._box_layout = BoxLayout(orientation='vertical', spacing=10)
        self._main_screen = main_screen

        self.add_widget(self._box_layout)
        self._init_screen_elements()

        self._uid_sheet_info_modifier = UidSheetInfoModifier()

        _thread.start_new_thread(self._get_next_nfc_tag_uid,
                                 (self, None))
