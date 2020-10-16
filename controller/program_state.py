import threading
from view.screen_management import ScreenManager
from model.selenium_session import SeleniumSession
import time

class ProgramState():
	selenium_instance = None
	screen_controller = None
	active_thread = None
	stop_thread_flag = False

	@staticmethod
	def init_resources():
		ProgramState.selenium_instance = SeleniumSession("https://www.easports.com/br/fifa/ultimate-team/web-app/#")
		ProgramState.screen_controller = ScreenManager()

	@staticmethod
	def stop_thread():
		if ProgramState.active_thread:
			ProgramState.stop_thread_flag = True

			while True:
				if not ProgramState.active_thread.isAlive():
					break
				time.sleep(1)
				print(ProgramState.active_thread.isAlive())

			print(f"dando join na thread")
			ProgramState.active_thread.join()
			print(f"dei join na thread")
			ProgramState.stop_thread_flag = False
	
	@staticmethod
	def switch_thread(func_name, kwargs={}):
		ProgramState.stop_thread()
		ProgramState.active_thread = threading.Thread(target=func_name, kwargs=kwargs)
		ProgramState.active_thread.start()