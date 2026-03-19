
import sys
import os
import time

# Add src to path
sys.path.append(os.getcwd())

from src.logic.background_monitor import BackgroundMonitor

def run_debug_monitor():
    print("Starting Background Monitor in Debug Mode...")
    monitor = BackgroundMonitor()
    monitor.start()
    
    print("Monitor started. Waiting 75 seconds to catch the 60s interval...")
    try:
        # Keep main thread alive
        for i in range(75):
            time.sleep(1)
            if i % 10 == 0:
                print(f"Tick {i}...")
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping monitor...")
        monitor.stop()

if __name__ == "__main__":
    run_debug_monitor()
