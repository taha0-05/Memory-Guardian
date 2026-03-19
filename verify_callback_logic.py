
import sys
import os

# Add src to path
sys.path.append(os.getcwd())

from src.logic.app_controller import AppController
from src.logic.background_monitor import BackgroundMonitor

# Mock args class
class MockArgs:
    def __init__(self, args_str):
        self.arguments = args_str

def test_callback():
    print("Initializing Controller...")
    controller = AppController()
    
    # Setup test user
    username = "test_callback_user"
    password = "password123"
    
    print("Registering/Login user...")
    try:
        controller.register(username, password)
    except ValueError:
        user = controller.login(username, password)
    
    user_id = controller.current_user.user_id
    
    # Add Item
    print("Adding item 'Callback Item'...")
    categories = controller.get_categories()
    if not categories:
        print("Error: No categories found.")
        return
        
    cat_id = categories[0].category_id
    item_id = controller.add_item(cat_id, "Callback Item")
    print(f"Item ID: {item_id}")
    
    # Get initial score
    pattern = controller.pattern_repo.get_pattern(user_id, item_id)
    initial_score = pattern.current_score if pattern else 0.0
    print(f"Initial Score: {initial_score}")
    
    # Initialize Monitor (No start, we just want the method)
    monitor = BackgroundMonitor()
    
    # Simulate 'Remembered' Callback
    print("Simulating 'Remembered' action...")
    args_str = f"action=remember&item_id={item_id}&user_id={user_id}"
    mock_args = MockArgs(args_str)
    
    monitor._handle_toast_activation(mock_args)
    
    # Check new score
    pattern = controller.pattern_repo.get_pattern(user_id, item_id)
    new_score = pattern.current_score if pattern else 0.0
    print(f"New Score: {new_score}")
    
    if new_score > initial_score:
        print("SUCCESS: Score increased (Remembered)!")
    else:
        print("FAILURE: Score did not increase.")

    # Cleanup
    controller.delete_item(item_id)
    controller.delete_account()

if __name__ == "__main__":
    try:
        test_callback()
    except Exception as e:
        print(f"An error occurred: {e}")
