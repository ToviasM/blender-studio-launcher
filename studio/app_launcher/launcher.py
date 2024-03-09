import subprocess
import os
import sys
import shutil
from pathlib import Path
from constants import STUDIO_PATH
import yaml

APP_CONFIG = "configs/apps.yml"

class App():

    __logo__ = "default.png"
    __name__ = "Launcher"
    __category__ = ""
    __extensions__ = []

    def __init__(self, cmds, config, **kwargs):
        self.cmds = cmds
        self.config = config
        self.env = kwargs
        pass

    def _get_environment(self) -> dict:
        "Creates a suitable environment for launching applications. Using both the initial environment, as well as any additions"
        env = os.environ.copy()
        for key, value in self.env.items():
            env[key] = value
        return env

    def _get_commands(self, temp_cmds:list=None) -> list:
        "Returns a set of commands from the class commands and any temporary commands"
        cmds = self.cmds.copy()
        if temp_cmds:
            cmds.extend(temp_cmds)
        
        return cmds
    
    def _launch(self, temp_cmds:list=None):
        "Private function for launching applications through a subprocess"
    
        self.prepare_launch()
        subprocess.Popen(self._get_commands(), env=self._get_environment())
    
    def asset_launch(self, asset_path):
        "Overridable function that launches the application with a targeted asset path"
        
        if os.path.splitext(asset_path)[1] in self.__extensions__:
            self._launch(temp_cmds=[asset_path])

    def prepare_launch(self):
        "Prepares the application with any required setup"
        pass 

class_registry = {"default" : App}

def register_class(key):
    "Decorator for registering app classes by name, allowing for new apps to be linked easily with the app config"
    def decorator(cls):
        class_registry[key] = cls
        return cls
    return decorator

@register_class("blender")
class BlenderLauncher(App):
    __logo__ = "blender.png"
    __name__ = "Blender Launcher"
    __category__ = "DCC"
    __extensions__ = [".blend"]

    def __init__(self, cmds, config, **kwargs):
        super().__init__(cmds, config, **kwargs)
    
    def prepare_launch(self):
        "Copies studio startup folder to Blenders startup directory"

        startup_src = Path(self.env.get("STUDIO_STARTUP_PATH"))
        startup_destination = Path(os.path.dirname(self.cmds[0]) + "/{version}".format(version=self.config.get("version")) + "/scripts/startup")

        def copy_directory_contents(src, destination):

            for item in src.iterdir():
                source_item = src / item
                destination_item = destination / os.path.basename(item)

                if source_item.is_dir():
                    source_item.mkdir(exist_ok=True)
                    copy_directory_contents(source_item, destination_item)
                else:
                    print(source_item)
                    print(destination_item)
                    shutil.copy2(source_item, destination_item)

        copy_directory_contents(startup_src, startup_destination)



class ConfigReader():
    def __init__(self):
        self.launchers = []
        self.load_config()

    def load_config(self):
        "Loads the app config and creates launchers"

        with open(STUDIO_PATH + "/" + APP_CONFIG, 'r') as file:
            config = yaml.safe_load(file)
        
        for app in config.get("apps"):

            variables = {
                'STUDIO_REPO_PATH': STUDIO_PATH,
                'PROGRAMFILES': os.environ.get('PROGRAMFILES'),
                'version': config.get("apps").get(app).get("version")
            }

            launcher_class = class_registry.get(app)
            if launcher_class is None:
                launcher_class = class_registry.get("default")

            envs = config.get("apps").get(app).get("env")
            for env in envs.keys():
                envs[env] = envs[env].format_map(variables)

            cmds = config.get("apps").get(app).get("cmds")
            for index, cmd in enumerate(cmds):
                cmds[index] = cmd.format_map(variables)


            launcher = launcher_class(cmds, config.get("apps").get(app), **envs)
            self.launchers.append(launcher)

    def get_launchers(self) -> list:
        return self.launchers

