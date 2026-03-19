
from windows_toasts import InteractableWindowsToaster, Toast, ToastButton

def test_simple_toast():
    print("Attempting to send a simple toast...")
    try:
        # Match the shortcut name "Memory Guardian"
        toaster = InteractableWindowsToaster('Memory Guardian')
        
        new_toast = Toast()
        new_toast.text_fields = ["This is a test notification", "If you see this, notifications work!"]
        
        btn = ToastButton("Click Me", "action=test")
        new_toast.AddAction(btn)
        
        toaster.show_toast(new_toast)
        print("Toast sent command executed.")
    except Exception as e:
        print(f"Error sending toast: {e}")

if __name__ == "__main__":
    test_simple_toast()
