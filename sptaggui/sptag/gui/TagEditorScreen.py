from tkinter import Entry, Label, StringVar

class TagEditorScreen():
    _entry_list = []
    _labels_for_entries_list = []
    _text_box_labels = []
    _window = None

    def _add_text_entry_label(self, i):
        if i == 0:
            self._text_box_labels.append(Label(self._window,
                                               text="Name"))
        elif i == 1:
            self._text_box_labels.append(Label(self._window,
                                               text="Description")
        elif i == 2:
            self._text_box_labels.append(Label(self._window,
                                               text="Location")

    def _init_screen_elements(self):
        for i in range(3):
            self._add_text_entry_label(i)

            self._entry_list.append(Entry(self._window))

        for entry in self._entry_list:
            entry.pack()

        for label in self._text_box_labels:
            label.pack()

    def __init__(self, window):
        self._window = window

        self._init_screen_elements()
