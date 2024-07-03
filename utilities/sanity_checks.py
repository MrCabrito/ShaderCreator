from __future__ import annotations
import re

def main_sanity_checks(name:str, objs_list: list[str]) -> str:
    from .mel_helper import surface_check
    error_message = ""
    surface_error = list()
    name_error = name_check(name)
    if objs_list:
        surface_error = surface_check(objs_list)

    if name_error:
        error_message = ''
        error_message = '<font color="red", size="25"><b>Name Error:</b></font><br />There are some special characters in the name:<br /><font color="red", size="4"><b>{}</b></font>, please remove them.<br />'.format(name)
    if surface_error:
        error_message = '{0}<font color="red", size="25"><b>Objects Selected Error:</b></font><br />There are some objects selected that can\'t be assign a shader, please select only MESHES or a NURB SURFACE.<br /><font color="red", size="4"><b>{1}</b></font>'.format(error_message,"<br />".join(surface_error))

    return error_message

def name_check(name:str) -> bool:
    special_char = re.compile('[@!#$%^&*()<>?/\|}{~:´]')
    if(special_char.search(name) == None and name.isascii() == True):
        return False
    return True

#color="red", 