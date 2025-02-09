#!/bin/bash

# Wait for the container to fully initialize
sleep 1

# Default the TZ environment variable to UTC.
TZ=${TZ:-UTC}
export TZ

# Set environment variable that holds the Internal Docker IP
INTERNAL_IP=$(ip route get 1 | awk '{print $(NF-2);exit}')
export INTERNAL_IP

# Information output
echo "Running on Debian $(cat /etc/debian_version)"
echo "Current timezone: $(cat /etc/timezone)"
wine --version

## just in case someone removed the defaults.
if [ "${STEAM_USER}" == "" ]; then
   echo -e "steam user is not set.\n"
   echo -e "Using anonymous user.\n"
   STEAM_USER=anonymous
   STEAM_PASS=""
   STEAM_AUTH=""
else
   echo -e "user set to ${STEAM_USER}"
fi

## if auto_update is not set or to 1 update
if [ -z ${AUTO_UPDATE} ] || [ "${AUTO_UPDATE}" == "1" ]; then 
   # Update Source Server
   if [ ! -z ${SRCDS_APPID} ]; then
       if [ "${STEAM_USER}" == "anonymous" ]; then
           ./steamcmd/steamcmd.sh +force_install_dir /home/container +login ${STEAM_USER} ${STEAM_PASS} ${STEAM_AUTH} $( [[ "${WINDOWS_INSTALL}" == "1" ]] && printf %s '+@sSteamCmdForcePlatformType windows' ) +app_update ${SRCDS_APPID} +app_update 1007 $( [[ -z ${SRCDS_BETAID} ]] || printf %s "-beta ${SRCDS_BETAID}" ) $( [[ -z ${SRCDS_BETAPASS} ]] || printf %s "-betapassword ${SRCDS_BETAPASS}" ) $( [[ -z ${HLDS_GAME} ]] || printf %s "+app_set_config 90 mod ${HLDS_GAME}" ) $( [[ -z ${VALIDATE} ]] || printf %s "validate" ) +quit
       else
           numactl --physcpubind=+0 ./steamcmd/steamcmd.sh +force_install_dir /home/container +login ${STEAM_USER} ${STEAM_PASS} ${STEAM_AUTH} $( [[ "${WINDOWS_INSTALL}" == "1" ]] && printf %s '+@sSteamCmdForcePlatformType windows' ) +app_update ${SRCDS_APPID} +app_update 1007 $( [[ -z ${SRCDS_BETAID} ]] || printf %s "-beta ${SRCDS_BETAID}" ) $( [[ -z ${SRCDS_BETAPASS} ]] || printf %s "-betapassword ${SRCDS_BETAPASS}" ) $( [[ -z ${HLDS_GAME} ]] || printf %s "+app_set_config 90 mod ${HLDS_GAME}" ) $( [[ -z ${VALIDATE} ]] || printf %s "validate" ) +quit
       fi
   else
       echo -e "No appid set. Starting Server"
   fi
else
   echo -e "Not updating game server as auto update was set to 0. Starting Server"
fi

if [[ $XVFB == 1 ]]; then
       Xvfb :0 -screen 0 ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT}x${DISPLAY_DEPTH} &
fi

# Install necessary to run packages
echo "First launch will throw some errors. Ignore them"
mkdir -p $WINEPREFIX

# Install vcrun2019
echo "Installing vcrun2019"
winetricks -q vcrun2019

# Check if wine-gecko required and install it if so
if [[ $WINETRICKS_RUN =~ gecko ]]; then
       echo "Installing Gecko"
       WINETRICKS_RUN=${WINETRICKS_RUN/gecko}
       if [ ! -f "$WINEPREFIX/gecko_x86.msi" ]; then
               wget -q -O $WINEPREFIX/gecko_x86.msi http://dl.winehq.org/wine/wine-gecko/2.47.4/wine_gecko-2.47.4-x86.msi
       fi
       if [ ! -f "$WINEPREFIX/gecko_x86_64.msi" ]; then
               wget -q -O $WINEPREFIX/gecko_x86_64.msi http://dl.winehq.org/wine/wine-gecko/2.47.4/wine_gecko-2.47.4-x86_64.msi
       fi
       wine msiexec /i $WINEPREFIX/gecko_x86.msi /qn /quiet /norestart /log $WINEPREFIX/gecko_x86_install.log
       wine msiexec /i $WINEPREFIX/gecko_x86_64.msi /qn /quiet /norestart /log $WINEPREFIX/gecko_x86_64_install.log
fi

# Check if wine-mono required and install it if so
if [[ $WINETRICKS_RUN =~ mono ]]; then
       echo "Installing mono"
       WINETRICKS_RUN=${WINETRICKS_RUN/mono}
       if [ ! -f "$WINEPREFIX/mono.msi" ]; then
               wget -q -O $WINEPREFIX/mono.msi https://dl.winehq.org/wine/wine-mono/9.1.0/wine-mono-9.1.0-x86.msi
       fi
       wine msiexec /i $WINEPREFIX/mono.msi /qn /quiet /norestart /log $WINEPREFIX/mono_install.log
fi

# List and install other packages
for trick in $WINETRICKS_RUN; do
       echo "Installing $trick"
       winetricks -q $trick
done

# Replace Startup Variables
MODIFIED_STARTUP=$(echo ${STARTUP} | sed -e 's/{{/${/g' -e 's/}}/}/g')
echo ":/home/container$ ${MODIFIED_STARTUP}"

# Clean and validate XML file
if [ -f "/home/container/config/SpaceEngineers-Dedicated.cfg" ]; then
    # Remove BOM and ensure no leading whitespace
    sed -i '1s/^\xEF\xBB\xBF//' "/home/container/config/SpaceEngineers-Dedicated.cfg"
    # Ensure XML declaration is first line
    sed -i '/<?xml/!b;1{h;d};1!{x;/<?xml/!p;x}' "/home/container/config/SpaceEngineers-Dedicated.cfg"
    # Remove any empty lines at start of file
    sed -i '/./,$!d' "/home/container/config/SpaceEngineers-Dedicated.cfg"
    # Convert to Unix line endings
    dos2unix "/home/container/config/SpaceEngineers-Dedicated.cfg"
    
    echo "XML file cleaned, checking first line:"
    head -n 1 "/home/container/config/SpaceEngineers-Dedicated.cfg"
fi

python3 /config_parser.py

# Run the Server
eval ${MODIFIED_STARTUP}