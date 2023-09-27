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
        filepath=bpy.path.abspath("//Source_Files\\FBX\\Character.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )

    # Textures pointing to the wrong directory. Fix that
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        if image.source == "FILE":
            # Make absolute
            image.filepath = bpy.path.abspath(
                "//Source_Files\\Textures\\" + os.path.basename(image.filepath)
            )

import_characters()