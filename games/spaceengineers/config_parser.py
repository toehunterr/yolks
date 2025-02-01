#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

def update_element(element, key, value):
    if element is not None:
        if value:
            print(f"Updating key: {key} with value: {value}")
        else:
            print(f"Updating empty key: {key}")
        element.text = value

def update_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    session = root.find('SessionSettings')
    if session is not None:
        update_element(session.find('GameMode'), 'GameMode', os.environ['SERVER_MODE'])
        update_element(session.find('MaxPlayers'), 'MaxPlayers', os.environ['MAX_PLAYERS'])
        update_element(session.find('AutoSaveInMinutes'), 'AutoSaveInMinutes', os.environ['SAVE_INTERVAL'])
        update_element(session.find('EnableSaving'), 'EnableSaving', os.environ['SAVE_ENABLED'])
        update_element(session.find('ExperimentalMode'), 'ExperimentalMode', os.environ['EXPERIMENTAL_ENABLED'])
        update_element(session.find('EnableIngameScripts'), 'EnableIngameScripts', os.environ['INGAMESCRIPTS_ENABLED'])
    
    update_path = f"Z:/home/container/config/Saves/{os.environ['WORLD_NAME']}/Sandbox.sbc"
    update_element(root.find('LoadWorld'), 'LoadWorld', update_path)
    
    update_element(root.find('ServerPort'), 'ServerPort', os.environ['SERVER_PORT'])
    update_element(root.find('SteamPort'), 'SteamPort', os.environ['STEAM_PORT'])
    update_element(root.find('ServerName'), 'ServerName', os.environ['SERVER_NAME'])
    update_element(root.find('WorldName'), 'WorldName', os.environ['WORLD_NAME'])
    update_element(root.find('ServerDescription'), 'ServerDescription', os.environ['SERVER_DESC'])
    update_element(root.find('RemoteApiEnabled'), 'RemoteApiEnabled', os.environ['REMOTEAPI_ENABLE'])
    update_element(root.find('RemoteApiPort'), 'RemoteApiPort', os.environ['REMOTEAPI_PORT'])
    
    tree.write(file_path)

def update_sandbox(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    settings = root.find('Settings')
    if settings is not None:
        update_element(settings.find('GameMode'), 'GameMode', os.environ['SERVER_MODE'])
        update_element(settings.find('MaxPlayers'), 'MaxPlayers', os.environ['MAX_PLAYERS'])
        update_element(settings.find('AutoSaveInMinutes'), 'AutoSaveInMinutes', os.environ['SAVE_INTERVAL'])
        update_element(settings.find('EnableSaving'), 'EnableSaving', os.environ['SAVE_ENABLED'])
        update_element(settings.find('ExperimentalMode'), 'ExperimentalMode', os.environ['EXPERIMENTAL_ENABLED'])
        update_element(settings.find('EnableIngameScripts'), 'EnableIngameScripts', os.environ['INGAMESCRIPTS_ENABLED'])
    
    tree.write(file_path)

print("Starting configuration update...")
config_file = "/home/container/config/SpaceEngineers-Dedicated.cfg"
update_xml(config_file)

world_path = f"/home/container/config/Saves/{os.environ['WORLD_NAME']}"
sandbox_files = [
    f"{world_path}/Sandbox.sbc",
    f"{world_path}/Sandbox_config.sbc"
]

for file in sandbox_files:
    if os.path.exists(file):
        print(f"\nUpdating {file}")
        update_sandbox(file)