
import sys
import os
import time

# Add src to path
sys.path.append(os.getcwd())

from src.logic.app_controller import AppController
from src.logic.prediction_engine import PredictionEngine

def check_items():
    print("Initializing Controller...")
    controller = AppController()
    
    users = controller.user_repo.get_all_users()
    print(f"Found {len(users)} users.")
    
    for user in users:
        print(f"\nUser: {user.username} (ID: {user.user_id})")
        items = controller.item_repo.get_items_by_user(user.user_id)
        if not items:
            print("  No items found.")
            continue
            
        for item in items:
            pattern = controller.pattern_repo.get_pattern(user.user_id, item.item_id)
            if pattern:
                retention, status = PredictionEngine.calculate_retention(pattern)
                print(f"  Item: '{item.item_name}' (ID: {item.item_id})")
                print(f"    - Score: {pattern.current_score}")
                print(f"    - Retention: {retention:.2f}")
                print(f"    - Status: {status}")
                
                # Check criteria
                interval = 0
                if retention <= 0.30: interval = 60
                elif retention < 0.50: interval = 300
                elif retention < 0.75: interval = 900
                
                if interval > 0:
                    print(f"    -> SHOULD NOTIFY (Interval: {interval}s)")
                else:
                    print("    -> No notification expected (Retention >= 0.75)")
            else:
                print(f"  Item: '{item.item_name}' - No pattern data.")

if __name__ == "__main__":
    check_items()
