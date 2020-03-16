import kivy
kivy.require("1.11.0")

import _thread
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from sptag.gui.MainScreen import MainScreen
from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagInfoScreen import TagInfoScreen


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
		self.screens.append(TagInfoScreen(self.main_screen))

		self.screen_manager.current = self.current_screen
		
if __name__ == '__main__':
	BarnyardApp().run()
