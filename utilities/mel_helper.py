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