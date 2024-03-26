def run_assign_shader(shader_name: str, shader_type: str) -> None:
    from .mel_helper import create_shader, assign_shader, selection_shapes_meshes
    meshes_list = selection_shapes_meshes()
    material, sg = create_shader(shader_name, shader_type)
    assign_shader(meshes_list, sg)

def run_create_shader(shader_name: str, shader_type: str) -> None:
    from .mel_helper import create_shader
    material, sg = create_shader(shader_name, shader_type)