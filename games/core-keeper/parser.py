import json
import os

def parse_world_mode(mode: str) -> int:
    mode = str(mode).strip()
    modes = {
        "Normal": 0,
        "Hard": 1
    }
    return modes.get(mode, int(mode) if mode.isdigit() else 0)

def parse_season_override(season: str) -> int:
    season = str(season).strip()
    seasons = {
        "None": -1,
        "Easter": 1,
        "Halloween": 2,
        "Christmas": 3,
        "Valentines": 4,
        "Anniversary": 5,
        "Cherry Blossom Festival": 6,
        "Lunar New Year": 7
    }
    return seasons.get(season, int(season) if season.isdigit() else -1)

def update_config(config_path: str) -> None:
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}")
        return

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

    updated = False
    for env_var, (config_key, parser) in env_vars.items():
        if env_var in os.environ:
            value = os.environ[env_var]
            try:
                parsed_value = parser(value)
                if config.get(config_key) != parsed_value:
                    config[config_key] = parsed_value
                    print(f"Updating {config_key}: {value} ({parsed_value})")
                    updated = True
            except Exception as e:
                print(f"Error parsing {env_var}: {e}")

    if updated:
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            print("Config updated successfully")
        except Exception as e:
            print(f"Error writing config: {e}")

if __name__ == "__main__":
    config_path = "/home/container/.config/unity3d/Pugstorm/CoreKeeper/DedicatedServer/ServerConfig.json"
    update_config(config_path)