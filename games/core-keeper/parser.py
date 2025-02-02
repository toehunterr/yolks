import json
import os
import time

def parse_world_mode(mode: str) -> int:
    mode = str(mode).upper()
    if mode == "NORMAL": return 0
    if mode == "HARD": return 1
    return int(mode) if mode.isdigit() else 0

def parse_season_override(season: str) -> int:
    season = str(season).upper()
    if season == "NONE": return -1
    if season == "EASTER": return 1
    if season == "HALLOWEEN": return 2
    if season == "CHRISTMAS": return 3
    if season == "VALENTINES": return 4
    if season == "ANNIVERSARY": return 5
    if season == "CHERRY BLOSSOM FESTIVAL": return 6
    if season == "LUNAR NEW YEAR": return 7
    return int(season) if season.isdigit() else -1

def wait_for_config(config_path: str, timeout: int = 300) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(config_path):
            return True
        time.sleep(1)
    return False

def update_config(config_path: str) -> None:
    if not wait_for_config(config_path):
        print(f"Config file not found after waiting: {config_path}")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    env_vars = {
        "GAME_ID": ("gameId", str),
        "WORLD": ("world", int),
        "WORLD_NAME": ("worldName", str),
        "WORLD_SEED": ("worldSeed", str),
        "MAX_PLAYERS": ("maxNumberPlayers", int),
        "MAX_PACKETS": ("maxNumberPacketsSentPerFrame", int),
        "NETWORK_SEND_RATE": ("networkSendRate", int),
        "WORLD_MODE": ("worldMode", parse_world_mode),
        "SEASON_OVERRIDE": ("seasonOverride", parse_season_override)
    }

    for env_var, (config_key, parser) in env_vars.items():
        if env_var in os.environ:
            value = os.environ[env_var]
            try:
                parsed_value = parser(value)
                config[config_key] = parsed_value
                if env_var in ["WORLD_MODE", "SEASON_OVERRIDE"]:
                    print(f"Updating {config_key}: {value} ({parsed_value})")
                else:
                    print(f"Updating {config_key}: {value}")
            except:
                print(f"Error parsing {env_var}")

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    config_path = "/home/container/.config/unity3d/Pugstorm/CoreKeeper/DedicatedServer/ServerConfig.json"
    update_config(config_path)