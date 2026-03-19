import threading
import time
# from plyer import notification # Removed
import pystray
from PIL import Image, ImageDraw
from src.logic.app_controller import AppController
from src.logic.prediction_engine import PredictionEngine

from windows_toasts import InteractableWindowsToaster, Toast, ToastButton, ToastActivatedEventArgs

class BackgroundMonitor:
    def __init__(self):
        self.running = False
        self.monitor_thread = None
        self.tray_thread = None
        self.icon = None
        self.notification_history = {} # Maps item_id -> last_notification_timestamp
        
        # Initialize Windows Toaster for interactive notifications
        # InteractableWindowsToaster is required for buttons
        self.toaster = InteractableWindowsToaster('Memory Guardian')

    def create_image(self):
        # Generate an image for the icon (Blue box with White 'M')
        width = 64
        height = 64
        color1 = "#0A84FF" # Memory Guardian Blue
        color2 = "white"
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill=color2)
        
        return image

    def start(self):
        if self.running:
            return
        self.running = True
        
        # Start Monitor Logic
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start System Tray Icon
        self.tray_thread = threading.Thread(target=self._tray_loop, daemon=True)
        self.tray_thread.start()

    def stop(self):
        self.running = False
        if self.icon:
            self.icon.stop()

    def _tray_loop(self):
        # Set AppUserModelID to ensure notifications persist in Action Center
        import ctypes
        app_id = 'mycompany.memoryguardian.app.1.0' # Arbitrary unique ID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        # Define menu
        menu = pystray.Menu(
            pystray.MenuItem("Memory Guardian Active", lambda: None, enabled=False),
        )
        
        self.icon = pystray.Icon("Memory Guardian", self.create_image(), "Memory Guardian", menu)
        self.icon.run()

    def _monitor_loop(self):
        # Create a new controller for this thread
        controller = AppController()

        while self.running:
            try:
                # Fetch all users to monitor
                users = controller.user_repo.get_all_users()
                
                current_time = time.time()
                
                for user in users:
                    items = controller.item_repo.get_items_by_user(user.user_id)
                    
                    for item in items:
                        pattern = controller.pattern_repo.get_pattern(user.user_id, item.item_id)
                        retention, status = PredictionEngine.calculate_retention(pattern)
                        
                        interval = 0
                        message = ""
                        
                        # Logic for Intervals vs Memory Strength
                        username = user.username

                        if retention <= 0.30: # Critical (< 30%)
                             interval = 60 # 1 minute
                             message = f"{username}, you're most probably going to forget your '{item.item_name}'"
                        elif retention < 0.50: # Weak (30% - 50%)
                            interval = 300 # 5 minutes
                            message = f"{username}, you're likely to forget '{item.item_name}' soon. Review it!"
                        elif retention < 0.75: # Growing (50% - 75%)
                            interval = 900 # 15 minutes
                            message = f"Keep it fresh, {username}! Review '{item.item_name}' to make it strong."
                        
                        if interval > 0:
                            last_time = self.notification_history.get(item.item_id, 0)
                            if current_time - last_time >= interval:
                                self.send_notification(item.item_name, message, item.item_id, user.user_id)
                                self.notification_history[item.item_id] = current_time
                        
            except Exception as e:
                print(f"Background Monitor Error: {e}")

            
            # Sleep Loop (Check every 10s)
            for _ in range(10): 
                if not self.running: break
                time.sleep(1)

    def send_notification(self, title, message, item_id, user_id):
        try:
            new_toast = Toast()
            new_toast.text_fields = [message] # First line is title/header usually, but message works better as main text here
            new_toast.launch_action = f"action=view&item_id={item_id}&user_id={user_id}"
            
            # Interactive Buttons
            btn_remember = ToastButton("I Remembered", f"action=remember&item_id={item_id}&user_id={user_id}")
            btn_forgot = ToastButton("I Forgot", f"action=forgot&item_id={item_id}&user_id={user_id}")
            
            new_toast.AddAction(btn_remember)
            new_toast.AddAction(btn_forgot)
            
            new_toast.on_activated = self._handle_toast_activation
            self.toaster.show_toast(new_toast)
        except Exception as e:
            print(f"Toast Notification Failed: {e}")
            # Fallback to tray if toaster fails
            if self.icon:
                 self.icon.notify(message, f"Memory Guardian: {title}")

    def _handle_toast_activation(self, activatedEventArgs: ToastActivatedEventArgs):
        # Callback runs in a separate thread usually
        try:
            args = activatedEventArgs.arguments
            # Parse arguments (naive parsing)
            params = {}
            if args:
                for part in args.split('&'):
                    k, v = part.split('=')
                    params[k] = v
            
            action = params.get('action')
            item_id = int(params.get('item_id')) if params.get('item_id') else None
            user_id = int(params.get('user_id')) if params.get('user_id') else None
            
            if action and item_id and user_id:
                # Create a fresh controller for this operation
                controller = AppController()
                
                if action == 'remember':
                    controller.mark_remembered(item_id, user_id)
                    # Optional: Show confirmation toast?
                    # self.send_notification("Updated", "Great! Keep it up!", item_id, user_id) 
                
                elif action == 'forgot':
                    controller.mark_forgotten(item_id, user_id)
                    
        except Exception as e:
            print(f"Activation Callback Error: {e}")
