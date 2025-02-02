#!/bin/bash

# Path to the Core Keeper server configuration file
CONFIG_PATH=~/container/.config/unity3d/Pugstorm/CoreKeeper/DedicatedServer/ServerConfig.json

# Function to parse world mode
parse_world_mode() {
    local mode="$1"
    case "${mode^^}" in
        NORMAL) echo "Normal (0)" ;;
        HARD) echo "Hard (1)" ;;
        *) echo "$mode" ;;
    esac
}

# Function to parse and modify the configuration file
modify_config() {
    # Check if the configuration file exists
    if [[ ! -f "$CONFIG_PATH" ]]; then
        echo "Error: Configuration file not found at $CONFIG_PATH"
        exit 1
    }

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required but not installed. Please install jq first."
        exit 1
    }

    # Iterate through environment variables to modify settings
    while IFS='=' read -r setting value; do
        # Convert setting to camelCase to match JSON keys
        case "$setting" in
            GAME_ID)
                echo "Updating key: gameId with value: $value"
                jq -r ".gameId = \"$value\"" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            WORLD)
                echo "Updating key: world with value: $value"
                jq -r ".world = $value" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            WORLD_NAME)
                echo "Updating key: worldName with value: $value"
                jq -r ".worldName = \"$value\"" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            WORLD_SEED)
                echo "Updating key: worldSeed with value: $value"
                jq -r ".worldSeed = \"$value\"" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            MAX_PLAYERS)
                echo "Updating key: maxNumberPlayers with value: $value"
                jq -r ".maxNumberPlayers = $value" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            MAX_PACKETS)
                echo "Updating key: maxNumberPacketsSentPerFrame with value: $value"
                jq -r ".maxNumberPacketsSentPerFrame = $value" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            NETWORK_SEND_RATE)
                echo "Updating key: networkSendRate with value: $value"
                jq -r ".networkSendRate = $value" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            WORLD_MODE)
                parsed_mode=$(parse_world_mode "$value")
                echo "Updating key: worldMode with value: $parsed_mode"
                jq -r ".worldMode = $(echo "$parsed_mode" | grep -oE '[0-9]+')" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            SEASON_OVERRIDE)
                echo "Updating key: seasonOverride with value: $value"
                jq -r ".seasonOverride = $value" "$CONFIG_PATH" > "$CONFIG_PATH"
                ;;
            *)
                echo "Skipping unknown setting: $setting"
                ;;
        esac
    done < <(env | grep -E "^(GAME_ID|WORLD|WORLD_NAME|WORLD_SEED|MAX_PLAYERS|MAX_PACKETS|NETWORK_SEND_RATE|WORLD_MODE|SEASON_OVERRIDE)=")

    # Display the final configuration
    echo "Updated configuration:"
    cat "$CONFIG_PATH"
}

# Main script execution
main() {
    # If arguments are provided, set them as environment variables
    if [[ $# -gt 0 ]]; then
        export "$@"
    fi

    # Modify configuration based on environment variables
    modify_config
}

# Run the main function with any provided arguments
main "$@"