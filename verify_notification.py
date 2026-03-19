
import sys
import os
import time

# Add src to path
sys.path.append(os.getcwd())

from src.logic.app_controller import AppController
from src.logic.background_monitor import BackgroundMonitor

def test_notification():
    print("Initializing Controller...")
    controller = AppController()
    
    # Setup test user
    username = "test_notify_user"
    password = "password123"
    
    print("Registering/Login user...")
    try:
        controller.register(username, password)
    except ValueError:
        user = controller.login(username, password)
    
    user_id = controller.current_user.user_id
    print(f"User ID: {user_id}")
    
    # Add Item
    print("Adding item 'Test Memory'...")
    categories = controller.get_categories()
    if not categories:
        print("Error: No categories found.")
        return
        
    cat_id = categories[0].category_id
    try:
        item_id = controller.add_item(cat_id, "Test Memory")
    except:
        # Get existing
        items = controller.item_repo.get_items_by_user(user_id)
        item_id = next((i.item_id for i in items if i.item_name == "Test Memory"), None)
        
    print(f"Item ID: {item_id}")
    
    # Check initial score
    pattern = controller.pattern_repo.get_pattern(user_id, item_id)
    initial_score = pattern.current_score if pattern else 0.0
    print(f"Initial Score: {initial_score}")
    
    # Initialize Monitor
    print("Initializing Monitor...")
    monitor = BackgroundMonitor()
    
    # Send Notification
    print("Sending Notification... Please click 'I Remembered' in the toast!")
    monitor.send_notification("Test Memory", "Do you remember this?", item_id, user_id)
    
    # Wait for interaction
    print("Waiting 15 seconds for interaction...")
    time.sleep(15)
    
    # Check new score
    pattern = controller.pattern_repo.get_pattern(user_id, item_id)
    new_score = pattern.current_score if pattern else 0.0
    print(f"New Score: {new_score}")
    
    if new_score > initial_score:
        print("SUCCESS: Score increased!")
    elif new_score == initial_score:
        print("WARNING: Score unchanged. Did you click the button?")
    else:
        print("FAILURE: Score decreased?")

if __name__ == "__main__":
    try:
        test_notification()
    except Exception as e:
        print(f"An error occurred: {e}")
