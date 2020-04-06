import kivy
kivy.require("1.9.1")

from pathlib import Path
from time import sleep

from kivy.core.window import Window

from kivy.graphics.transformation import Matrix

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from sptag.sheets.PartInfo import PartInfo
from sptag.sheets.UidCsvInfoModifier import UidCsvInfoModifier
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier

import _thread
import os
import importlib


class TagEditorScreen(Screen):
    _back_button = None
    _camera = None

    _box_layout = None
    
    _entry_list = []
    _tag_association_button = None
    _text_box_labels = []
    
    _delete_part_button = None
    
    _association_label = None
    _association_label_image = None
    
    _part_info = None
    
    _main_screen = None

    return_to_main_screen = True

    def _adapt_keyboard(self, instance, value):
        if instance.keyboard is not None:
            instance.keyboard.widget.apply_transform(Matrix().scale(.65, .65, .65))

    def take_photo(self):
        piCameraSpec = importlib.util.find_spec("picamera")

        if piCameraSpec is None:
            from SimpleCV import Camera

            print("No PiCamera library found. Using opencv...")
            self._camera = Camera()

            sleep(4)
            image = self._camera.getImage()
            image.save(str(Path.home()) + "/Barnyard-2/" +
                       self._part_info.uid + ".png")
        else:
            from picamera import PiCamera

            print("PiCamera library found.")
            self._camera = PiCamera()

            self._camera.start_preview(alpha=200)
            self._camera.rotation = 270

            sleep(4)

            if os.path.isfile(str(Path.home()) + "/Barnyard-2/" +
                              self._part_info.uid + ".jpg"):
                os.remove(str(Path.home()) + "/Barnyard-2/" +
                          self._part_info.uid + ".jpg")

            self._camera.capture(str(Path.home()) + "/Barnyard-2/" +
                                 self._part_info.uid + ".jpg")
            self._camera.stop_preview()

            self._camera.close()

    def associate_tag(self, instance):
        for entry in self._entry_list:
            self._box_layout.remove_widget(entry)
        
        self._box_layout.remove_widget(self._tag_association_button)
        
        for text_box_label in self._text_box_labels:
            self._box_layout.remove_widget(text_box_label)
        
        if self._part_info.uid is None:
            self._association_label_image = AsyncImage(source=os.getcwd() + "/tap.png")
            self._association_label = Label(text="Tap an NFC tag now to associate")

            self._box_layout.add_widget(self._association_label_image)
            self._box_layout.add_widget(self._association_label)

            _thread.start_new_thread(self._get_next_nfc_tag_uid,
                                     ())
        else:
           try:
                uid_sheet_info_modifier = UidSheetInfoModifier()
           except:
                # No connection... Use CSV Backup
                uid_sheet_info_modifier = UidCsvInfoModifier()
           
           self._update_part_info()

           uid_sheet_info_modifier.add_part(self._part_info)
                
           self.go_back()

    def delete_tag(self, instance):
        try:
            uid_sheet_info_modifier = UidSheetInfoModifier()
        except:
            # No connection... Use CSV Backup
            uid_sheet_info_modifier = UidCsvInfoModifier()

        uid_sheet_info_modifier.delete_part(self._part_info)

        self.go_back()

    def go_back(self, notedited=True):
        Window.release_all_keyboards()

        if self.return_to_main_screen:
            self._main_screen.switch_screen("main_screen")
        else:
            self._main_screen.switch_screen("search_tag")

    def modify_tag(self, instance):
        try:
            uid_sheet_info_modifier = UidSheetInfoModifier()
        except:
            # No connection... Use CSV Backup
            uid_sheet_info_modifier = UidCsvInfoModifier()

        self._update_part_info()

        uid_sheet_info_modifier.edit_part(self._part_info)

        self.go_back(False)

    def _add_text_entry_label(self, i):
        if i == 0:
            self._text_box_labels.append(Label(text="Name"))
        elif i == 1:
            self._text_box_labels.append(Label(text="Description"))
        elif i == 2:
            self._text_box_labels.append(Label(text="Location"))
        elif i == 3:
            self._text_box_labels.append(Label(text="Image URL"))
    
    def _get_next_nfc_tag_uid(self):
        while True:
            next_uid = self._main_screen.tag_uid_extractor.\
                get_uid_from_next_tag()
            
            try:
                uid_sheet_info_modifier = UidSheetInfoModifier()
            except:
                # No connection... Use CSV Backup
                uid_sheet_info_modifier = UidCsvInfoModifier()

            if next_uid is not None:
                self._part_info.uid = next_uid
                
                self._update_part_info()

                uid_sheet_info_modifier.add_part(self._part_info)
                
                self.go_back()
                
                break

    def _init_screen_elements(self, editing=True):
        self._back_button = Button(text="Back",
                                   on_press=self.go_back)

        if editing:
            self._tag_association_button = Button(text="Retake Photo (if " +
                                                       "url is blank) and " +
                                                       "modify tag.",
                                                  on_press=self.modify_tag)

            self._delete_part_button = Button(text="Delete " +
                                              self._part_info.name,
                                              on_press=self.delete_tag)
        else:
            self._tag_association_button = Button(text="Take Photo and " +
                                                  "Associate with Tag",
                                                  on_press=self.associate_tag)

        for i in range(4):
            self._add_text_entry_label(i)
            
            if i == 0:
                self._entry_list.append(TextInput(multiline=False))
                
                if self._part_info.name is not None:
                    self._entry_list[-1].text = self._part_info.name
            else:
                self._entry_list.append(TextInput(multiline=True))

                if i == 1 and self._part_info.description is not None:
                    self._entry_list[-1].text = self._part_info.description
                elif i == 2 and self._part_info.location is not None:
                    self._entry_list[-1].text = self._part_info.location
                elif i == 3 and self._part_info.image_url is not None:
                    self._entry_list[-1].text = self._part_info.image_url

            self._entry_list[-1].bind(focus=self._adapt_keyboard)

        self._box_layout.add_widget(self._back_button)

        if editing:
            self._box_layout.add_widget(self._delete_part_button)

        for entry_index in range(len(self._entry_list)):
            self._box_layout.add_widget(self._text_box_labels[entry_index])
            self._box_layout.add_widget(self._entry_list[entry_index])

        self._box_layout.add_widget(self._tag_association_button)


    def _update_part_info(self):
        for entry_list_index in range(len(self._entry_list)):
            current_label = self._entry_list[entry_list_index]

            if entry_list_index == 0:
                self._part_info.name = current_label.text.rstrip()
            elif entry_list_index == 1:
                self._part_info.description = current_label.text.rstrip()
            elif entry_list_index == 2:
                self._part_info.location = current_label.text.rstrip()
            elif entry_list_index == 3:
                self._part_info.image_url = current_label.text.rstrip()

        if self._part_info.image_url == "\n" or \
                self._part_info.image_url == "":
            self._part_info.image_url = "locallystored"

            self.take_photo()

    def __init__(self, main_screen):
        super().__init__(name="Tag Editor Screen")

        self._box_layout = BoxLayout(orientation='vertical', spacing=10)
        
        self._main_screen = main_screen

        self.add_widget(self._box_layout)
     
    def part_init(self, part_info):
        if self._back_button is not None:
            self._box_layout.remove_widget(self._back_button)
            self._back_button = None
        
        if self._delete_part_button is not None:
            self._box_layout.remove_widget(self._delete_part_button)
            self._delete_part_button = None

        for entry_index in range(len(self._entry_list)):
            self._box_layout.remove_widget(self._text_box_labels[entry_index])
            self._box_layout.remove_widget(self._entry_list[entry_index])
            
        self._text_box_labels.clear()
        self._entry_list.clear()
        
        if self._tag_association_button is not None:
            self._box_layout.remove_widget(self._tag_association_button)
            self._tag_association_button = None

        self._part_info = part_info

        self._init_screen_elements(part_info.name is not None)
