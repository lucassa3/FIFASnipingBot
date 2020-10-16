import threading
import routines as routines
from program_state import ProgramState
        
if __name__ == "__main__":
    ProgramState.init_resources()
    routines.call_login("credentials.txt")
    ProgramState.screen_controller.title("FIFA 21 Bot")
    ProgramState.screen_controller.mainloop()