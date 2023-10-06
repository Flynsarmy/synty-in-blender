import bpy
import os

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/Chr")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") \
        and f.startswith("SK_Chr_") \
        and not f.startswith("SK_Chr_Baby")
        # These ones have 's' versions whatever that means
        and f not in ["SK_Chr_Eyebrows_01.fbx", "SK_Chr_Eyes_Female_01.fbx", "SK_Chr_Eyes_Male_01.fbx"]
    ]

    # Import them
    for fbx in fbxs:
        bpy.ops.import_scene.fbx(
            filepath=os.path.join(folder, fbx),
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=True,
            automatic_bone_orientation=True,
        )

    # Loop through Characters
    first_armature = None
    collection = bpy.data.collections["Characters"]
    for obj in collection.objects:
        # Save the first armature object
        if first_armature == None and obj.type == 'ARMATURE':
            first_armature = obj
            continue

        if obj.type == 'MESH':
            # Always use non-duplicate version of material
            obj.active_material = bpy.data.materials[
                obj
                    .active_material.name
                    # SK_Chr_Kid_Schoolboy_01 has a broken 'lambert3' material. Set it to
                    # the same as all the others
                    .replace("lambert3", "lambert2")
                    # The eyes/eyebrows should also be on lambert2
                    .replace("KIds", "lambert2")
                    .split('.')[0]
            ]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


            if first_armature != None and obj.modifiers[0].type == 'ARMATURE':
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

    first_armature.name = "Armature"



def import_attachments():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Character_Attachments']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") \
        and (f.startswith("SM_Chr_Attach_") or f.startswith("SM_Chr_Hair"))
    ]

    collection = bpy.data.collections["Character_Attachments"]

    # Import them
    for fbx in fbxs:
        bpy.ops.import_scene.fbx(
            filepath=os.path.join(folder, fbx),
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=True,
            automatic_bone_orientation=True,
        )

    for obj in collection.objects:
        if obj.type == 'MESH':
            # Use the same material as the characters
            obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def import_weapons():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Weapons']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) if f.endswith(".fbx") and f.startswith("SK_Wep_")]

    collection = bpy.data.collections["Weapons"]

    # Import them
    for fbx in fbxs:
        bpy.ops.import_scene.fbx(
            filepath=os.path.join(folder, fbx),
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=True,
            automatic_bone_orientation=True,
        )

    for obj in collection.objects:
        # Rename any armatures to their first mesh object name
        # So they're not just 'Armature'.
        if obj.type == 'ARMATURE':
            for obj2 in collection.objects:
                if obj2.type == 'MESH' and obj2.parent == obj:
                    obj.name = obj2.name
                    break


        if obj.type == 'MESH':
            # Use the same material as the characters
            obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def fix_materials():
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            # Eye/Eyebrow pointing to wrong file in wrong directory. Fix that
            if filename == "Polygon_Kids_Texture_Facial_Expression_Frown_Freckles_01.png":
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\Faces_Human\\Normal\\Expression\\Polygon_Kids_Texture_Facial_Expression_Frown_01.png"
                )
            # Everything else goes to default texture
            else:
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\PolygonKids_Texture_01_A.png"
                )

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
import_attachments()
import_weapons()
fix_materials()
cleanup()