from kivy.core.window import Window

from kivy.graphics.transformation import Matrix

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from sptag.sheets.UidCsvInfoModifier import UidCsvInfoModifier
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier

from sptag.gui.MainScreen import MainScreen

import _thread


class TagSearchScreen(Screen):
    connected = True

    _box_layout = None
    _item_box_layout = None
    _scroll_view = None
    
    _back_button = None
    _keyword_field = None
    _search_description_button = None
    _search_name_button = None
    _search_label = None
    _search_location_button = None
    _search_result_label = None
    
    _current_items = []
    _current_item_details = None
    _search_item_widgets = []
    
    _main_screen = None

    _on_item_details = False

    _uid_sheet_info_modifier = None

    def _adapt_keyboard(self, instance, value):
        if instance.keyboard is not None and instance.keyboard.widget is not None:
            instance.keyboard.widget.apply_transform(Matrix().scale(.65, .65, .65))

    def _gather_results(self, data):
        for widget in self._search_item_widgets:
            self._box_layout.remove_widget(widget)

        if self._search_result_label is not None:
            self._box_layout.remove_widget(self._search_result_label)

        self._current_items.clear()
        self._search_item_widgets.clear()

        if len(data) > 0:
            if self._search_name_button.state == 'down':
                self._current_items = self._uid_sheet_info_modifier.search_for_parts(name=data)
            elif self._search_description_button.state == 'down':
                self._current_items = self._uid_sheet_info_modifier.search_for_parts(description=data)
            elif self._search_location_button.state == 'down':
                self._current_items = self._uid_sheet_info_modifier.search_for_parts(location=data)

            self._search_result_label = Label(text="Search Results:")

            for item in self._current_items:
                self._search_item_widgets.append(MainScreen.generate_image(item.image_url, item.uid, self.connected))
                self._search_item_widgets.append(Button(text="UID: " + item.uid + " Name: " + item.name,
                                                        on_press=self.open_item_details))

            if len(self._current_items) <= 0:
                self._search_result_label.text = "No Search Results"
        else:
            self._search_result_label = Label(text="No Search Results")

        self._box_layout.add_widget(self._search_result_label)

        for widget in self._search_item_widgets:
            self._box_layout.add_widget(widget)

    def __init__(self, main_screen):
        super().__init__(name="Tag Searching Screen")
    
        try:
            self._uid_sheet_info_modifier = UidSheetInfoModifier()
        except:
            self._uid_sheet_info_modifier = UidCsvInfoModifier()
        
        self._main_screen = main_screen
        
        self._box_layout = BoxLayout(orientation='vertical', spacing=10)
        self._scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        
        self._back_button = Button(text="Back", on_press=self.go_back)
        self._keyword_field = TextInput(multiline=False)
        self._search_name_button = ToggleButton(text="by Name", group="search_type", state='down',
                                                on_press=self.on_search_query)
        self._search_description_button = ToggleButton(text="by Description", group="search_type",
                                                       on_press=self.on_search_query)
        self._search_label = Label(text="Enter search keyword")
        self._search_location_button = ToggleButton(text="by Location", group="search_type",
                                                    on_press=self.on_search_query)

        self._keyword_field.bind(focus=self._adapt_keyboard, text=self.on_search_query)

        self.add_widget(self._scroll_view)

        self._scroll_view.add_widget(self._box_layout)

        self._box_layout.add_widget(self._back_button)
        self._box_layout.add_widget(self._search_label)
        self._box_layout.add_widget(self._keyword_field)
        
        self._box_layout.add_widget(self._search_name_button)
        self._box_layout.add_widget(self._search_description_button)
        self._box_layout.add_widget(self._search_location_button)

    def go_back(self, instance):
        print("back")

        if self._on_item_details:
            self._item_box_layout.remove_widget(self._back_button)

            self.remove_widget(self._item_box_layout)

            self._item_box_layout = None

            self.add_widget(self._scroll_view)

            # TODO(Bobby): A cleaner way to reset the _box_layout view properly
            self._box_layout.remove_widget(self._search_result_label)

            for widget in self._search_item_widgets:
                self._box_layout.remove_widget(widget)

            self._box_layout.remove_widget(self._search_label)
            self._box_layout.remove_widget(self._keyword_field)

            self._box_layout.remove_widget(self._search_name_button)
            self._box_layout.remove_widget(self._search_description_button)
            self._box_layout.remove_widget(self._search_location_button)

            self._box_layout.add_widget(self._back_button)
            self._box_layout.add_widget(self._search_label)
            self._box_layout.add_widget(self._keyword_field)

            self._box_layout.add_widget(self._search_name_button)
            self._box_layout.add_widget(self._search_description_button)
            self._box_layout.add_widget(self._search_location_button)

            self._box_layout.add_widget(self._search_result_label)

            for widget in self._search_item_widgets:
                self._box_layout.add_widget(widget)

            self._on_item_details = False
        else:
            self._main_screen.switch_screen("main_screen")

    def modify_part(self, instance):
        self.go_back(None)

        self._main_screen.switch_screen("register_tag", self._current_item_details)

    def on_search_query(self, instance, data=None):
        if data is None:
            data = self._keyword_field.text

        _thread.start_new_thread(self._gather_results, (data,))

    def open_item_details(self, instance):
        self._on_item_details = True

        self._box_layout.remove_widget(self._back_button)

        self.remove_widget(self._scroll_view)

        for item in self._current_items:
            if item.uid == instance.text.split("UID: ")[-1].split(" Name: ")[0]:
                self._current_item_details = item
                break

        self._item_box_layout = BoxLayout(orientation='vertical', spacing=10)

        self.add_widget(self._item_box_layout)

        self._item_box_layout.add_widget(self._back_button)
        self._item_box_layout.add_widget(MainScreen.generate_image(self._current_item_details.image_url,
                                                                   self._current_item_details.uid,
                                                                   self.connected))
        self._item_box_layout.add_widget(Label(text="UID: " + self._current_item_details.uid))
        self._item_box_layout.add_widget(Label(text="Name: " + self._current_item_details.name))
        self._item_box_layout.add_widget(Label(text="Description: " + self._current_item_details.description))
        self._item_box_layout.add_widget(Label(text="Location: " + self._current_item_details.location))
        self._item_box_layout.add_widget(Button(text="Modify/Delete Part", on_press=self.modify_part))
