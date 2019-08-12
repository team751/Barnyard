import _thread

from os import getcwd
from PIL import Image, ImageTk
from tempfile import gettempdir
from tkinter import Button, Label
from urllib.request import urlretrieve

from sptag.nfc.TagUidExtractor import TagUidExtractor
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier


class TagInfoScreen():
    _back_button = None
    _main_screen = None
    _nfc_tap_label = None
    _part_info_label_list = []
    _part_info_image = None
    _tag_uid_extractor = None
    _uid_sheet_info_modifier = None
    _window = None

    def _generate_image_label(self, image_url, part_uid):
        temp_image_file_name = gettempdir() + "/temp_" + str(part_uid) +  ".png"

        urlretrieve(image_url, temp_image_file_name)

        pil_image = Image.open(temp_image_file_name)

        self._part_info_image = ImageTk.PhotoImage(pil_image)
        self._part_info_label_list.append(Label(self._window,
                                                image=self._part_info_image))

    def display_part(self, part_info, uid):
        self._part_info_label_list.clear()

        if part_info is None:
            self._part_info_label_list.append(Label(self._window,
                                        text="Couldn't find UID in database!"))
            self._part_info_label_list.append(Label(self._window,
                                        text="UID Scanned =" + uid))
        else:
            self._part_info_label_list.append(Label(self._window,
                                                text="UID:" + part_info.uid))
            self._part_info_label_list.append(Label(self._window,
                                                text="Name:" + part_info.name))
            self._part_info_label_list.append(Label(self._window,
                                                text="Description:" +
                                                     part_info.description))
            self._part_info_label_list.append(Label(self._window,
                                                text="Location:" +
                                                     part_info.location))

            self._generate_image_label(part_info.image_url, part_info.uid)

        for part_info_label in self._part_info_label_list:
            # all objects part of this list should be a Label
            #assert part_info_label is Label

            part_info_label.pack()

    def _get_next_nfc_tag_uid(self):
        while True:
            next_uid = self._tag_uid_extractor.get_uid_from_next_tag()

            if next_uid != None:
                print("id=" + next_uid)
                self.display_part(self._uid_sheet_info_modifier.
                                 get_part_info(next_uid), next_uid)
            
    def go_back(self):
        self._back_button.pack_forget()
        self._nfc_tap_label.pack_forget()
        
        for label in self._part_info_label_list:
            label.destroy()
        
        self._main_screen.close_current_screen()

    def _init_screen_elements(self):
        self._back_button = Button(self._window, text="Back", 
                                   command=self.go_back)
        self._nfc_tap_label = Label(self._window, text="Please tap an NFC tag")

        self._back_button.pack()
        self._nfc_tap_label.pack()

    def __init__(self, main_screen, window):
        self._main_screen = main_screen
        self._window = window

        self._init_screen_elements()

        self._tag_uid_extractor = TagUidExtractor(getcwd() + "/libNFCWrapper.so")
        self._uid_sheet_info_modifier = UidSheetInfoModifier()

        if self._tag_uid_extractor.init_device():
            _thread.start_new_thread(self._get_next_nfc_tag_uid, (self, None))
        else:
            print("ERROR: Couldn't initialize NFC reader/writer!")
