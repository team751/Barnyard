import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from sptag.gui.MainScreen import MainScreen
from sptag.gui.TagEditorScreen import TagEditorScreen
from sptag.gui.TagSearchScreen import TagSearchScreen
from sptag.gui.UpdaterScreen import UpdaterScreen


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
		self.screens.append(UpdaterScreen())
		
		for screen in self.screens:
			self.screen_manager.add_widget(screen)
		
		self.screen_manager.current = self.current_screen
		
		self.main_screen.scan_tag()
		
		return self.screen_manager

	def switch_screen(self, screen_name, data=None):
		if screen_name == "register_tag":
			self.current_screen = "Tag Editor Screen"
			self.screens[1].part_init(data)
			self.screens[1].return_to_main_screen = (self.screen_manager.current == "main_screen")
		elif screen_name == "main_screen":
			self.current_screen = "Main Screen"
			self.main_screen.refresh_part_data()
		elif screen_name == "search_tag":
			self.current_screen = "Tag Searching Screen"
			self.screens[2].connected = self.main_screen.connected
		elif screen_name == "update":
			self.current_screen = "Updater Screen"
			self.screens[3].start_update(data)

		self.main_screen.screen_active = (screen_name == "main_screen")
		
		self.screen_manager.current = self.current_screen
		print("current_screen=" + self.current_screen)


if __name__ == '__main__':
	BarnyardApp().run()
