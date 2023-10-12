import bpy
import os

## IMPORTANT! Convert the SourceFiles/Characters/*.fbx from ASCII to FBX 2013.
## Put the converted files in a 'FBX 2013' subfolder like so:
## SourceFiles/Characters/FBX 2013/*.fbx
## Do the same for the following files in SourceFiles/FBX/ :
## - SM_Chr_Attach_ScarecrowHat_01.fbx
## - SM_Veh_Pickup_01.fbx


def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/Characters/FBX 2013")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") \
        and f.startswith("SK_Chr_")
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
        and f.startswith("SM_Chr_Attach_") \
        and f not in ["SM_Chr_Attach_ScarecrowHat_01.fbx"]
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
    # And the converted one
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//SourceFiles/FBX/FBX 2013/SM_Chr_Attach_ScarecrowHat_01.fbx"),
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
            # Use the same material as the characters
            obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def import_buildings():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Buildings']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
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
            # Use the same material as the characters
            obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def import_environments():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Environments']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and (f.startswith("SM_Env_") or f.startswith("SM_Generic_"))
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
            # Use the same material as the characters
            obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def import_props():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Props']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Prop_")
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
                # Use the same material as the characters
                if (material_slot.material.name in [
                        "Farm", "lambert1", "lambert23", "Vehicles", "Blade",
                        "lambert861"
                    ]) \
                    or material_slot.material.name.startswith("Farm"):
                    material_slot.material = bpy.data.materials["lambert2"]
                elif material_slot.material.name in ["Leaves"]:
                    material_slot.material = bpy.data.materials["lambert863"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name

def import_vehicles():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Vehicles']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") \
        and f.startswith("SM_Veh_") \
        and f not in ["SM_Veh_Pickup_01.fbx"]
    ]

    collection = bpy.data.collections["Vehicles"]

    # Import them
    for fbx in fbxs:
        bpy.ops.import_scene.fbx(
            filepath=os.path.join(folder, fbx),
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=True,
            automatic_bone_orientation=True,
        )
    # And the converted one
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//SourceFiles/FBX/FBX 2013/SM_Veh_Pickup_01.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )


    for obj in collection.objects:
        if obj.type == 'MESH':
            # Always use non-duplicate version of material
            obj.active_material = bpy.data.materials[
                obj
                    .active_material.name
                    .split('.')[0]
            ]
            # Use the same material as the characters
            if obj.active_material.name in ["lambert1", "lambert2"]:
                obj.active_material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def fix_materials():
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            if filename in ['Fence_Alpha.tga', 'PolygonFarm_Texture_01_A.png', 'PolygonFarm_Signs.png']:
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\" + filename
                )
            elif filename == 'leavessheet_cavity.png':
                image.filepath = bpy.path.abspath(
                    "//SourceFiles\\Textures\\Leaves_Diff.tga"
                )

    for material in bpy.data.materials:
        # Leaves material
        if material.name == 'lambert863':
            material.name = "POLYGONFarm_Leaves"

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]

            tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(bpy.path.abspath(
                "//SourceFiles\\Textures\\Leaves_Diff.tga"
            ))

            norm_image = material.node_tree.nodes.new('ShaderNodeTexImage')
            norm_image.image = bpy.data.images.load(bpy.path.abspath(
                "//SourceFiles\\Textures\\Leaves_Normals.png"
            ))

            normal_map = material.node_tree.nodes["Normal Map"]
            material.node_tree.links.new(bsdf.inputs['Alpha'], tex_image.outputs['Alpha'])
            material.node_tree.links.new(normal_map.inputs['Color'], norm_image.outputs['Color'])

            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.8

        # Glass material
        elif material.name == 'lambert3':
            material.name = "POLYGONFarm_Glass"

            bsdf = material.node_tree.nodes["Principled BSDF"]

            tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(bpy.path.abspath(
                "//SourceFiles\\Textures\\PolygonFarm_Texture_01_A.png"
            ))
            material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.8
            bsdf.inputs["Roughness"].default_value = 0.2
            bsdf.inputs["Alpha"].default_value = 0.5

        elif material.name == 'fence':
            material.name = "POLYGONFarm_Fence"
        elif material.name == 'lambert864':
            material.name = "POLYGONFarm_Signs"

            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.8
        elif material.name == 'lambert9':
            material.name = "POLYGONFarm_Wire"

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]

            alpha_tex = material.node_tree.nodes['Image Texture.001']
            material.node_tree.links.new(bsdf.inputs['Alpha'], alpha_tex.outputs['Alpha'])

            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.8
        elif material.name == 'lambert2':
            material.name = "POLYGONFarm_Base"

            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.8


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
import_buildings()
import_environments()
import_props()
import_vehicles()
fix_materials()
cleanup()