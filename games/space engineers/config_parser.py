#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

def update_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    session = root.find('SessionSettings')
    if session is not None:
        session.find('GameMode').text = os.environ['SERVER_MODE']
        session.find('MaxPlayers').text = os.environ['MAX_PLAYERS']
        session.find('AutoSaveInMinutes').text = os.environ['SAVE_INTERVAL']
        session.find('EnableSaving').text = os.environ['SAVE_ENABLED']
        session.find('ExperimentalMode').text = os.environ['EXPERIMENTAL_ENABLED']
        session.find('EnableIngameScripts').text = os.environ['INGAMESCRIPTS_ENABLED']
    
    # Only this path needs Wine Z: drive format for the game server
    update_path = f"Z:/home/container/config/Saves/{os.environ['WORLD_NAME']}/Sandbox.sbc"
    root.find('LoadWorld').text = update_path
    
    root.find('ServerPort').text = os.environ['SERVER_PORT']
    root.find('SteamPort').text = os.environ['STEAM_PORT']
    root.find('ServerName').text = os.environ['SERVER_NAME']
    root.find('WorldName').text = os.environ['WORLD_NAME']
    root.find('ServerDescription').text = os.environ['SERVER_DESC']
    root.find('RemoteApiEnabled').text = os.environ['REMOTEAPI_ENABLE']
    root.find('RemoteApiPort').text = os.environ['REMOTEAPI_PORT']
    
    tree.write(file_path)

def update_sandbox(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    settings = root.find('Settings')
    if settings is not None:
        settings.find('GameMode').text = os.environ['SERVER_MODE']
        settings.find('MaxPlayers').text = os.environ['MAX_PLAYERS']
        settings.find('AutoSaveInMinutes').text = os.environ['SAVE_INTERVAL']
        settings.find('EnableSaving').text = os.environ['SAVE_ENABLED']
        settings.find('ExperimentalMode').text = os.environ['EXPERIMENTAL_ENABLED']
        settings.find('EnableIngameScripts').text = os.environ['INGAMESCRIPTS_ENABLED']
    
    tree.write(file_path)

config_file = "/home/container/config/SpaceEngineers-Dedicated.cfg"
update_xml(config_file)

world_path = f"/home/container/config/Saves/{os.environ['WORLD_NAME']}"
sandbox_files = [
    f"{world_path}/Sandbox.sbc",
    f"{world_path}/Sandbox_config.sbc"
]

for file in sandbox_files:
    if os.path.exists(file):
        update_sandbox(file)