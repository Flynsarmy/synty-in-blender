import bpy
import os

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Import characters
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//Source_Files/FBX/Character.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )

def fix_materials():
    # Textures pointing to the wrong directory. Fix that
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        if image.source == "FILE":
            # Make absolute
            image.filepath = bpy.path.abspath(
                "//Source_Files/Textures/" + os.path.basename(image.filepath)
            )

    for material in bpy.data.materials:
        if material.name == 'lambert2':
            material.name = 'POLYGONCityCharacters_Base'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]

            bsdf.inputs["Specular"].default_value = 0.5
            bsdf.inputs["Roughness"].default_value = 0.6


def cleanup():
    # Apply rotation, scale
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True, rotation=True)

    # Removed orphaned data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


import_characters()
fix_materials()
cleanup()