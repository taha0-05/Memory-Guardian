from src.models.user import User
from src.models.item import Item
from src.models.category import Category
from src.models.pattern import UserPattern
from src.database.db_manager import DatabaseManager

class UserRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_user(self, username, password_hash):
        query = "INSERT INTO Users (Username, PasswordHash) OUTPUT INSERTED.UserID VALUES (?, ?)"
        # Use fetch_one because we expect a result from OUTPUT
        row = self.db.fetch_one(query, (username, password_hash))
        return row[0] if row else None

    def get_user_by_name(self, username):
        query = "SELECT UserID, Username, CreatedAt, PasswordHash FROM Users WHERE Username = ?"
        row = self.db.fetch_one(query, (username,))
        if row:
            user = User(user_id=row[0], username=row[1], created_at=row[2])
            user.password_hash = row[3] # Attach hash to user object for controller to verify
            return user
        return None

    def get_user_by_id(self, user_id):
        query = "SELECT UserID, Username, CreatedAt FROM Users WHERE UserID = ?"
        row = self.db.fetch_one(query, (user_id,))
        if row:
            return User(user_id=row[0], username=row[1], created_at=row[2])
        return None

    def get_all_users(self):
        query = "SELECT UserID, Username, CreatedAt FROM Users"
        rows = self.db.fetch_all(query)
        users = []
        for row in rows:
            users.append(User(user_id=row[0], username=row[1], created_at=row[2]))
        return users

    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE UserID = ?"
        self.db.execute_commit(query, (user_id,))

class CategoryRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_all_categories(self):
        query = "SELECT CategoryID, CategoryName FROM Categories"
        rows = self.db.fetch_all(query)
        categories = []
        for row in rows:
            categories.append(Category(category_id=row[0], category_name=row[1]))
        return categories

class ItemRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_item(self, item: Item):
        query = """
            INSERT INTO Items (UserID, CategoryID, ItemName, Description, IsActive)
            OUTPUT INSERTED.ItemID
            VALUES (?, ?, ?, ?, ?)
        """
        params = (item.user_id, item.category_id, item.item_name, item.description, item.is_active)
        row = self.db.fetch_one(query, params)
        return row[0] if row else None

    def get_items_by_user(self, user_id):
        query = """
            SELECT i.ItemID, i.UserID, i.CategoryID, i.ItemName, i.Description, i.IsActive, i.CreatedAt
            FROM Items i
            WHERE i.UserID = ?
        """
        rows = self.db.fetch_all(query, (user_id,))
        items = []
        for row in rows:
            items.append(Item(
                item_id=row[0], user_id=row[1], category_id=row[2],
                item_name=row[3], description=row[4], is_active=row[5], created_at=row[6]
            ))
        return items

    def delete_item(self, item_id, user_id):
        # First check if item belongs to user
        query = "DELETE FROM Items WHERE ItemID = ? AND UserID = ?"
        self.db.execute_commit(query, (item_id, user_id))

    def delete_all_items_for_user(self, user_id):
        query = "DELETE FROM Items WHERE UserID = ?"
        self.db.execute_commit(query, (user_id,))

    def rename_item(self, item_id, user_id, new_name):
        query = "UPDATE Items SET ItemName = ? WHERE ItemID = ? AND UserID = ?"
        self.db.execute_commit(query, (new_name, item_id, user_id))

class PatternRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_pattern(self, user_id, item_id):
        query = """
            SELECT PatternID, UserID, ItemID, LastRememberedDate, LastForgottenDate, ForgetCount, CurrentScore
            FROM UserPatterns
            WHERE UserID = ? AND ItemID = ?
        """
        row = self.db.fetch_one(query, (user_id, item_id))
        if row:
            return UserPattern(
                pattern_id=row[0], user_id=row[1], item_id=row[2],
                last_remembered=row[3], last_forgotten=row[4], forget_count=row[5],
                current_score=row[6]
            )
        return None

    def update_pattern(self, pattern: UserPattern):
        if pattern.pattern_id:
            query = """
                UPDATE UserPatterns
                SET LastRememberedDate = ?, LastForgottenDate = ?, ForgetCount = ?, CurrentScore = ?
                WHERE PatternID = ?
            """
            params = (pattern.last_remembered, pattern.last_forgotten, pattern.forget_count, pattern.current_score, pattern.pattern_id)
            self.db.execute_commit(query, params)
        else:
            query = """
                INSERT INTO UserPatterns (UserID, ItemID, LastRememberedDate, LastForgottenDate, ForgetCount, CurrentScore)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (pattern.user_id, pattern.item_id, pattern.last_remembered, pattern.last_forgotten, pattern.forget_count, pattern.current_score)
            self.db.execute_commit(query, params)

    def delete_patterns_for_item(self, item_id, user_id):
        query = "DELETE FROM UserPatterns WHERE ItemID = ? AND UserID = ?"
        self.db.execute_commit(query, (item_id, user_id))

    def delete_all_patterns_for_user(self, user_id):
        query = "DELETE FROM UserPatterns WHERE UserID = ?"
        self.db.execute_commit(query, (user_id,))
