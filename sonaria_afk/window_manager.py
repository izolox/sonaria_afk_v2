import pygetwindow as gw
import config
import time

class WindowManager:
    def __init__(self, window_name: str) -> None:
        self.window_name = window_name
        self.windows = []
        
        # Grab all windows with the specified name
        _windows = gw.getWindowsWithTitle(self.window_name)
        _window_handles = [window._hWnd for window in _windows]
        
        if config.DEBUG and (not _window_handles or len(_window_handles) == 0):
            print(f"DEBUG: No windows found with the name '{self.window_name}'")
        elif config.DEBUG:
            print(f"DEBUG: Found {len(_window_handles)} windows with the name '{self.window_name}'")
            print(f"DEBUG: Window handles: {_window_handles}")
            
        print("Window manager initialized")
        
        self.windows = _windows
        
    def get_windows(self) -> list:
        return self.windows
    
    def preform_action(self, callback: callable) -> None:
            try:
                for window in self.windows:
                    if window.isMinimized:
                        window.restore()
                        time.sleep(0.5)
                        
                    if not window.isActive: 
                        window.activate()
                        time.sleep(0.5)

                    # Perform the action
                    callback()
                    
                    time.sleep(1)
                    print(f"Performed action on window '{window.title}', {window._hWnd}")
                
            except Exception as e:
                print(f"Error while performing action on window '{window.title}', {window._hWnd}: {e}")
                