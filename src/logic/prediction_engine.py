from datetime import datetime, timedelta
import math

class PredictionEngine:
    @staticmethod
    def calculate_retention(pattern):
        # Gradual Score Logic (Gamified)
        # We process 'Decay' on read.
        
        if not pattern:
            return 0.0, "New Item"
            
        score = pattern.current_score
        
        # Calculate Decay since last interaction
        # Decay speed depends on difficulty (forget_count)
        # Stable item (low forget count) decays 5% per day
        # Unstable item (high forget count) decays 20% per day
        last_interaction = pattern.last_remembered or pattern.last_forgotten or datetime.now()
        hours_elapsed = (datetime.now() - last_interaction).total_seconds() / 3600
        
        # Base decay rate per hour
        decay_rate_per_hour = 0.5 + (pattern.forget_count * 0.2) # Increases with difficulty
        
        # Apply decay
        # Note: We don't save this decay back to DB instantly on every read (performance), 
        # but the UI shows the decayed value. The 'real' update happens on action.
        effective_score = max(0.0, score - (hours_elapsed * decay_rate_per_hour))
        
        retention = effective_score / 100.0
        percentage = int(effective_score)
        
        if percentage <= 20: 
            status = f"Critical ({percentage}%)"
        elif percentage < 50:
            status = f"Weak ({percentage}%)"
        elif percentage < 75:
            status = f"Growing ({percentage}%)"
        else:
            status = f"Strong ({percentage}%)"
            
        return retention, status

    @staticmethod
    def get_status(pattern):
        # Wrapper for backward compatibility if needed, but we'll use the new tuple return
        _, status = PredictionEngine.calculate_retention(pattern)
        return status
