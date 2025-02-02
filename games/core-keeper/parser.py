import json
import os
import time

def parse_world_mode(mode: str) -> int:
    mode = str(mode).strip().upper()
    modes = {
        "NORMAL": 0,
        "HARD": 1
    }
    return modes.get(mode, int(mode) if mode.isdigit() else 0)

def parse_season_override(season: str) -> int:
    season = str(season).strip().upper()
    seasons = {
        "NONE": -1,
        "EASTER": 1,
        "HALLOWEEN": 2,
        "CHRISTMAS": 3,
        "VALENTINES": 4,
        "ANNIVERSARY": 5,
        "CHERRY BLOSSOM FESTIVAL": 6,
        "LUNAR NEW YEAR": 7
    }
    return seasons.get(season, int(season) if season.isdigit() else -1)

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
            except Exception as e:
                print(f"Error parsing {env_var}: {e}")

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    config_path = "/home/container/.config/unity3d/Pugstorm/CoreKeeper/DedicatedServer/ServerConfig.json"
    update_config(config_path)