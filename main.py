import threading
import controller.routines as routines
from state.program_state import State
        
if __name__ == "__main__":
    State.init_resources()
    routines.call_login("credentials.txt")
    State.gui_instance.title("FIFA 22 Bot")
    State.gui_instance.mainloop()