from __future__ import annotations
import maya.cmds as cmds

def get_all_shaders() -> list[str]:
    """
     Get all Shaders in the system. This is useful for debugging and to see if we can run a command that is in an environment that has a shader attached.
     
     
     @return A list of shader names that are in the system or None if there are no shaders in
    """
    return cmds.listNodeTypes('shader', ex = "volume")

def create_shader(name:str, node_type:str) -> tuple:
    """
     Create a shading node and set it as a surface shader. The node will be named _SG where name is the name of the shader and outColor is the color of the node.
     
     @param name - The name of the shader. If None a random name will be generated.
     @param node_type - The type of node to create.
     
     @return A tuple containing the created node and the created surface shader.
    """
    flags = {'asShader':True}
    # Set the name of the flag.
    if name:
        flags["name"] = name
    material = cmds.shadingNode(node_type, **flags)
    sg = cmds.sets(name="{}_SG".format(name), empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg

def assign_shader(obj_list: list[str], SG: str) -> None:
    """
     Assign a shaders to objects.
     
     @param obj_list - List of objects to assign the shaders to
     @param SG - Name of the shader to assign the objects to
     
     @return None
    """
    cmds.sets(obj_list, forceElement=SG)

def selection_shapes_meshes() -> list[str]:
    """
     List shapes in DAG with meshes.
     
     
     @return list of shapes in DAG with meshes
    """
    return cmds.ls(selection = True, dag=True, type="mesh", noIntermediate=True)

def get_attributes_shaders(shader: str, sg:str)-> list[str]:
    """
     Get attributes shaders. This is a helper function to get a list of shader attributes
     
     @param shader - name of the shader to search for
     @param sg - name of the shader group to search for
     
     @return list of shader attributes in the order they were found in the shaders.
    """
    shader_attr = cmds.listAttr(shader)
    shader_attr.extend(cmds.listAttr(sg))
    return shader_attr

def create_texture_file(shader_name:str, attr_type:str, file_path:str|None = None) -> str:
    """
     Create a file node that is used to place shaders.
     
     @param shader_name - Name of the shader to create
     @param attr_type - Type of attribute to use
     @param file_path - Path to file if None will use default
     
     @return The created node
    """
    file_node = cmds.shadingNode('file', name = '{0}_{1}'.format(shader_name, attr_type), asTexture=True)
    # Set the file texture name attribute to file_path
    if file_path:
        cmds.setAttr('{0}.fileTextureName'.format(file_node), file_path, type='string')
    create_2d_placement(file_node)
    return file_node

def create_2d_placement(texture_node:str) -> None:
    """
     Create a 2D placement node. This is used to place a texture in the scene.
     
     @param texture_node - The name of the node to place.
     
     @return The newly created node
    """
    placement_node = cmds.shadingNode("place2dTexture", asTexture=True, name='place2d_{0}'.format(texture_node))
    cmds.defaultNavigation(connectToExisting=True, source=placement_node, destination=texture_node)

def connect_attributes(out_obj:str, out_attr:str, in_obj:str, in_attr:str) -> None:
    """
     Connect attributes between two objects. This is a wrapper around cmds. connectAttr that uses { 0 }. { 1 } to connect the out_obj's attribute to the in_obj's attribute.
     
     @param out_obj - Name of the output object. It should be a string like'p1'or'p2 '.
     @param out_attr - Name of the attribute to connect the out_obj's attribute to.
     @param in_obj - Name of the input object. It should be a string like'p1'or'p2 '.
     @param in_attr - Name of the attribute to connect the in_obj's attribute to.
     
     @return None
    """
    cmds.connectAttr('{0}.{1}'.format(out_obj, out_attr), '{0}.{1}'.format(in_obj, in_attr))

def create_bump(shader_name:str, texture_node:str) -> str:
    """
     Create a bump shading node. This is used to bump an image to a different color. The shader must be created beforehand and it will be connected to the texture
     
     @param shader_name - name of the shader to use
     @param texture_node - name of the texture node to connect
     
     @return the created bump shading
    """
    bump_node = cmds.shadingNode('bump2d', name = '{0}_bump2d'.format(shader_name), asUtility=True)
    connect_attributes(texture_node, 'outColorR', bump_node, 'bumpValue')
    return bump_node

def create_displacement(shader_name:str, texture_node:str) -> str:
    """
     Create displacement Shader. This is used to render textures with different color in each direction.
     
     @param shader_name - Name of the shader to create.
     @param texture_node - Node to be connected to the shader.
     
     @return Reference to the created shader node.
    """
    displacement_node = cmds.shadingNode('displacementShader', name = '{0}_dispShd'.format(shader_name), asShader=True)
    connect_attributes(texture_node, 'outColorR', displacement_node, 'displacement')
    return displacement_node

def dialog_window() -> list:
    """
     Create and return a dialog window to select images. It is called by the command line and can be used to modify the list of images in the GUI.
     
     
     @return The list of images in the GUI or None
    """
    imageFilter = "Images Files (*.jpg *.jpeg *.tif *.png *.tga *.exr)"
    return cmds.fileDialog2(fileFilter=imageFilter, dialogStyle=2, okc='Ok', fm=1)