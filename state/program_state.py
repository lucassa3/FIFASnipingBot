import threading
from view.gui import GUI
from model.selenium_session import SeleniumSession
import time


class State:
    selenium_instance = None
    gui_instance = None
    active_thread = None
    stop_thread_flag = False

    @staticmethod
    def init_resources():
        State.selenium_instance = SeleniumSession(
            "https://www.easports.com/br/fifa/ultimate-team/web-app/#"
        )
        State.gui_instance = GUI()

    @staticmethod
    def stop_thread():
        if State.active_thread:
            State.stop_thread_flag = True

            while True:
                if not State.active_thread.isAlive():
                    break
                time.sleep(1)
                print("Attempting to join routine thread...")

            State.active_thread.join()
            print(f"Thread joined")
            State.stop_thread_flag = False

    @staticmethod
    def switch_thread(func_name, kwargs={}):
        State.stop_thread()
        State.active_thread = threading.Thread(target=func_name, kwargs=kwargs)
        State.active_thread.start()
