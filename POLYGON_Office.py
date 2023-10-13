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
        filepath=bpy.path.abspath("//SourceFiles/FBX/Character.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )

    collection = bpy.data.collections["Characters"]

    for obj in collection.objects:
        if obj.type == 'MESH':
            # All these characters share the same material
            obj.active_material = bpy.data.materials['lambert295']


def import_character_attachments():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Buildings' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Character_Attachments']

    # Find our FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX/")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") and f.startswith("SM_Chr_Attachment_")
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
            # All char attachments in this pack use a single texture and it's always
            # the base one.
            obj.active_material = bpy.data.materials['lambert295']


            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_buildings():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Buildings' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Buildings']

    # Find our FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX/")
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
            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

                for material_slot in obj.material_slots:
                    if material_slot.material.name.startswith("A_Glass") \
                        or material_slot.material.name.startswith("Glass"):
                        material_slot.material = bpy.data.materials["A_Glass"]
                    elif material_slot.material.name.startswith('lambert') \
                        or material_slot.material.name.startswith('OfficeSHD'):
                        material_slot.material = bpy.data.materials['lambert295']


            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_props():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Buildings' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Props']

    # Find our FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX/")
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
            # A couple of meshes have incorrect materials
            if obj.name in ['SM_Prop_Sculpture_02', 'SM_Prop_Sculpture_Base_01']:
                obj.active_material = bpy.data.materials['lambert295']
            # This one has a material named 'lambert12' and it's the only
            # one that needs to be set to Chrome so do that here to avoid
            # name clashes in other meshes.
            elif obj.name == 'SM_Prop_Sculpture_01':
                obj.active_material.name = 'POLYGONOffice_Chrome'

            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]

                if obj.name == 'SM_Prop_Clock_02' and material_slot.material.name == 'lambert2':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_Laptop_02' and material_slot.material.name == 'OfficeSHD18':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_Laptop_01' and material_slot.material.name == 'OfficeSHD16':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_GraphicsTablet_02' and material_slot.material.name == 'OfficeSHD1':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_GraphicsTablet_03' and material_slot.material.name == 'OfficeSHD1':
                    material_slot.material = bpy.data.materials["Screen3"]
                elif obj.name == 'SM_Prop_GraphicsTablet_04' and material_slot.material.name == 'OfficeSHD1':
                    material_slot.material = bpy.data.materials["Screen2"]
                elif obj.name == 'SM_Prop_TV_Wall_01' and material_slot.material.name == '_lambert2':
                    material_slot.material = bpy.data.materials["Screen2"]
                elif obj.name in ['SM_Prop_Photocopier_01', 'SM_Prop_Photocopier_02'] and material_slot.material.name == 'Screen':
                    material_slot.material = bpy.data.materials["Screen2"]
                elif obj.name == 'SM_Prop_Laptop_Folding_Screen_01' and material_slot.material.name == 'OfficeSHD16':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_Laptop_Folding_Screen_02' and material_slot.material.name == 'OfficeSHD16':
                    material_slot.material = bpy.data.materials["Screen2"]
                elif obj.name == 'SM_Prop_Monitor_Crt_01' and material_slot.material.name == 'OfficeSHD7':
                    material_slot.material = bpy.data.materials["Screen"]
                elif obj.name == 'SM_Prop_ArcadeMachine_01' and material_slot.material.name == 'OfficeSHD1':
                    material_slot.material = bpy.data.materials.new(name="POLYGONOffice_Arcade")
                elif obj.name == 'SM_Prop_Bottle_01' and material_slot.material.name == 'lambert8':
                    material_slot.material = bpy.data.materials["A_Glass"]
                elif material_slot.material.name == 'glassSHD':
                    material_slot.material = bpy.data.materials["A_Glass"]
                # Everything else goes to default mat
                elif material_slot.material.name.startswith("lambert") \
                    or material_slot.material.name.startswith("Office") \
                    or material_slot.material.name.startswith("gang"):
                    material_slot.material = bpy.data.materials["lambert295"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def import_weapons():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Buildings' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Weapons']

    # Find our FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//SourceFiles/FBX/")
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

                # All weapons in this pack use a single texture and it's always
                # the base one.
                obj.active_material = bpy.data.materials['lambert295']

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def fix_materials():
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            # Eye/Eyebrow pointing to wrong file in wrong directory. Fix that
            if filename == "PolygonOffice_Texture_01_A_New.psd":
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles/Textures/PolygonOffice_Texture_01_A.png"
                )
            else:
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//SourceFiles/Textures/" + filename
                )


    for material in bpy.data.materials:
        if material.name == 'lambert295':
            material.name = 'POLYGONOffice_Base'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.2
            bsdf.inputs["Roughness"].default_value = 0.8

            tex_emissive = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_emissive.image = bpy.data.images.load(bpy.path.abspath(
                "//SourceFiles/Textures/Emissive_01.png"
            ))
            tex_emissive_mp = material.node_tree.nodes.new('ShaderNodeMath')
            tex_emissive_mp.operation = 'MULTIPLY'
            tex_emissive_mp.inputs[1].default_value = 2
            material.node_tree.links.new(tex_emissive_mp.inputs[0], tex_emissive.outputs['Color'])
            material.node_tree.links.new(bsdf.inputs['Emission Strength'], tex_emissive_mp.outputs[0])
        elif material.name == 'A_Glass':
            material.name = 'POLYGONOffice_Glass'

            # https://blender.stackexchange.com/a/129014
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Alpha"].default_value = 0.5
        elif material.name == 'Net1':
            material.name = 'POLYGONOffice_Net'

            bsdf = material.node_tree.nodes["Principled BSDF"]
            tex_emissive = material.node_tree.nodes["Image Texture.001"]

            material.node_tree.links.new(bsdf.inputs['Alpha'], tex_emissive.outputs['Alpha'])
        elif material.name == 'POLYGONOffice_Arcade':
            material.use_nodes = True
            bsdf = material.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
            tex_albedo = material.node_tree.nodes.new('ShaderNodeTexImage')
            tex_albedo.image = bpy.data.images.load(bpy.path.abspath(
                "//SourceFiles/Textures/PolygonOffice_Texture_Sceen_Arcade_01.png"
            ))
            material.node_tree.links.new(bsdf.inputs['Base Color'], tex_albedo.outputs['Color'])
            material.node_tree.links.new(bsdf.inputs['Emission'], tex_albedo.outputs['Color'])

        # Set up the 5 Screen materials
        for i in range(1, 4):
            if material.name == 'Screen' + str(i).replace('1', ''):
                material.name = 'POLYGONOffice_Screen' + str(i)

                bsdf = material.node_tree.nodes["Principled BSDF"]
                tex_albedo = material.node_tree.nodes.new('ShaderNodeTexImage')
                tex_albedo.image = bpy.data.images.load(bpy.path.abspath(
                    "//SourceFiles/Textures/PolygonOffice_Texture_Sceen_0" + str(i) + ".png"
                ))
                material.node_tree.links.new(bsdf.inputs['Base Color'], tex_albedo.outputs['Color'])
                material.node_tree.links.new(bsdf.inputs['Emission'], tex_albedo.outputs['Color'])




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
import_character_attachments()
import_buildings()
import_props()
import_weapons()
fix_materials()
cleanup()