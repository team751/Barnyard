from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagInfoScreen import TagInfoScreen

from tkinter import Button, Label

class MainScreen():
	_current_screen = None
	
	_register_tag_button = None
	_view_tag_button = None
	
	_window = None
	
	def _init_screen_elements(self):
		self._register_tag_button = Button(self._window,
										   text="Register Tag",
										   command=self.register_tag)
		self._view_tag_button = Button(self._window,
									   text="View Tag",
									   command=self.view_tag)
		
		self._register_tag_button.grid(row=0, column=0, pady=(50, 10))
		self._view_tag_button.grid(row=1, column=0, pady=(100, 50))
	
	def __init__(self, window):
		self._window = window
		
		self._init_screen_elements()
	
	def close_current_screen(self):
		self._register_tag_button.grid(row=0, column=0, pady=(100, 10))
		self._view_tag_button.grid(row=1, column=0, pady=(100, 10))
		
		self._current_screen = None
		
	def register_tag(self):
		self._register_tag_button.grid_forget()
		self._view_tag_button.grid_forget()
		
		self._current_screen = TagEditorScreen(self, self._window)
	
	def view_tag(self):
		self._register_tag_button.grid_forget()
		self._view_tag_button.grid_forget()
		
		self._current_screen = TagInfoScreen(self, self._window)
