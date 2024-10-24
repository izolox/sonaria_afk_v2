from sonaria_afk import *
from pynput.keyboard import Controller
import time
import config

# Create keyboard controller
controller = Controller()

def afk_action():
    time.sleep(1)
    controller.press('e')

def main():
    process_start = time.time()
    interval_timer = time.time()
                                                    
    # Create telemetry handler
    telemetry = TelemetryHandler(config.WEBHOOK_URL)
    
    # Create window manager
    window_manager = WindowManager(config.WINDOW_NAME)
    windows = window_manager.get_windows()
    
    if len(windows) < 2:
        print("Not enough windows found, exiting...")
        return
    
    while True:
        window_manager.preform_action(afk_action)
        
        if time.time() - interval_timer >= (60 * 10):
            telemetry.send_telemetry()
            interval_timer = time.time()
        
        time.sleep(60 * 5)
        

if __name__ == "__main__":
    main()