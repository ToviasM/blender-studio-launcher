# Blender Studio Launcher

## Overview
The Blender Studio Launcher is designed to integrate Blender with our custom studio environment seamlessly. It ensures that Blender starts with specific arguments and an environment tailored to our studio's needs, with a focus on the addons and configurations that we've developed in-house.

## Features
- **Environment Variable Integration**: Set up to launch Blender with custom environment variables that direct our addons
- **Studio Addons Repository**: Blender's addon utility paths are updated to point to our repository's addon location, which contains our custom `bl_info` addons.
- **Addon Management**: Post-registration, a Python script executes to enable or disable addons within our environment, ensuring a tailored Blender experience.

## Getting Started
To get started with the Blender Studio Launcher, clone the repository. Then, execute the `main.py` to open a QT Window that enables us to launch Blender

## How it's done
To set up a cohesive environment we need to start by opening Blender through Python. This can be done through a subprocess

```subprocess.Popen(["users/programFiles/blender foundation/blender.exe"], env={"VARIABLE" : "VALUE"})```

###  Simple Setup
This subprocess takes a list of cmds, and an environment. Both are useful in launching and creating a Blender environment. For creating a simple environment, or running simple commands, you can run a Python script that runs when Blender is done registering classes

```subprocess.Popen(["users/programFiles/blender foundation/blender.exe", "-P", "user_setup_blender.py"], env={"VARIABLE" : "VALUE"})```

### BLENDER_USER_SCRIPTS
For our case we want to point Blender to our studio-specific path that contains our addons. This can be done by setting Blenders user script environment variable BLENDER_USER_SCRIPTS 

```subprocess.Popen(["users/programFiles/blender foundation/blender.exe", "-P", "user_setup_blender.py"], env={"BLENDER_USER_SCRIPTS" : "PATH"})```

### The Full Pipeline
This is great for a controlled environment, but if we set this path it removes all other user addons that are set in Blender. This is far from ideal, so we need to create our very own environment variable. This can be done by replacing the path function in blenders addon_utils.py script. This can be done directly, or in our case we create a new startup script that runs and replaces the function with the added environment variable

```
import addon_utils

STUDIO_VARIABLE = "STUDIO_ADDON_PATH"

original_path_func = addon_utils.paths

def register():
    "Overrides addon_utils path to include studio environment variable. Providing Blender with access to custom addon directories"

    def paths():
        addon_paths = original_path_func()
        import os 

        if STUDIO_VARIABLE in os.environ:
            envpaths = os.environ[STUDIO_VARIABLE].split(os.pathsep)
            for p in envpaths:
                if os.path.isdir(p):
                    addon_paths.append(os.path.normpath(p))
        return addon_paths
    addon_utils.paths = paths

def unregister():
    addon_utils.paths = original_path_func
```
