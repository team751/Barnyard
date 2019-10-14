from os import getcwd
#from picamera import PiCamera
from PIL import Image, ImageTk
from time import sleep
from tkinter import Button, Entry, Frame, END, Label, SOLID, Text

from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier, \
                                              PartInfo

import _thread


class TagEditorScreen:
    _back_button = None
    _camera = None
    
    _entry_list = []
    _tag_association_button = None
    _text_box_labels = []
    
    _association_label = None
    _association_label_image = None
    
    _part_info = None
    
    _main_screen = None
    _window = None

    def take_photo(self):  
        self._camera = PiCamera()
        
        self._camera.start_preview(alpha=200)
        sleep(5)
        self._camera.capture("/home/pi/Pictures/Barnyard-2/" +
                             self._part_info.uid + ".jpg")
        self._camera.stop_preview()

    def associate_tag(self):

        
        for entry in self._entry_list:
            entry.pack_forget()
        
        self._tag_association_button.pack_forget()
        
        for text_box_label in self._text_box_labels:
            text_box_label.pack_forget()

        pil_image = Image.open(getcwd() + "/tap.png")
        
        self._association_label_image = ImageTk.PhotoImage(pil_image)
        self._association_label = Label(self._window, 
                                        image=self._association_label_image,
                                        text="Tap an NFC tag now to associate",
                                        compound="top")
        
        self._association_label.pack()

        _thread.start_new_thread(self._get_next_nfc_tag_uid,
                                 ())

    def delete_tag(self):
        uid_sheet_info_modifier = UidSheetInfoModifier()

        uid_sheet_info_modifier.delete_part(self._part_info)

        self.go_back()

    def go_back(self, edited=False):
        if self._association_label is not None:
            self._association_label.pack_forget()
        
        self._back_button.pack_forget()
        self._delete_part_button.pack_forget()
        self._tag_association_button.pack_forget()

        self._editor_frame.pack_forget()
        
        for entry in self._entry_list:
            entry.destroy()
        
        for label in self._text_box_labels:
            label.destroy()
        
        self._entry_list.clear()
        self._text_box_labels.clear()

        if edited:
            self._main_screen.view_tag()
        else:
            self._main_screen.close_current_screen()

    def modify_tag(self):
        uid_sheet_info_modifier = UidSheetInfoModifier()

        self._update_part_info()

        uid_sheet_info_modifier.edit_part(self._part_info)

        self.go_back(True)

    def _add_text_entry_label(self, i):
        if i == 0:
            self._text_box_labels.append(Label(self._editor_frame,
                                               text="Name"))
        elif i == 1:
            self._text_box_labels.append(Label(self._editor_frame,
                                               text="Description"))
        elif i == 2:
            self._text_box_labels.append(Label(self._editor_frame,
                                               text="Location"))
        elif i == 3:
            self._text_box_labels.append(Label(self._editor_frame,
                                               text="Image URL"))
    
    def _get_next_nfc_tag_uid(self):
        while True:
            next_uid = self._main_screen.tag_uid_extractor.\
                get_uid_from_next_tag()
            uid_sheet_info_modifier = UidSheetInfoModifier()

            if next_uid is not None:
                self._part_info.uid = next_uid
                
                self._update_part_info()

                uid_sheet_info_modifier.add_part(self._part_info)
                
                self.go_back()
                
                break

    def _init_screen_elements(self, editing=True):
        self._editor_frame = Frame(self._window, borderwidth=10, relief=SOLID)

        self._back_button = Button(self._editor_frame, text="Back",
                                   command=self.go_back)

        if editing:
            self._tag_association_button = Button(self._editor_frame,
                                                  text="Retake Photo (if " +
                                                       "url is blank) and " +
                                                       "modify tag.",
                                                  command=self.modify_tag)

            self._delete_part_button = Button(self._window,
                                              text="Delete " +
                                                   self._part_info.name,
                                              command=self.delete_tag)
        else:
            self._tag_association_button = Button(self._editor_frame,
                                                  text="Take Photo and " +
                                                  "Associate with Tag",
                                                  command=self.associate_tag)

        for i in range(4):
            self._add_text_entry_label(i)
            
            if i == 0:
                self._entry_list.append(Entry(self._editor_frame))
                
                if self._part_info.name is not None:
                    self._entry_list[-1].delete(0, END)
                    self._entry_list[-1].insert(0, self._part_info.name)
            else:
                self._entry_list.append(Text(self._editor_frame, width=20,
                                             height=7))
                if i == 1 and self._part_info.description is not None:
                    self._entry_list[-1].delete(1.0, END)
                    self._entry_list[-1].insert(1.0, self._part_info.description)
                elif i == 2 and self._part_info.location is not None:
                    self._entry_list[-1].delete(1.0, END)
                    self._entry_list[-1].insert(1.0, self._part_info.location)
                elif i == 3 and self._part_info.image_url is not None:
                    self._entry_list[-1].delete(1.0, END)
                    self._entry_list[-1].insert(1.0, self._part_info.image_url)

        self._back_button.pack()

        self._editor_frame.pack()

        if editing:
            self._delete_part_button.pack()

        for entry_index in range(len(self._entry_list)):
            self._text_box_labels[entry_index].pack()
            self._entry_list[entry_index].pack()

        self._tag_association_button.pack()

    def _update_part_info(self):
        for entry_list_index in range(len(self._entry_list)):
            current_label = self._entry_list[entry_list_index]

            if entry_list_index == 0:
                self._part_info.name = current_label.get().rstrip()
            elif entry_list_index == 1:
                self._part_info.description = current_label.get(
                    "1.0", "end").rstrip()
            elif entry_list_index == 2:
                self._part_info.location = current_label.get(
                    "1.0", "end").rstrip()
            elif entry_list_index == 3:
                self._part_info.image_url = current_label.get(
                    "1.0", "end").rstrip()

        if self._part_info.image_url == "\n" or \
                self._part_info.image_url == "":
            self._part_info.image_url = "locallystored"

            self.take_photo()

    def __init__(self, main_screen, window, part_info=None):
        if part_info is None:
            self._part_info = PartInfo()
        else:
            self._part_info = part_info
        
        self._main_screen = main_screen
        self._window = window

        self._init_screen_elements(part_info is not None)
