import _thread
import kivy
kivy.require("1.9.1")

import os

from functools import partial
from pathlib import Path

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage

from sptag.nfc.TagUidExtractor import TagUidExtractor
from sptag.sheets.PartInfo import PartInfo
from sptag.sheets.UidCsvInfoModifier import UidCsvInfoModifier
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier

from pathlib import Path


class MainScreen(Screen):
    tag_uid_extractor = None

    _box_layout = None
    _instruction_label = None
    _internet_status_label = None
    _new_tag_button = None
    _past_register_bind = None
    _register_tag_button = None
    _search_tag_button = None
    _signal_sender = None
    _uid_sheet_info_modifier = None

    _part_info_labels = []
    _part_uid = None

    _window = None

    def _attempt_sheets_connection(self):
        if self._internet_status_label is None:
            self._internet_status_label = Label()
    
        try:
            self._uid_sheet_info_modifier = UidSheetInfoModifier()
            
            self._internet_status_label.color = [0, 1, 0, 1]
            self._internet_status_label.text = "Connected to Google Sheets"
        except:
            print("No connection")
            self._uid_sheet_info_modifier = UidCsvInfoModifier()
            
            self._internet_status_label.text = "Not connected to Google " +\
                                               "Sheets. Using backed up CSV " +\
                                               "file last modified at " +\
                                               self._uid_sheet_info_modifier.\
                                               get_last_update()
            self._internet_status_label.color = [1, 0, 0, 1]

    def _generate_image(self, image_url):
        if image_url == "locallystored":
            if os.path.isfile(str(Path.home()) + "/Barnyard-2/" + self._part_uid + ".jpg"):
                return AsyncImage(source=str(Path.home()) + "/Barnyard-2/" + self._part_uid + ".jpg")
            else:
                return AsyncImage(source=str(Path.home()) + "/Barnyard-2/" + self._part_uid + ".png")
        elif "Not connected" in self._internet_status_label.text:
            # Offline mode: get downloaded image on hdd
            path = str(Path.home()) + "/Barnyard-2/" + "downloaded_" + self._part_uid + ".png"
            
            print(path)
            
            return AsyncImage(source=path)
        else:
            return AsyncImage(source=image_url)

    def _init_screen_elements(self):
        self._instruction_label = Label(text="Scan NFC Part Tag")
        self._new_tag_button = Button(text="Scan New Tag")
        self._register_tag_button = Button(text="Register Tag")
        self._search_tag_button = Button(text="Search Registered Tags")
        
        self._new_tag_button.bind(on_press=self.scan_tag)
        self._search_tag_button.bind(on_press=self.search_tags)
        
        self._box_layout.add_widget(self._instruction_label)
        self._box_layout.add_widget(self._internet_status_label)

 
    def __init__(self, signal_sender):
        super().__init__(name="Main Screen")

        self._signal_sender = signal_sender
       
        self._attempt_sheets_connection()

        self._box_layout = BoxLayout(orientation="vertical")

        print(os.getcwd() + "/libNFCWrapper.so")
        self.tag_uid_extractor = TagUidExtractor(os.getcwd() +
                                                 "/libNFCWrapper.so")

        self.add_widget(self._box_layout)

        if self.tag_uid_extractor.init_device():
            self._init_screen_elements()
        else:
            self.error_label = Label(text="FATAL ERROR: Couldn't initialize " +
                                          "NFC reader/writer!")
            self._box_layout.add_widget(self.error_label)

    def switch_screen(self, screen_name, data=None):
        self._signal_sender.switch_screen(screen_name, data)

    def _scanning_thread(self):
        print("scanning")
        while True:
            print("scanningnextuid")
            next_uid = self.tag_uid_extractor.get_uid_from_next_tag()
            print("UID GOT! " + next_uid)

            if next_uid is not None:
                self._part_uid = next_uid
            
                self.refresh_part_data()
            
                break
        
    def scan_tag(self, instance=None):
        if self._instruction_label is None:
            return
        
        
        self._instruction_label.text = "Scan NFC Part Tag"
    
        for label in self._part_info_labels:
            self._box_layout.remove_widget(label)
    
        self._part_info_labels.clear()
    
        self._box_layout.remove_widget(self._register_tag_button)
        self._box_layout.remove_widget(self._new_tag_button)
        self._box_layout.add_widget(self._search_tag_button)

        _thread.start_new_thread(self._scanning_thread, ())
    
    def search_tags(self, instance=None):
        self.switch_screen("search_tag")
    
    def refresh_part_data(self):
        self._box_layout.remove_widget(self._search_tag_button)
        
        self._box_layout.remove_widget(self._new_tag_button)
        self._box_layout.remove_widget(self._register_tag_button)
    
        self._attempt_sheets_connection()
    
        part_info = self._uid_sheet_info_modifier.get_part_info(self._part_uid)
    
        if part_info is None:
            if self._part_uid is None:
                self.scan_tag()
            else:
                self._instruction_label.text = "No Part Found!"
                self._register_tag_button.text = "Add Part"

                part_info = PartInfo(self._part_uid)

                for label in self._part_info_labels:
                    self._box_layout.remove_widget(label)

                self._part_info_labels.clear()

                self._part_info_labels.append(Label(text="Tag UID:" + self._part_uid))
            
                self._box_layout.add_widget(self._part_info_labels[0])
        else:
            self._instruction_label.text = "Part Found!"
            self._register_tag_button.text = "Modify/Delete Part"
            
            if len(self._part_info_labels) > 1:
                self._box_layout.remove_widget(self._part_info_labels[-1])
            
                self._part_info_labels[1].text = "Name:" + part_info.name
                self._part_info_labels[2].text = "Description:" + \
                                                  part_info.description
                self._part_info_labels[3].text = "Location:" + part_info.location
                
                self._part_info_labels[4] = self._generate_image(part_info.image_url)

                self._box_layout.add_widget(self._part_info_labels[-1])
            else:
                for label in self._part_info_labels:
                    self._box_layout.remove_widget(label)
                
                self._part_info_labels.clear()
            
                self._part_info_labels.append(Label(text="Tag UID:" + self._part_uid))
                self._part_info_labels.append(Label(text="Name:" + part_info.name))
                self._part_info_labels.append(Label(text="Description:" +
                                                         part_info.description))
                self._part_info_labels.append(Label(text="Location:" +
                                                         part_info.location))
                self._part_info_labels.append(self._generate_image(part_info.image_url))

                for label in self._part_info_labels:
                    self._box_layout.add_widget(label)

            self._part_info_labels[-1].reload()
        
        if self._past_register_bind is not None:
            self._register_tag_button.unbind(on_press=self._past_register_bind)

        self._past_register_bind = partial(self.register_tag, part_info) 
        
        self._register_tag_button.bind(on_press=self._past_register_bind)
        
        self._box_layout.add_widget(self._register_tag_button)
        self._box_layout.add_widget(self._new_tag_button)

    def register_tag(self, part_info, instance):
        print(part_info.name)
        self.switch_screen("register_tag", part_info)

