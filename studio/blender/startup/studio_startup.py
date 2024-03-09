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