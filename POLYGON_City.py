## IMPORTANT! Some files in Polygon_City_SourceFiles/SourceFiles/FBX/*.fbx are in ASCII
## format and need conversion. Use Autodesk FBX Converter 2013 to convert them.
## Put the converted files in a 'FBX 2013' subfolder like so:
## Polygon_City_SourceFiles/SourceFiles/FBX/FBX 2013/*.fbx
## Here are the files that need conversion:
## - SM_Bld_Station_01.fbx
## - SM_Env_Flower_01.fbx

import bpy
import os
import mathutils

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/Characters")
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
                obj
                    .active_material.name
                    .split('.')[0]
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


def import_buildings():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Buildings']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX/")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Bld_") and f not in ["SM_Bld_Station_01.fbx"]
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
    # Import the converted file
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX/FBX 2013/SM_Bld_Station_01.fbx"),
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

            # Fix scaling
            if obj.scale.x < 1.0:
                obj.scale *= 100

            # Use the same material as the characters
            for material_slot in obj.material_slots:
                if material_slot.material.name in ['blinn283', 'blinn284', 'blinn285']:
                    material_slot.material = bpy.data.materials["lambert14"]


            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_environments():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Environments']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Env_") and f not in ["SM_Env_Flower_01.fbx"]
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
    # Import the converted file
    bpy.ops.import_scene.fbx(
        filepath=bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX/FBX 2013/SM_Env_Flower_01.fbx"),
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

                if material_slot.material.name in ['blinn283', 'blinn284', 'blinn285', 'lambert2']:
                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_props():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Props']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX")
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

                if material_slot.material.name in ['blinn283', 'lambert2']:
                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_vehicles():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Vehicles']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Polygon_City_SourceFiles/SourceFiles/FBX//Veh")
    fbxs = [f for f in os.listdir(folder) if f.endswith(".fbx") and f.startswith("SM_Veh_")]

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

    for obj in collection.objects:
        if obj.type == 'MESH':
            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

                if material_slot.material.name in ['Body']:
                    material_slot.material = bpy.data.materials["lambert14"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def fix_materials():
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            if filename in ["PolygonCity_Texture_01_C.png"]:
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//Polygon_City_SourceFiles\\SourceFiles\\Textures\\" + filename
                )
#            elif filename in ["PolygonCity_Texture_Normal.png", "PolygonCity_Texture_Metallic.tga"]:
#                image.colorspace_settings.name = 'Non-Color'

    for material in bpy.data.materials:
        if material.name == 'lambert14':
            material.name = 'POLYGONCity_Base'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Specular"].default_value = 0.5

            # Set up metallic map
            uv_map = material.node_tree.nodes.new('ShaderNodeUVMap')
            mapping = material.node_tree.nodes.new('ShaderNodeMapping')
            tex_metallic = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_metallic.image = bpy.data.images.load(bpy.path.abspath(
                "//Polygon_City_SourceFiles/SourceFiles/Textures/PolygonCity_Texture_Metallic.tga"
            ))
            tex_metallic.image.colorspace_settings.name = 'Non-Color'
            tex_metallic_mp = material.node_tree.nodes.new('ShaderNodeMath')
            tex_metallic_mp.operation = 'MULTIPLY'
            tex_metallic_mp.inputs[1].default_value = 1.5
            material.node_tree.links.new(mapping.inputs['Vector'], uv_map.outputs['UV'])
            material.node_tree.links.new(tex_metallic.inputs['Vector'], mapping.outputs['Vector'])
            material.node_tree.links.new(tex_metallic_mp.inputs[0], tex_metallic.outputs['Color'])
            material.node_tree.links.new(bsdf.inputs['Metallic'], tex_metallic_mp.outputs[0])

            # Set up normal map
            uv_map = material.node_tree.nodes.new('ShaderNodeUVMap')
            mapping = material.node_tree.nodes.new('ShaderNodeMapping')
            tex_normal = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_normal.image = bpy.data.images.load(bpy.path.abspath(
                "//Polygon_City_SourceFiles/SourceFiles/Textures/PolygonCity_Texture_Normal.png"
            ))
            tex_normal.image.colorspace_settings.name = 'Non-Color'
            normal = material.node_tree.nodes["Normal Map"]
            material.node_tree.links.new(mapping.inputs['Vector'], uv_map.outputs['UV'])
            material.node_tree.links.new(tex_normal.inputs['Vector'], mapping.outputs['Vector'])
            material.node_tree.links.new(normal.inputs['Color'], tex_normal.outputs['Color'])
            material.node_tree.links.new(bsdf.inputs['Normal'], normal.outputs['Normal'])

        elif material.name == 'Glass':
            material.name = 'POLYGONCity_Glass'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]

            bsdf.inputs["Base Color"].default_value = (0.054, 0.8, 0.627, 0)
            bsdf.inputs["Metallic"].default_value = 0.5
            bsdf.inputs["Specular"].default_value = 0.9
            bsdf.inputs["Roughness"].default_value = 0.2
            bsdf.inputs["Alpha"].default_value = 0.5


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
import_buildings()
import_environments()
import_props()
import_vehicles()
fix_materials()
cleanup()