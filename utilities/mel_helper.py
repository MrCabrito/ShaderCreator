import maya.cmds as cmds

def get_all_shaders() -> list[str]:
    return cmds.listNodeTypes('shader', ex = "volume")

def create_shader(name:str, node_type:str) -> tuple:
    flags = {'asShader':True}
    if name:
        flags["name"] = name
    material = cmds.shadingNode(node_type, **flags)
    sg = cmds.sets(name="{}_SG".format(name), empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg

def assign_shader(obj_list: list[str], SG: str) -> None:
    cmds.sets(obj_list, forceElement=SG)

def selection_shapes_meshes() -> list[str]:
    return cmds.ls(selection = True, dag=True, type="mesh", noIntermediate=True)

def get_attributes_shaders(shader: str, sg:str)-> list[str]:
    shader_attr = cmds.listAttr(shader)
    shader_attr.extend(cmds.listAttr(sg))
    return shader_attr

def create_texture_file(shader_name:str, attr_type:str, file_path:str|None = None) -> str:
    file_node = cmds.shadingNode('file', name = '{0}_{1}'.format(shader_name, attr_type), asTexture=True)
    if file_path:
        cmds.setAttr('{0}.fileTextureName'.format(file_node), file_path, type='string')
    create_2d_placement(file_node)
    return file_node

def create_2d_placement(texture_node:str) -> None:
    placement_node = cmds.shadingNode("place2dTexture", asTexture=True, name='place2d_{0}'.format(texture_node))
    cmds.defaultNavigation(connectToExisting=True, source=placement_node, destination=texture_node)

def connect_attributes(out_obj:str, out_attr:str, in_obj:str, in_attr:str) -> None:
    cmds.connectAttr('{0}.{1}'.format(out_obj, out_attr), '{0}.{1}'.format(in_obj, in_attr))

def create_bump(shader_name:str, texture_node:str) -> str:
    bump_node = cmds.shadingNode('bump2d', name = '{0}_bump2d'.format(shader_name), asUtility=True)
    connect_attributes(texture_node, 'outColorR', bump_node, 'bumpValue')
    return bump_node

def create_displacement(shader_name:str, texture_node:str) -> str:
    displacement_node = cmds.shadingNode('displacementShader', name = '{0}_dispShd'.format(shader_name), asShader=True)
    connect_attributes(texture_node, 'outColorR', displacement_node, 'displacement')
    return displacement_node

def dialog_window() -> list:
    imageFilter = "Images Files (*.jpg *.jpeg *.tif *.png *.tga *.exr)"
    return cmds.fileDialog2(fileFilter=imageFilter, dialogStyle=2, okc='Ok', fm=1)