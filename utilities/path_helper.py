from __future__ import annotations
import re
import os

def path_udim(file_path: str) -> tuple:
    """
     Checks for UDIM format and modifies path if needed. This is a helper function for get_udim_file
     
     @param file_path - Path to file to check
     
     @return Tuple with path and udim or None if not found or invalid UDIM format
    """
    udim = None
    # Check for UDIM format
    if re.search('(\/.*?\.[\w:]+\.[\w:]+)', file_path):
        file_path, udim, extension = file_path.split('.')
        # Check for UDIM format Mari mode and modify path
        if re.search('(\d{4})', udim):
            file_path = '{0}.<UDIM>.{1}'.format(file_path, extension)
            udim = 3
        # Check for UDIM format Zbrush mode and modify path
        elif re.search('(u0\_v0)',udim):
            file_path = '{0}.u<u>_v<v>.{1}'.format(file_path, extension)
            udim = 1
        # Check for UDIM format Mudbox mode and modify path
        elif re.search('(u1\_v1)',udim):
            file_path = '{0}.u<U>_v<V>.{1}'.format(file_path, extension)
            udim = 2
    return file_path, udim

def path_look_relatives(file_path: str) -> dict:
    """
     Look for relatives in a path and return a dictionary. This is a helper function for path_look ()
     
     @param file_path - path to look for relatives
     
     @return dict with relative paths as keys and lists of file
    """
    # Split the path and file name of the given path
    path, file = file_path.rsplit("/", 1)
    # Look if the giving file has an specific map type
    map_type = re.search('([Dd]iffuse)|([Ss]pecular)|([Rr]oughness)|([Tt]ransmission)|([Ss]ssColor)|([Ss]ss)|([Bb]ump)|([Dd]isplacement)', file)
    if map_type:
        # Look for all the file in the same path of the file given
        files_found = [file_found for file_found in os.listdir(path) if os.path.isfile(os.path.join(path,file_found))]
        
        re_pattern = r'{}(([Dd]iffuse)|([Ss]pecular)|([Rr]oughness)|([Tt]ransmission)|([Ss]ssColor)|([Ss]ss)|([Bb]ump)|([Dd]isplacement))'.format(file.split(map_type.group())[0])
        re_compile = re.compile(re_pattern)
        files_relative = dict()

        # Loop through the files looking for a pattern similar of the given file
        for file_match in files_found:
            re_match = re.search(re_compile, file_match)
            if re_match:
                files_relative[(re_match.group().replace(file.split(map_type.group())[0], ''))]='{0}/{1}'.format(path,file_match)
        # Returns a dictionary of the map type and path founded
        return files_relative