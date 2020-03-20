from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from sptag.sheets.UidCsvInfoModifier import UidCsvInfoModifier
from sptag.sheets.UidSheetInfoModifier import UidSheetInfoModifier


class TagSearchScreen(Screen):
    _box_layout = None
    _float_layout = None
    _grid_layout = None
    _radio_grid_layout = None
    _scroll_view = None
    
    _back_button = None
    _keyword_field = None
    _search_description_button = None
    _search_name_button = None
    _search_label = None
    _search_location_button = None
    
    _current_items = []
    _search_item_widgets = []
    
    _main_screen = None
    
    _uid_sheet_info_modifier = None

    def __init__(self, main_screen):
        super().__init__(name="Tag Searching Screen")
    
        try:
            self._uid_sheet_info_modifier = UidSheetInfoModifier()
        except:
            self._uid_sheet_info_modifier = UidCsvInfoModifier()
        
        self._main_screen = main_screen
        
        self._box_layout = BoxLayout(orientation='vertical', spacing=10)
        self._float_layout = FloatLayout(pos_hint={'top': 0.2})
        self._grid_layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self._radio_grid_layout = GridLayout(cols=3)
        self._scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        
        self._back_button = Button(text="Back", on_press=self.go_back)
        self._keyword_field = TextInput(multiline=False, on_text=self.on_search_query)
        self._search_name_button = ToggleButton(text="by Name", group="search_type", state='down')
        self._search_description_button = ToggleButton(text="by Description", group="search_type")
        self._search_label = Label(text="Enter search keyword")
        self._search_location_button = ToggleButton(text="by Location", group="search_type")
        
        self.add_widget(self._box_layout)
        
        self._box_layout.add_widget(self._back_button)
        self._box_layout.add_widget(self._search_label)
        self._box_layout.add_widget(self._keyword_field)
        self._box_layout.add_widget(self._radio_grid_layout)
        self._box_layout.add_widget(self._float_layout)
        
        self._float_layout.add_widget(self._scroll_view)
        
        self._scroll_view.add_widget(self._grid_layout)
        
        self._radio_grid_layout.add_widget(self._search_name_button)
        self._radio_grid_layout.add_widget(self._search_description_button)
        self._radio_grid_layout.add_widget(self._search_location_button)

    def go_back(self, instance):
        self._main_screen.switch_screen("main_screen")
    
    def on_search_query(self, instance):
        for widget in self._search_item_widgets:
            self._grid_layout.remove_widget(widget)
    
        self._current_items.clear()
        self._search_item_widgets.clear()
        
        regex_query = instance.text + "*"
        
        if self._search_name_button.state == 'down':
            self._current_items = self._uid_sheet_info_modifier.search_for_parts(name=regex_query)
        elif self._search_description_button.state == 'down':
            self._current_items = self._uid_sheet_info_modifier.search_for_parts(description=regex_query)
        elif self._search_location_button.state == 'down':
            self._current_items = self._uid_sheet_info_modifier.search_for_parts(location=regex_query)
        
        for item in self._current_items:
            pass
        
