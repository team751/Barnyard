from tkinter import Entry, StringVar

class TagEditorScreen():
    _entry_list = []
    _labels_for_entries_list = []
    _text_box_string_variables = []
    _window = None

    def _add_text_entry_label(self, i):
        if i == 0:
            self._text_box_string_variables.append(self._window, text="Name")
        elif i == 1:
            self._text_box_string_variables.append(self._window,
                                                   text="Description")
        elif i == 2:
            self._text_box_string_variables.append(self._window,
                                                   text="Location")

    def _init_screen_elements(self):
        for i in range(3):
            self._text_box_string_variables.append(StringVar())

            self._add_text_entry_label(i)

            self._entry_list.append(Entry(self._window, textvariable=
                                        self._text_box_string_variables[i]))

        for entry in self._entry_list:
            entry.pack()

        for label in self._text_box_string_variables:
            label.pack()

    def __init__(self, window):
        self._window = window

        self._init_screen_elements()