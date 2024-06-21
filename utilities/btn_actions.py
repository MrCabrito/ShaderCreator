def run_assign_shader(shader_name: str, shader_type: str) -> None:
    from .mel_helper import create_shader, assign_shader, selection_shapes_meshes
    meshes_list = selection_shapes_meshes()
    material, sg = create_shader(shader_name, shader_type)
    assign_shader(meshes_list, sg)
    return material, sg

def run_create_shader(shader_name: str, shader_type: str) -> None:
    from .mel_helper import create_shader
    material, sg = create_shader(shader_name, shader_type)
    return material, sg

def run_connect_textures(shader: str, textures: dict, sg:str):
    from .mel_helper import get_attributes_shaders, create_texture_file, connect_attributes, create_bump, create_displacement

    list_attr = get_attributes_shaders(shader, sg)
    
    attr_dict = {
        'diffuse': [
            'color', 
            'baseColor', 
            'diffuseColor'
                    ],
        'specular': [
            'specular', 
            'specularReflection', 
            'specularIntensity', 
            'specularColor', 
                     ],
        'roughness': [
            'roughness', 
            'specularRoughness'
            ],
        'transmission': [
            'transmission', 
            'transparent', 
            # 'transmissionColor',
            ],
        'sss': [
            'subsurface'
            ],
        'sssColor': [
            'subsurfaceColor'
            ],
        'bump': [
            'normalCamera'
            ],
        'displacement': [
            'displacementShader'
        ]
    }

    for attr, value in textures.items():
        attr_name = set(list_attr) & set(attr_dict.get(attr))
        if not attr_name:
            continue
        file_node = create_texture_file(shader, attr, value)
        if attr == 'bump':
            bump_node = create_bump(shader, file_node)
            connect_attributes(bump_node, 'outNormal', shader, '{0}'.format(list(attr_name)[0]))
            continue
        elif attr == 'displacement':
            displacement_node = create_displacement(shader, file_node)
            connect_attributes(displacement_node, 'displacement', sg, '{0}'.format(list(attr_name)[0]))
            continue
        matches = ['color','Color']
        if any(x in list(attr_name)[0] for x in matches):
            connect_attributes(file_node, 'outColor', shader, '{0}'.format(list(attr_name)[0]))
        else:
            connect_attributes(file_node, 'outColorR', shader, '{0}'.format(list(attr_name)[0]))