class User:
    def __init__(self, user_id=None, username=None, created_at=None):
        self.user_id = user_id
        self.username = username
        self.created_at = created_at

    def __repr__(self):
        return f"<User(ID={self.user_id}, Name='{self.username}')>"
