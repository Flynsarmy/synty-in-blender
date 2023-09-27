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
    fbxs = [f for f in os.listdir(folder) if f.endswith(".fbx") and f.startswith("SK_Chr_ZombieBoss_")]

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

        if first_armature != None and obj.type == 'MESH' and obj.modifiers[0].type == 'ARMATURE':
            # Set all mesh Armature modifiers to the first armature object
            obj.modifiers[0].object = first_armature
            # Make our first armature the object parent
            obj.parent = first_armature

            # Add missing texture node to the material
            texture_path = bpy.path.abspath("//SourceFiles\\Textures\\PolygonZombieBoss_Texture_01_A.png")
            for material_slot in obj.material_slots:
                material = material_slot.material

                # https://blender.stackexchange.com/a/129014
                bsdf = material.node_tree.nodes["Principled BSDF"]
                tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
                tex_image.image = bpy.data.images.load(texture_path)
                material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

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

    bpy.context.view_layer.objects.active = first_armature

    # Remove IK bones
    bpy.ops.object.mode_set(mode='EDIT')
    # Remove the IK bones
    for bone in first_armature.data.edit_bones:
        if bone.name.startswith("ik_"):
            first_armature.data.edit_bones.remove(bone)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Apply rotation, scale
    for obj in collection.objects:
        obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True, rotation=True)

    first_armature.name = "Characters"


import_characters()
