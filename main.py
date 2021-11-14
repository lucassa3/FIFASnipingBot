import threading
import controller.routines as routines
from controller.program_state import ProgramState
        
if __name__ == "__main__":
    ProgramState.init_resources()
    routines.call_login("credentials.txt")
    ProgramState.screen_controller.title("FIFA 22 Bot")
    ProgramState.screen_controller.mainloop()