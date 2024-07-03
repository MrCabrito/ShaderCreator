from __future__ import annotations
import re

def main_sanity_checks(name:str, objs_list: list[str], textures: dict) -> str:
    from .mel_helper import surface_check
    error_message = ""
    surface_error = list()
    # Check if the name is valid
    name_error = name_check(name)
    # Check if the surface is valid.
    if objs_list:
        surface_error = surface_check(objs_list)
    if textures:
        empty_textures = path_is_empty_check(textures)
        path_not_found = path_exists_check(textures)

    # Add text if there is some errors found, depending where it didn't pass the sanity check.
    if name_error:
        error_message = '<font color="orange", size="25"><b>Name Warning:</b></font><br />There are some special characters in the name:<br /><font color="red", size="4"><b>{}</b></font>, remove them.<br />'.format(name)
    if surface_error:
        error_message = '{0}<br /><font color="orange", size="25"><b>Objects Selected Warning:</b></font><br />There are some objects selected that can\'t be assign a shader, select only MESHES or a NURB SURFACE.<br /><font color="red", size="4"><b>{1}</b></font><br />'.format(error_message,"<br />".join(surface_error))
    if empty_textures:
        error_message = '{0}<br /><font color="orange", size="25"><b>Empty Textures Warning:</b></font><br />There are some empty texture path, select a texture or uncheck them.<br /><font color="red", size="4"><b>{1}</b></font><br />'.format(error_message,"<br />".join(empty_textures))
    if path_not_found:
        error_message = '{0}<br /><font color="orange", size="25"><b>Path not Found Warning:</b></font><br />There are some files that doesn\'t exist in your computer, select an existing one.<br /><font color="red", size="4"><b>{1}</b></font><br />'.format(error_message,"<br />".join(path_not_found))

    return error_message

def name_check(name:str) -> bool:
    """
     Check if name is valid. This is a helper function for : func : ` get_name `.
     
     @param name - The name to check. It must not contain special characters and is not ascii.
     
     @return True if name is valid False otherwise.
    """
    special_char = re.compile('[@!#$%^&*()<>?/\|}{~:´]')
    # Return True if name is a special character.
    if(special_char.search(name) == None and name.isascii() == True):
        return False
    return True

def path_is_empty_check(textures: dict) -> list[str]:
    """
     Checks if the path is empty. This is to avoid having to do a path check in the textures.
     
     @param textures - A dictionary of texture names to paths.
     
     @return A list of texture names that are empty
    """
    empty_textures = [map_type for map_type,texture_path in textures.items() if not texture_path]
    return empty_textures

def path_exists_check(textures: dict) -> list[str]:
    """
     Checks if path exists in file system. This is to avoid problems with OpenGL's built - in texture loading
     
     @param textures - dictionary of map types and paths
     
     @return list of paths that don't exist in file
    """
    import os
    # path_not_found_dict = {map_type: texture_path for map_type,texture_path in textures.items() if texture_path and not os.path.isfile(texture_path)}
    path_not_found = ['{0}: {1}'.format(map_type, texture_path) for map_type,texture_path in textures.items() if texture_path and not os.path.isfile(texture_path)]
    return path_not_found