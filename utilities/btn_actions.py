from __future__ import annotations
import re

def run_create(shader_name: str, shader_type: str, assign: bool, textures: dict) -> str|None:
    from .mel_helper import selection_shapes_meshes
    from .sanity_checks import main_sanity_checks
    meshes_list = list()
    if assign:
        meshes_list = selection_shapes_meshes()
    sanity_errors = main_sanity_checks(shader_name, meshes_list)
    if sanity_errors:
        return sanity_errors
    material, sg = run_create_shader(shader_name, shader_type)
    if meshes_list:
        run_assign_shader(sg, meshes_list)
    if textures:
        run_connect_textures(material, textures, sg)
    return None

def run_assign_shader(sg: str, meshes_list: list[str]) -> None:
    from .mel_helper import assign_shader
    assign_shader(meshes_list, sg)

def run_create_shader(shader_name: str, shader_type: str) -> tuple:
    """
     Create a shader and return material and shaders. This is a wrapper around mel_helper.
     
     @param shader_name - Name of the shader to create.
     @param shader_type - Type of the shader.
     
     @return ( material sg ) where material is a : class : ` Material ` object and sg is a : class : ` ShaderGroup ` object
    """
    from .mel_helper import create_shader
    material, sg = create_shader(shader_name, shader_type)
    return material, sg

def run_connect_textures(shader: str, textures: dict, sg:str) -> None:
    """
     Connect textures to a subsurface.
     
     @param shader - name of the shader to connect to.
     @param textures - dictionary of attributes to be connected to the subsurface.
     @param sg - name of the subsurface to connect to. If None the shader is connected to the main

     @return None
    """
    from .mel_helper import (get_attributes_shaders, 
                             create_texture_file, 
                             connect_attributes, 
                             create_bump, 
                             create_displacement, 
                             create_color_correct, 
                             create_range)

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

    # Creates a texture file for each texture attribute.
    for attr, value in textures.items():
        attr_name = set(list_attr) & set(attr_dict.get(attr))
        # If attr_name is not set.
        if not attr_name:
            continue
        file_node = create_texture_file(shader, attr, value)
        # Create the bump and displacement attributes.
        if attr == 'bump':
            create_bump(shader, file_node, file_path = value, shader_attr=list(attr_name)[0])
            continue
        elif attr == 'displacement':
            displacement_node = create_displacement(shader, file_node)
            connect_attributes(displacement_node, 'displacement', sg, '{0}'.format(list(attr_name)[0]))
            continue
        # Connect to the shader and color attributes.
        if re.search('[Cc]olor', list(attr_name)[0]):
            color_correct_node = create_color_correct(shader, file_node, attr)
            connect_attributes(color_correct_node, 'outColor', shader, '{0}'.format(list(attr_name)[0]))
        else:
            range_node = create_range(shader, file_node, attr)
            connect_attributes(range_node, 'outColorR', shader, '{0}'.format(list(attr_name)[0]))