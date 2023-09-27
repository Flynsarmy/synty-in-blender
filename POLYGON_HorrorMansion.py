import bpy
import os

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Import the characters
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//SourceFiles\\FBX\\Characters.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )

    collection = bpy.data.collections["Characters"]

    # Apply location, rotation, scale to deltas
    for obj in collection.all_objects:
        obj.delta_location += obj.location
        obj.location = (0, 0, 0)
        obj.delta_rotation_euler.rotate(obj.rotation_euler)
        obj.rotation_euler = (0, 0, 0)
        obj.delta_scale = obj.scale
        obj.scale = (1, 1, 1)

    # Textures pointing to the wrong directory. Fix that
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        # Textures are pointing towards PolygonCity. Fix that
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            if filename == "PolygonHorror_Texture_01.psd":
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\Alts\\PolygonHorror_Texture_01_A.png"
                )
            else:
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\Alts\\" + filename
                )

import_characters()