from __future__ import annotations
import re
import os

def path_udim(file_path: str) -> tuple:
    """
     Checks for UDIM format and modifies path if needed. This is a helper function for get_udim_file
     
     @param file_path - Path to file to check
     
     @return Tuple with path and udim or None if not found or invalid UDIM format
    """
    udim_attr = None
    # Check for UDIM format
    udim_match = re.search('(\.\d{4}\.)|(\.u0\_v0\.)|(\.u1\_v1\.)', file_path)
    if udim_match:
        file_path, end_file = file_path.split(udim_match.group())
        # Check for UDIM format Mari mode and modify path
        if re.search('(\.\d{4}\.)', udim_match.group()):
            file_path = '{0}.<UDIM>.{1}'.format(file_path, end_file)
            udim_attr = 3
        # Check for UDIM format Zbrush mode and modify path
        elif re.search('(\.u0\_v0\.)',udim_match.group()):
            file_path = '{0}.u<u>_v<v>.{1}'.format(file_path, end_file)
            udim_attr = 1
        # Check for UDIM format Mudbox mode and modify path
        elif re.search('(\.u1\_v1\.)',udim_match.group()):
            file_path = '{0}.u<U>_v<V>.{1}'.format(file_path, end_file)
            udim_attr = 2
    return file_path, udim_attr

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
        file_name, file_extension = file.rsplit('.', 1)
        file_version = re.search('([Vv]\d{2})', file_name)
        file_name = file_name.replace(file_version.group(), '([Vv]\d{2})')
        file_root, file_end = file_name.split(map_type.group())
        re_pattern = r'{0}(([Dd]iffuse)|([Ss]pecular)|([Rr]oughness)|([Tt]ransmission)|([Ss]ssColor)|([Ss]ss)|([Bb]ump)|([Dd]isplacement)){1}.{2}'.format(file_root, file_end, file_extension)
        re_compile = re.compile(re_pattern)
        files_relative = dict()
        
        # Loop through the files looking for a pattern similar of the given file
        for file in files_found:
            re_match = re.search(re_compile, file)
            if re_match:
                map_type = (re.search('([Dd]iffuse)|([Ss]pecular)|([Rr]oughness)|([Tt]ransmission)|([Ss]ssColor)|([Ss]ss)|([Bb]ump)|([Dd]isplacement)', file)).group()
                if not files_relative.get(map_type):
                    files_relative[map_type] = list()
                files_relative[map_type].append('{0}/{1}'.format(path,file))
        # Returns a dictionary of the map type and path founded
        files_latest_version = file_latest_version(files_relative)
        return files_latest_version
    
def file_latest_version(files_dict: dict) -> dict:
    """
     Given a dictionary of map types and a list of files find the latest version
     
     @param files_dict - Dictionary of map types and lists of files
     
     @return Dictionary of map types and latest version of each file
    """
    files_latest_version = dict()
    # This function will find the latest version of the files in the files_dict and update the files_latest_version map_type.
    for map_type, files in files_dict.items():
        current_version = int()
        latest_version = str()
        # Find the latest version of the given files.
        for file in files:
            re_match = re.search('([Vv]\d{2})', file)
            match_version = int(re_match.group()[1:])
            # Set current_version to the latest version
            if match_version > current_version:
                current_version = match_version
                latest_version = file
        files_latest_version[map_type] = latest_version
    return files_latest_version