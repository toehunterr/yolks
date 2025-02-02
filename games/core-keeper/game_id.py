import re
import time
import os
import sys
import signal

class LogMonitor:
    def __init__(self):
        self.shutdown_requested = False
        signal.signal(signal.SIGTERM, self.handle_sigterm)

    def handle_sigterm(self, signum, frame):
        print("SIGTERM received. Initiating shutdown...", file=sys.stderr)
        self.shutdown_requested = True

    def monitor_log(self):
        start_time = time.time()
        timeout = 180  # 3 minutes
        
        while time.time() - start_time < timeout:
            if self.shutdown_requested:
                print("Shutdown requested. Exiting log monitor.", file=sys.stderr)
                return None
            
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
                            return game_id
                except Exception as e:
                    print(f"Error reading log file: {e}", file=sys.stderr)
            
            time.sleep(5)
        
        print("Timeout reached: Game ID not found", file=sys.stderr)
        return None

    def run(self):
        while not self.shutdown_requested:
            result = self.monitor_log()
            if result:
                break
            
            # Check for shutdown every 30 seconds if no result
            for _ in range(6):  # 6 * 5 = 30 seconds
                if self.shutdown_requested:
                    break
                time.sleep(5)

def main():
    monitor = LogMonitor()
    monitor.run()

if __name__ == "__main__":
    main()