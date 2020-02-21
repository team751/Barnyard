import kivy
kivy.require("1.11.0")

import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from sptag.gui.MainScreen import MainScreen

class BarnyardApp(App):
	current_screen = "Main Screen"
	screens = []
	screen_manager = None
	
	def build(self):
		self.screen_manager = ScreenManager()

		self.screens.append(MainScreen(self))
		self.screens.append(Tag)

		self.screen_manager.add_widget()

if __name__ == '__main__':
	BarnyardApp().run()
