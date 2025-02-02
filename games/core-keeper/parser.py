import json
import os
from typing import Dict, Any

def parse_world_mode(mode: str) -> int:
    """Convert world mode string to corresponding integer value."""
    mode_mapping = {
        "NORMAL": 0,
        "HARD": 1
    }
    return mode_mapping.get(mode.upper(), int(mode) if mode.isdigit() else 0)

def parse_season_override(season: str) -> int:
    """Convert season string to corresponding integer value."""
    season_mapping = {
        "NONE": -1,
        "EASTER": 1,
        "HALLOWEEN": 2,
        "CHRISTMAS": 3,
        "VALENTINES": 4,
        "ANNIVERSARY": 5,
        "CHERRY BLOSSOM FESTIVAL": 6,
        "LUNAR NEW YEAR": 7
    }
    
    if season.upper() in season_mapping:
        return season_mapping[season.upper()]
    
    # Try to parse as integer if it's a number
    try:
        return int(season)
    except ValueError:
        return -1

def update_config(config_path: str) -> None:
    """Update configuration based on environment variables."""
    # Read existing config
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Mapping of environment variables to config keys and their parser functions
    env_mapping = {
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

    # Update config based on environment variables
    for env_var, (config_key, parser) in env_mapping.items():
        if env_var in os.environ:
            value = os.environ[env_var]
            if env_var == "GAME_ID" and not value:
                config[config_key] = ""
            else:
                config[config_key] = parser(value)

    # Write updated configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    # Print final configuration
    print("Updated configuration:")
    print(json.dumps(config, indent=4))

if __name__ == "__main__":
    config_path = os.path.expanduser("~/container/.config/unity3d/Pugstorm/CoreKeeper/DedicatedServer/ServerConfig.json")
    update_config(config_path)