from datetime import datetime

class UserPattern:
    def __init__(self, pattern_id=None, user_id=None, item_id=None, last_remembered=None, last_forgotten=None, forget_count=0, current_score=0.0):
        self.pattern_id = pattern_id
        self.user_id = user_id
        self.item_id = item_id
        self.last_remembered = last_remembered
        self.last_forgotten = last_forgotten
        self.forget_count = forget_count
        self.current_score = current_score

    def mark_forgotten(self):
        self.last_forgotten = datetime.now()
        self.forget_count += 1
    
    def mark_remembered(self):
        self.last_remembered = datetime.now()
        # Reward: Reduce the 'forget count' so the penalty decreases over time.
        if self.forget_count > 0:
            self.forget_count -= 1

    def __repr__(self):
        return f"<Pattern(User={self.user_id}, Item={self.item_id}, ForgetCount={self.forget_count})>"
