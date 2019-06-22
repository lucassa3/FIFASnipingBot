import threading
from screens import ScreenController
from selenium_session import SeleniumSession

class ProgramState():
	selenium_instance = None
	screen_controller = None
	active_thread = None

	def init_resources():
		ProgramState.selenium_instance = SeleniumSession("https://www.easports.com/br/fifa/ultimate-team/web-app/#")
		ProgramState.screen_controller = ScreenController()

	def stop_thread():
		if ProgramState.active_thread:
			ProgramState.active_thread.join()

	def switch_thread(func_name, kwargs):
		ProgramState.stop_thread()
		ProgramState.active_thread = threading.Thread(target=func_name, kwargs=kwargs)
		ProgramState.active_thread.start()