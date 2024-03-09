import subprocess
import os
import sys
import shutil
from pathlib import Path
from constants import STUDIO_PATH
import yaml

APP_CONFIG = "configs/apps.yml"
class_registry = {}

class App():
    def __init__(self, cmds, config, **kwargs):
        self._cmds = cmds
        self._config = config
        self._env = kwargs
        pass

    def get_environment(self):
        env = os.environ.copy()
        for key, value in self.env.items():
            env[key] = value
        return env
    
    @property
    def config(self):
        return self._config
    
    @property
    def cmds(self):
        return self._cmds
    
    @property
    def env(self):
        return self._env

    def _default_launch(self):
        self.prepare_launch()
        subprocess.Popen(self.cmds, env=self.get_environment())

    def prepare_launch(self):
        pass 

def register_class(key):
    def decorator(cls):
        class_registry[key] = cls
        return cls
    return decorator

@register_class("blender")
class BlenderLauncher(App):
    __name__ = "Blender Launcher"
    __category__ = "DCC"

    def __init__(self, cmds, config, **kwargs):
        super().__init__(cmds, config, **kwargs)
    
    def prepare_launch(self):
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
    def __init__(self) -> None:
        self.launchers = []
        self.load_config()

    def load_config(self):
        with open(STUDIO_PATH + "/" + APP_CONFIG, 'r') as file:
            config = yaml.safe_load(file)
        
        for app in config.get("apps"):
            launcher_class = class_registry.get(app)
            try:
                envs = config.get("apps").get(app).get("env")
                for env in envs.keys():
                    envs[env] = envs[env].format(STUDIO_REPO_PATH=STUDIO_PATH)
            except:
                pass
                
            cmds = config.get("apps").get(app).get("cmds")
            for index, cmd in enumerate(cmds):
                cmds[index] = cmd.format(PROGRAMFILES=os.environ.get('PROGRAMFILES'), version=config.get("apps").get(app).get("version"))


            launcher = launcher_class(cmds, config.get("apps").get(app), **envs)
            self.launchers.append(launcher)

    def get_launchers(self):
        return self.launchers

