from os import getcwd
from picamera import PiCamera
from PIL import Image, ImageTk
from time import sleep
from tkinter import Button, Entry, Label, PhotoImage, StringVar, Text

from sptag.nfc.TagUidExtractor import TagUidExtractor
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier, \
                                              PartInfo

import _thread

class TagEditorScreen():
    _back_button = None
    _camera = None
    
    _entry_list = []
    _tag_association_button = None
    _text_box_labels = []
    
    _association_label = None
    _association_label_image = None
    
    _part_info = None
    _tag_uid_extractor = None
    
    _main_screen = None
    _window = None


    def take_photo(self):
        self._camera = PiCamera()
        
        self._camera.start_preview(alpha=200)
        sleep(5)
        self._camera.capture("/home/pi/Pictures/Barnyard-2/" + \
                             self._part_info.uid + ".jpg")
        self._camera.stop_preview()

    def associate_tag(self):
        self._tag_uid_extractor = TagUidExtractor(getcwd() + 
                                                  "/libNFCWrapper.so")
        
        for entry in self._entry_list:
            entry.pack_forget()
        
        self._tag_association_button.pack_forget()
        
        for text_box_label in self._text_box_labels:
            text_box_label.pack_forget()
        
        pil_image = Image.open("nfc-tap.png")
        
        self._association_label_image = ImageTk.PhotoImage(pil_image)
        self._association_label = Label(self._window, 
                                image=self._association_label,
                                text="Tap an NFC tag now to associate")
        
        self._association_label.pack()
        
        if self._tag_uid_extractor.init_device():
            _thread.start_new_thread(self._get_next_nfc_tag_uid, 
                                     ())
        else:
            print("ERROR: Couldn't initialize NFC reader/writer!")
    
    def go_back(self):
        if self._association_label is not None:
            self._association_label.pack_forget()
        
        self._back_button.pack_forget()
        self._tag_association_button.pack_forget()
        
        for entry in self._entry_list:
            entry.destroy()
        
        for label in self._text_box_labels:
            label.destroy()
        
        self._entry_list.clear()
        self._text_box_labels.clear()
        
        self._main_screen.close_current_screen()

    def _add_text_entry_label(self, i):
        if i == 0:
            self._text_box_labels.append(Label(self._window,
                                               text="Name"))
        elif i == 1:
            self._text_box_labels.append(Label(self._window,
                                               text="Description"))
        elif i == 2:
            self._text_box_labels.append(Label(self._window,
                                            text="Location"))
        elif i == 3:
            self._text_box_labels.append(Label(self._window,
                                            text="Image URL"))
    
    def _get_next_nfc_tag_uid(self):
        while True:
            next_uid = self._tag_uid_extractor.get_uid_from_next_tag()
            uid_sheet_info_modifier = UidSheetInfoModifier()

            if next_uid != None:
                self._part_info.uid = next_uid
                
                for entry_list_index in range(len(self._entry_list)):
                    current_label = self._entry_list[entry_list_index]   
                    
                    if entry_list_index == 0:
                        self._part_info.name = current_label.get()
                    elif entry_list_index == 1:
                        self._part_info.description = current_label.get(
                                                           "1.0", "end")
                    elif entry_list_index == 2:
                        self._part_info.location = current_label.get(
                                                           "1.0", "end")
                    elif entry_list_index == 3:
                        self._part_info.image_url = current_label.get(
                                                           "1.0", "end")
                
                if self._part_info.image_url == "\n":
                    self._part_info.image_url = "locallystored"
                    
                    self.take_photo()
                
                uid_sheet_info_modifier.add_part(self._part_info)
                
                self.go_back()
                
                break

    def _init_screen_elements(self):
        self._back_button = Button(self._window, text="Back", 
                                   command=self.go_back)
        
        for i in range(4):
            self._add_text_entry_label(i)
            
            if i == 0:
                self._entry_list.append(Entry(self._window))
            else:
                self._entry_list.append(Text(self._window, width=20, 
                                             height=7))

        self._back_button.pack()

        for entry_index in range(len(self._entry_list)):
            self._text_box_labels[entry_index].pack()
            self._entry_list[entry_index].pack()

    def __init__(self, main_screen, window):
        self._part_info = PartInfo()
        
        self._main_screen = main_screen
        self._window = window

        self._init_screen_elements()
        
        self._tag_association_button = Button(self._window,
                                              text="Take Photo and " +
                                              "Associate with Tag",
                                              command=self.associate_tag)
        self._tag_association_button.pack()

