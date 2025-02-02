import re
import time
import os
import sys

def monitor_log():
    while True:
        if os.path.exists("CoreKeeperServerLog.txt"):
            try:
                with open("CoreKeeperServerLog.txt", "r") as f:
                    content = f.read()
                    match = re.search(r'Started session with Game ID ([a-zA-Z0-9]+)', content)
                    if match:
                        game_id = match.group(1)
                        print("-------------")
                        print(f"Server Game ID: {game_id}")
                        print("-------------")
                        break
            except Exception as e:
                print(f"Error reading log file: {e}", file=sys.stderr)
        
        time.sleep(5)

if __name__ == "__main__":
    monitor_log()