import re
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