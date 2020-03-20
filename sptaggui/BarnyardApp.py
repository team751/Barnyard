import kivy
kivy.require("1.9.1")

import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from sptag.gui.MainScreen import MainScreen
from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagSearchScreen import TagSearchScreen


class BarnyardApp(App):
	current_screen = "Main Screen"
	main_screen = None
	screens = []
	screen_manager = None
	
	def build(self):
		self.screen_manager = ScreenManager()
		self.main_screen = MainScreen(self)

		self.screens.append(self.main_screen)
		self.screens.append(TagEditorScreen(self.main_screen))
		self.screens.append(TagSearchScreen(self.main_screen))
		
		for screen in self.screens:
		    self.screen_manager.add_widget(screen)
		
		self.screen_manager.current = self.current_screen
		
		self.main_screen.scan_tag()
		
		return self.screen_manager

	def switch_screen(self, screen_name, data=None):
		if screen_name == "register_tag":
			self.current_screen = "Tag Editor Screen"
			self.screens[1].part_init(data)
		elif screen_name == "main_screen":
			self.current_screen = "Main Screen"
			self.main_screen.refresh_part_data()
		elif screen_name == "search_tag":
		    self.current_screen = "Tag Searching Screen"
		
		self.screen_manager.current = self.current_screen
		print("current_screen=" + self.current_screen)
     
if __name__ == '__main__':
	BarnyardApp().run()
