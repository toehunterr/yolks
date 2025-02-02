import re
import time
from datetime import datetime
import os

def monitor_log():
    start_time = time.time()
    timeout = 180
    while time.time() - start_time < timeout:
        try:
            if os.path.exists("CoreKeeperServerLog.txt"):
                break
            print("Waiting for log file to be created...")
            time.sleep(5)
        except Exception as e:
            print(f"Error checking for log file: {e}")
            time.sleep(5)
    else:
        print("Timeout: File not found after 3 minutes")
        exit(1)

    seen_markers = 0
    game_id = None
    timescale_seen = False
    game_id_time = None
    
    with open("CoreKeeperServerLog.txt", "r") as f:
        while time.time() - start_time < timeout:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
                
            if "Started session with Game ID" in line:
                game_id = re.search(r'Game ID ([a-zA-Z0-9]+)', line).group(1)
                game_id_time = time.time()
            
            if "Adding marker for" in line:
                seen_markers += 1
                
            if "timescale = 0" in line:
                timescale_seen = True

            current_time = time.time()
            if game_id and game_id_time and (current_time - game_id_time >= 15):
                print(f"Server GameID is {game_id}")
                if seen_markers >= 8 and timescale_seen:
                    exit(0)
                else:
                    exit(1)

if __name__ == "__main__":
    monitor_log()