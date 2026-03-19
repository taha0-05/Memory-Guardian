from src.database.db_manager import DatabaseManager
from src.database.repositories import UserRepository, ItemRepository, CategoryRepository, PatternRepository
from src.models.user import User
from src.models.item import Item

import hashlib

class AppController:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.user_repo = UserRepository(self.db_manager)
        self.item_repo = ItemRepository(self.db_manager)
        self.category_repo = CategoryRepository(self.db_manager)
        self.pattern_repo = PatternRepository(self.db_manager)
        self.current_user = None

    def _hash_password(self, password):
        # fast check/hashing
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        user = self.user_repo.get_user_by_name(username)
        # 1. Check if user exists (DB might return case-insensitive match)
        if not user:
            raise ValueError("User not found. Please re-enter username and password.")
        
        # 2. Enforce Strict Case Sensitivity
        if user.username != username:
            raise ValueError("User not found. Please re-enter username and password.")
            
        # 3. Verify password
        input_hash = self._hash_password(password)
        if getattr(user, 'password_hash', None) != input_hash:
            raise ValueError("Invalid password.")
            
        self.current_user = user
        return user

    def register(self, username, password):
        if self.user_repo.get_user_by_name(username):
            raise ValueError("Username already taken.")
            
        password_hash = self._hash_password(password)
        user_id = self.user_repo.create_user(username, password_hash)
        
        # Log them in automatically
        self.current_user = self.user_repo.get_user_by_name(username)
        return self.current_user

    def get_categories(self):
        return self.category_repo.get_all_categories()

    def add_item(self, category_id, item_name, description=""):
        if not self.current_user:
            raise ValueError("No user logged in")
        
        new_item = Item(
            user_id=self.current_user.user_id,
            category_id=category_id,
            item_name=item_name,
            description=description
        )
        return self.item_repo.add_item(new_item)

    def get_user_items(self):
        if not self.current_user:
            return []
        items = self.item_repo.get_items_by_user(self.current_user.user_id)
        # Check patterns for each item
        for item in items:
            pattern = self.pattern_repo.get_pattern(self.current_user.user_id, item.item_id)
            # Monkey-patching status onto the item object for UI convenience
            # In a strict architecture, we'd return a DTO (Data Transfer Object)
            from src.logic.prediction_engine import PredictionEngine
            retention, status_text = PredictionEngine.calculate_retention(pattern)
            item.status = status_text
            item.retention = retention # Storing float if we want to sort by it later
            
        return items

    def delete_item(self, item_id):
        if not self.current_user:
            raise ValueError("No user logged in")
        self.pattern_repo.delete_patterns_for_item(item_id, self.current_user.user_id)
        self.item_repo.delete_item(item_id, self.current_user.user_id)

    def rename_item(self, item_id, new_name):
        if not self.current_user:
            raise ValueError("No user logged in")
        if not new_name or not new_name.strip():
             raise ValueError("New name cannot be empty")
        self.item_repo.rename_item(item_id, self.current_user.user_id, new_name.strip())

    def delete_account(self):
        if not self.current_user:
            raise ValueError("No user logged in")
        
        user_id = self.current_user.user_id
        # Cascade delete manually
        self.pattern_repo.delete_all_patterns_for_user(user_id)
        self.item_repo.delete_all_items_for_user(user_id)
        self.user_repo.delete_user(user_id)
        
        self.current_user = None

    def mark_forgotten(self, item_id, user_id=None):
        if user_id is None:
             if not self.current_user:
                 raise ValueError("No user logged in and no user_id provided")
             user_id = self.current_user.user_id

        # Logic to update pattern when user forgot an item
        pattern = self.pattern_repo.get_pattern(user_id, item_id)
        if not pattern:
            # Create new pattern entry if not exists
            from src.models.pattern import UserPattern
            pattern = UserPattern(user_id=user_id, item_id=item_id)
        
        pattern.mark_forgotten()
        
        # GRADUAL LOGIC: Decrease score by 20, min 0
        pattern.current_score = max(0.0, pattern.current_score - 20.0)
        
        self.pattern_repo.update_pattern(pattern)

    def mark_remembered(self, item_id, user_id=None):
         # Logic to update pattern when user remembered an item
        if user_id is None:
             if not self.current_user:
                 raise ValueError("No user logged in and no user_id provided")
             user_id = self.current_user.user_id

        pattern = self.pattern_repo.get_pattern(user_id, item_id)
        if not pattern:
             # Create new pattern entry if not exists (Fix for "New Item" not updating)
             from src.models.pattern import UserPattern
             pattern = UserPattern(user_id=user_id, item_id=item_id)

        pattern.mark_remembered()
        
        # GRADUAL LOGIC: Increase score by 15, max 100
        pattern.current_score = min(100.0, pattern.current_score + 15.0)
        
        self.pattern_repo.update_pattern(pattern)

    def close(self):
        self.db_manager.close()
