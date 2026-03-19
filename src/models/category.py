class Category:
    def __init__(self, category_id=None, category_name=None):
        self.category_id = category_id
        self.category_name = category_name

    def __repr__(self):
        return f"<Category(ID={self.category_id}, Name='{self.category_name}')>"
