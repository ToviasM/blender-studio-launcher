import addon_utils

original_path_func = addon_utils.paths


def register():
    def paths():
        addon_paths = original_path_func()
        import os 

        if "STUDIO_ADDON_PATH" in os.environ:
            envpaths = os.environ["STUDIO_ADDON_PATH"].split(os.pathsep)
            for p in envpaths:
                if os.path.isdir(p):
                    addon_paths.append(os.path.normpath(p))
        return addon_paths
    addon_utils.paths = paths

def unregister():
    addon_utils.paths = original_path_func