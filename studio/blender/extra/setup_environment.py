import atexit
import json
import os 

import bpy

script_path = os.path.abspath(__file__)
folder_name =os.path.dirname(script_path)
config_path = os.path.join(folder_name, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

def setup_addons(config, key, status):
    addons = config[key]
    for addon in addons:
        if status is True:
            bpy.ops.preferences.addon_enable(module=addon)
        else:
            bpy.ops.preferences.addon_disable(module=addon)

setup_addons(config, "enabled_addons", True)
setup_addons(config, "disabled_addons", False)