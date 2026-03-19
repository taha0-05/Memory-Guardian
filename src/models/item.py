class Item:
    def __init__(self, item_id=None, user_id=None, category_id=None, item_name=None, description=None, is_active=True, created_at=None):
        self.item_id = item_id
        self.user_id = user_id
        self.category_id = category_id
        self.item_name = item_name
        self.description = description
        self.is_active = is_active
        self.created_at = created_at

    def __repr__(self):
        return f"<Item(ID={self.item_id}, Name='{self.item_name}', Category={self.category_id})>"
