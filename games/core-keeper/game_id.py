import re
import time
import os
import sys
import signal

def monitor_log():
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
                    signal.pause()
        except Exception as e:
            print(f"Error reading log file: {e}", file=sys.stderr)

if __name__ == "__main__":
    while True:
        monitor_log()
        time.sleep(5)