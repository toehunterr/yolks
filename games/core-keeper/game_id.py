import re
import time
from datetime import datetime
import os

def monitor_log():
    if os.environ.get('GAME_ID') and os.environ.get('GAME_ID').strip():
        print("GAME_ID environment variable is set. Monitoring disabled.")
        return

    start_time = time.time()
    timeout = 180  # 3 minutes

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

    with open("CoreKeeperServerLog.txt", "r") as f:
        f.seek(0, 2)
        game_id = None
        last_echo = 0
        last_file_size = os.path.getsize("CoreKeeperServerLog.txt")
        
        while time.time() - start_time < timeout:
            current_size = os.path.getsize("CoreKeeperServerLog.txt")
            if current_size < last_file_size:
                print("Log file not found, exiting...")
                exit(0)
            last_file_size = current_size
            
            line = f.readline()
            if line:
                if "Started session with Game ID" in line:
                    game_id = re.search(r'Game ID ([a-zA-Z0-9]+)', line).group(1)
                    print(f"\nNew Game ID detected: {game_id}")
            
            if game_id and time.time() - last_echo >= 60:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server GameID is {game_id}")
                last_echo = time.time()
            
            time.sleep(0.1)

if __name__ == "__main__":
    monitor_log()