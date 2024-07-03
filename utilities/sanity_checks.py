from __future__ import annotations
import re

def main_sanity_checks(name:str, objs_list: list[str]) -> str:
    """
     Check for sanity of Shader Creator Tool. This is a helper function to make sure that the user has entered all necessary information before running.
     
     @param name - The name of the shader
     @param objs_list - The list of objects to check for
     
     @return A string with error messages or empty string if everything is good
    """
    from .mel_helper import surface_check
    error_message = ""
    surface_error = list()
    # Check if the name is valid
    name_error = name_check(name)
    # Check if the surface is valid.
    if objs_list:
        surface_error = surface_check(objs_list)

    # Add text if there is some errors found, depending where it didn't pass the sanity check.
    if name_error:
        error_message = '<font color="red", size="25"><b>Name Error:</b></font><br />There are some special characters in the name:<br /><font color="red", size="4"><b>{}</b></font>, please remove them.<br />'.format(name)
    if surface_error:
        error_message = '{0}<font color="red", size="25"><b>Objects Selected Error:</b></font><br />There are some objects selected that can\'t be assign a shader, please select only MESHES or a NURB SURFACE.<br /><font color="red", size="4"><b>{1}</b></font>'.format(error_message,"<br />".join(surface_error))

    return error_message

def name_check(name:str) -> bool:
    """
     Check if name is valid. This is a helper function for : func : ` get_name `.
     
     @param name - The name to check. It must not contain special characters and is not ascii.
     
     @return True if name is valid False otherwise. >>> name_check ('John Smith') True >>> name_check ('John Smith
    """
    special_char = re.compile('[@!#$%^&*()<>?/\|}{~:´]')
    # Return True if name is a special character.
    if(special_char.search(name) == None and name.isascii() == True):
        return False
    return True