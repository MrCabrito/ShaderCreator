from __future__ import annotations
import maya.cmds as cmds
import re

def get_all_shaders() -> list[str]:
    """
     Get all shaders that maya knows about. This is used to determine which shaders should be used for the scene
     
     
     @return A list of shader
    """
    shader_maya = cmds.listNodeTypes('shader', ex = "volume")
    default_shaders = [
        'aiAmbientOcclusion',
        'aiAtmosphereVolume',
        'aiCarPaint',
        'aiLambert',
        'aiLayeredTexture',
        'aiMatte',
        'aiMixShader',
        'aiShadowMatte',
        'aiStandardHair',
        'aiStandardSurface',
        'aiToon',
        'aiTwoSided',
        'blinn',
        'lambert',
        'layeredShader',
        'phong',
        'rampShader',
        'surfaceShader',
        'RedshiftStandardMaterial',
        'RedshiftCarPaint',
    ]
    shaders_found = list(set(default_shaders) & set(shader_maya))
    return shaders_found

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
     List shapes in DAG with meshes and nurbsSurfaces.
     
     
     @return list of shapes in DAG with meshes and nurbsSurfaces.
    """
    return cmds.ls(selection = True, dag=True, type=["mesh", "nurbsSurface"], noIntermediate=True)

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

def create_texture_file(shader_name:str, attr_type:str, file_path:str) -> str:
    """
     Create a file node that is used to place shaders.
     
     @param shader_name - Name of the shader to create
     @param attr_type - Type of attribute to use
     @param file_path - Path to file
     
     @return The created node
    """
    from .path_helper import path_udim
    file_node = cmds.shadingNode('file', name = '{0}_{1}'.format(shader_name, attr_type), asTexture=True)
    # Set the file texture name attribute to file_path
    if file_path:
        # Check path before adding to the node for UDIM format
        file_path, udim_format = path_udim(file_path)
        cmds.setAttr('{0}.fileTextureName'.format(file_node), file_path, type='string')
        # Check if using UDIM format mode to set the attribute to the corresponding format
        if udim_format:
            cmds.setAttr('{0}.uvTilingMode'.format(file_node), udim_format)
    # Adds the 2d placement for the file node
    create_2d_placement(file_node)
    return file_node

def create_2d_placement(texture_node:str) -> None:
    """
     Create a 2D placement node. This is used to place a texture in the scene.
     
     @param texture_node - The name of the node to place.
     
     @return None
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

def create_bump(shader_name:str, texture_node:str, file_path:str, shader_attr:str) -> None:
    """
     Create a bump shading node. If shader_name is AI or Bb it will be used as a shader.
     
     @param shader_name - name of the shader to create
     @param texture_node - name of the texture node to connect the shader to
     @param file_path - path to the shader file that will be used
     @param shader_attr - attributes to set on the shader node
     
     @return None
    """
    shader_type = cmds.nodeType(shader_name)
    # If the shader type is arnold
    if shader_type.startswith('ai'):
        # If the file is a bump file or a normal map it will use different type of node.
        if re.search('[Bb]ump', file_path):
            bump_node = cmds.shadingNode('aiBump2d', name = '{0}_bump2d'.format(shader_name), asUtility=True)
            connect_attributes(texture_node, 'outColorR', bump_node, 'bumpMap')
        else:
            bump_node = cmds.shadingNode('aiNormalMap', name = '{0}_normal'.format(shader_name), asUtility=True)
            connect_attributes(texture_node, 'outColor', bump_node, 'input')
        connect_attributes(bump_node, 'outValue', shader_name, shader_attr)
        return bump_node
    bump_node = cmds.shadingNode('bump2d', name = '{0}_bump2d'.format(shader_name), asUtility=True)
    connect_attributes(texture_node, 'outColorR', bump_node, 'bumpValue')
    connect_attributes(bump_node, 'outNormal', shader_name, shader_attr)

def create_displacement(shader_name:str, texture_node:str) -> str:
    """
     Create displacement Shader. This is used to render textures with different color in each direction.
     
     @param shader_name - Name of the shader to create.
     @param texture_node - Node to be connected to the shader.
     
     @return The created node.
    """
    displacement_node = cmds.shadingNode('displacementShader', name = '{0}_dispShd'.format(shader_name), asShader=True)
    setRange_node = cmds.shadingNode('setRange', name = '{0}_displacement_setRange'.format(shader_name), asUtility=True)
    connect_attributes(texture_node, 'outColor', setRange_node, 'value')
    connect_attributes(setRange_node, 'outValueX', displacement_node, 'displacement')
    return displacement_node

def create_color_correct(shader_name:str, texture_node:str, attr_type:str) -> str:
    """
     Create colorCorrect node for shader. This is used to correct color of texture
     
     @param shader_name - name of shader to create node for
     @param texture_node - name of texture node to create node for
     @param attr_type - attribute type of node to create

     @return The created node.
    """
    shader_type = cmds.nodeType(shader_name)
    node_name = '{0}_{1}'.format(shader_name, attr_type)
    # Creates a color correct node for the shader type.
    if shader_type.startswith('ai'):
        color_correct_node = create_nodes('aiColorCorrect', node_name)
        connect_attributes(texture_node, 'outColor', color_correct_node, 'input')
    else:
        color_correct_node = create_nodes('colorCorrect', node_name)
        connect_attributes(texture_node, 'outColor', color_correct_node, 'inColor')
    return color_correct_node

def create_range(shader_name:str, texture_node:str, attr_type:str) -> str:
    """
     Create a range node to be used.
     
     @param shader_name - name of the shader to be used
     @param texture_node - name of the texture node to be used
     @param attr_type - type of attribute to be used
     
     @return name of the created node or the shader name
    """
    shader_type = cmds.nodeType(shader_name)
    node_name = '{0}_{1}'.format(shader_name, attr_type)
    # If shader_type starts with ai return shader_name
    if shader_type.startswith('ai'):
        color_correct_node = create_nodes('aiRange', node_name)
        connect_attributes(texture_node, 'outColor', color_correct_node, 'input')
    else:
        return shader_name
    return color_correct_node

def create_nodes(node_type:str, name:str) -> str:
    """
     Create shading nodes of type node_type.
     
     @param node_type - Type of node to create. Can be one of the following :'colorCorrect', 'setRange''
     @param name - Name to give the node. It is used as a prefix to the node name.
     
     @return The name of the created node or None if there was an error
    """
    return cmds.shadingNode(node_type, name = '{0}_{1}'.format(name, node_type), asUtility=True)

def dialog_window() -> list:
    """
     Create and return a dialog window to select images. It is called by the command line and can be used to modify the list of images in the GUI.
     
     
     @return The list of images in the GUI or None
    """
    imageFilter = "Images Files (*.jpg *.jpeg *.tif *.png *.tga *.exr)"
    return cmds.fileDialog2(fileFilter=imageFilter, dialogStyle=2, okc='Ok', fm=1)

def surface_check(objs_list:list[str]) -> list[str]|None:
    """
     Checks if nodes are surfaces or nurbsSurface. This is to avoid problems with node types that don't have mesh or nurbsSurface in them.
     
     @param objs_list - list of nodes to check
     
     @return list of nodes that do not have mesh or nurbs
    """
    wrong_objs = list()
    # Add any objects that are not mesh nurbsSurface objects
    for obj in objs_list:
        # Add obj to wrong_objs list if not mesh nurbsSurface
        if not re.findall('mesh|nurbsSurface', cmds.nodeType(obj)):
            wrong_objs.append(obj)
    return wrong_objs if wrong_objs else None