import kivy
kivy.require("1.11.0")

import os

from kivy.app import App
from kivy.uix import ScreenManager

from gui.MainScreen import MainScreen

class BarnyardApp(App):
	current_screen = 0
	screens = []
	
	def build(self):
		manager = ScreenManager()
		
		
		mana

if __name__ == '__main__':
    BarnyardApp.run()
