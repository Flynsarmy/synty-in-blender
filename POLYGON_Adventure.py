import bpy
import os
from mathutils import Matrix

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Character_Files/Unity_Version_Mechanim")
    fbxs = [f for f in os.listdir(folder) if f.endswith(".fbx")]

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

        if obj.type == 'MESH':
            # Always use non-duplicate version of material
            obj.active_material = bpy.data.materials[
                obj.active_material.name.split('.')[0]
            ]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

            if first_armature != None and obj.modifiers and obj.modifiers[0].type == 'ARMATURE':
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

    # Apply location, rotation, scale to deltas
    for obj in collection.all_objects:
        if obj.name != 'Armature':
            mat = obj.matrix_local
            obj.data.transform(mat)
            obj.matrix_local = Matrix()
        else:
            obj.delta_rotation_euler.rotate(obj.rotation_euler)
            obj.rotation_euler = (0, 0, 0)
            obj.delta_scale = obj.scale
            obj.scale = (1, 1, 1)


def import_buildings():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Buildings']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//FBX/")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Bld_")
    ]

    collection = bpy.data.collections["Buildings"]

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
            # Always use non-duplicate version of material
            obj.active_material = bpy.data.materials[
                obj.active_material.name.split('.')[0]
            ]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_environments():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Environments']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Env_")
    ]

    collection = bpy.data.collections["Environments"]

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
            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

#                if material_slot.material.name in ['blinn283', 'blinn284', 'blinn285', 'lambert2']:
#                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_props():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Props']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and (f.startswith("SM_Prop_") or f.startswith('SM_Item_'))
    ]

    collection = bpy.data.collections["Props"]

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
            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

#                if material_slot.material.name in ['blinn283', 'lambert2']:
#                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_weapons():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Weapons']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Wep_")
    ]

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
        if obj.type == 'MESH':
            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

#                if material_slot.material.name in ['blinn283', 'lambert2']:
#                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def fix_materials():
    # Textures pointing to the wrong directory. Fix that
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            if filename in ["Characters_White.png", "Characters_Black.png"]:
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//Textures/" + filename
                )
            elif filename in ["Texture_01.psd"]:
                image.filepath = bpy.path.abspath(
                    "//Textures/PolyAdventureTexture_01.png"
                )

    for material in bpy.data.materials:
        if material.name in ['Black', 'White']:
            material.name = 'POLYGONAdventure_' + material.name

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.5
            bsdf.inputs["Roughness"].default_value = 0.5
        elif material.name in ['blinn265']:
            material.name = 'POLYGONAdventure_Base'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.5
            bsdf.inputs["Roughness"].default_value = 0.5



def cleanup():
    bpy.ops.object.select_all(action='DESELECT')

    # Apply rotation, scale
    for obj in bpy.data.objects:
        # Skip the 'Characters' collection. Things mess up if we apply those.
        if obj.name != 'Armature' or (obj.parent and obj.parent.name != 'Armature'):
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
import_buildings()
import_environments()
import_props()
import_weapons()
fix_materials()
cleanup()