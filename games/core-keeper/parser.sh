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

# Function to parse season override
parse_season_override() {
    local season="$1"
    case "${season^^}" in
        NONE) echo "-1" ;;
        EASTER) echo "1" ;;
        HALLOWEEN) echo "2" ;;
        CHRISTMAS) echo "3" ;;
        VALENTINES) echo "4" ;;
        ANNIVERSARY) echo "5" ;;
        CHERRY BLOSSOM FESTIVAL) echo "6" ;;
        LUNAR NEW YEAR) echo "7" ;;
        *) 
            if [[ "$season" =~ ^-?[0-9]+$ ]]; then
                echo "$season"
            else
                echo "-1"
            fi
            ;;
    esac
}


# Function to parse and modify the configuration file
modify_config() {
    # Check if the configuration file exists
    if [[ ! -f "$CONFIG_PATH" ]]; then
        echo "Error: Configuration file not found at $CONFIG_PATH"
        exit 1
    fi

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required but not installed. Please install jq first."
        exit 1
    fi

    # Iterate through environment variables to modify settings
    while IFS='=' read -r setting value; do
        # Convert setting to camelCase to match JSON keys
        case "$setting" in
            GAME_ID)
                echo "Updating key: gameId with value: $value"
                jq -i ".gameId = \"$value\"" "$CONFIG_PATH"
                ;;
            WORLD)
                echo "Updating key: world with value: $value"
                jq -i ".world = $value" "$CONFIG_PATH"
                ;;
            WORLD_NAME)
                echo "Updating key: worldName with value: $value"
                jq -i ".worldName = \"$value\"" "$CONFIG_PATH"
                ;;
            WORLD_SEED)
                echo "Updating key: worldSeed with value: $value"
                jq -i ".worldSeed = \"$value\"" "$CONFIG_PATH"
                ;;
            MAX_PLAYERS)
                echo "Updating key: maxNumberPlayers with value: $value"
                jq -i ".maxNumberPlayers = $value" "$CONFIG_PATH"
                ;;
            MAX_PACKETS)
                echo "Updating key: maxNumberPacketsSentPerFrame with value: $value"
                jq -i ".maxNumberPacketsSentPerFrame = $value" "$CONFIG_PATH"
                ;;
            NETWORK_SEND_RATE)
                echo "Updating key: networkSendRate with value: $value"
                jq -i ".networkSendRate = $value" "$CONFIG_PATH"
                ;;
            WORLD_MODE)
                parsed_mode=$(parse_world_mode "$value")
                echo "Updating key: worldMode with value: $parsed_mode"
                jq -i ".worldMode = $(echo "$parsed_mode" | grep -oE '[0-9]+')" "$CONFIG_PATH"
                ;;
            SEASON_OVERRIDE)
                parsed_season=$(parse_season_override "$value")
                echo "Updating key: seasonOverride with value: $parsed_season"
                jq -i ".seasonOverride = $parsed_season" "$CONFIG_PATH"
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