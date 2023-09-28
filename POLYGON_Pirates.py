import bpy
import os

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles\\Characters")
    fbxs = [f for f in os.listdir(folder) if f.endswith(".fbx") and f.startswith("Character_")]

    # Import them
    for fbx in fbxs:
        bpy.ops.import_scene.fbx(
            filepath=os.path.join(folder, fbx),
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=True,
            automatic_bone_orientation=True,
        )

    collection = bpy.data.collections["Characters"]

    # Loop through Characters
    first_armature = None
    for obj in collection.objects:
        # Save the first armature object
        if first_armature == None and obj.type == 'ARMATURE':
            first_armature = obj
            continue

        if first_armature != None and obj.type == 'MESH':
            if obj.modifiers and obj.modifiers[0].type == 'ARMATURE':
                # Set all mesh Armature modifiers to the first armature object
                obj.modifiers[0].object = first_armature
            # Make our first armature the object parent
            obj.parent = first_armature

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select unnecessary armatures
    first_armature = None
    for obj in collection.objects:
        if obj.type == 'ARMATURE':
            if first_armature == None:
                first_armature = obj
            else:
                obj.select_set(True)

    # Delete them
    bpy.ops.object.delete()

    # Apply location, rotation, scale to deltas
    for obj in collection.all_objects:
        obj.delta_location += obj.location
        obj.location = (0, 0, 0)
        obj.delta_rotation_euler.rotate(obj.rotation_euler)
        obj.rotation_euler = (0, 0, 0)
        obj.delta_scale = obj.scale
        obj.scale = (1, 1, 1)

    first_armature.name = "Characters"

    # Textures pointing to the wrong directory. Fix that
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        if image.source == "FILE":
            # Textures are pointing towards PolygonCity. Fix that
            filename = os.path.basename(image.filepath)

            if filename == "Texture_01.psd":
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\Texture_01_A.png"
                )
            else:
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\" + filename
                )

import_characters()