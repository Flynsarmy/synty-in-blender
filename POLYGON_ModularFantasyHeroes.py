import bpy
import os

# https://blender.stackexchange.com/a/272730
def delete_hierarchy(parent_obj_name):
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects[parent_obj_name]
    obj.animation_data_clear()
    names = set()
    # Go over all the objects in the hierarchy like @zeffi suggested:
    def get_child_names(obj):
        for child in obj.children:
            names.add(child.name)
            if child.children:
                get_child_names(child)

    get_child_names(obj)
    names.add(parent_obj_name)
    objects = bpy.data.objects

    # Remove the animation from the all the child objects
    if names:
        for child_name in names:
            bpy.data.objects[child_name].animation_data_clear()
            objects[child_name].select_set(state=True)
            bpy.data.objects.remove(objects[child_name])

def import_characters():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Characters']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Source_Files/FBX")

    # Import them
    bpy.ops.import_scene.fbx(
        filepath=os.path.join(folder, "ModularCharactersFixedScale.fbx"),
        use_anim=False,
        ignore_leaf_bones=True,
        force_connect_children=True,
        automatic_bone_orientation=True,
    )

    collection = bpy.data.collections["Characters"]

    # https://discord.com/channels/502587764299006004/1103191808667824129
    # LegLeft_Male_* and LegRight_Male_* are reversed. It's a known issue
    # that won't get fixed so let's fix them here.
    for obj in collection.objects:
        if obj.type == 'MESH':
            if obj.name.startswith('Chr_LegLeft_Male_'):
                obj.name = 'Fixed' + obj.name.replace('LegLeft', 'LegRight')
            elif obj.name.startswith('Chr_LegRight_Male_'):
                obj.name = 'Fixed' + obj.name.replace('LegRight', 'LegLeft')

    # Now go through and remove the 'Fixed' prefixes we added above
    for obj in collection.objects:
        if obj.type == 'MESH':
            if obj.name.startswith('Fixed'):
                obj.name = obj.name[5:]

    # Rename Meshes to be the same as their parent MeshObjects
    for obj in collection.objects:
        if obj.type == 'MESH':
            obj.data.name = obj.name[4:]

    # Delete unneeded nodes
    delete_hierarchy('Modular_Characters')




def import_weapons():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Highlight the 'Characters' collection - https://blender.stackexchange.com/a/248563
    bpy.context.view_layer.active_layer_collection = \
        bpy.context.view_layer.layer_collection.children['Weapons']

    # Find our character FBX's - https://blender.stackexchange.com/a/253543
    folder = bpy.path.abspath("//Source_Files/FBX/Weapons")
    fbxs = [f for f in os.listdir(folder) \
        if f.endswith(".fbx") \
        and (f.startswith("SK_Wep_") or f.startswith("SM_Wep_"))
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
            # The static mesh assets are sitting inside EMPTYs. Pull them out.
            if obj.parent and obj.parent.type == 'EMPTY':
                obj.parent = None

            for material_slot in obj.material_slots:
                # Always use non-duplicate version of material
                material_slot.material = bpy.data.materials[
                    material_slot.material.name.split('.')[0]
                ]
                # Use the same material as the characters
                material_slot.material = bpy.data.materials["lambert2"]

            # Rename Meshes to be the same as their parent MeshObjects
            obj.data.name = obj.name


def fix_materials():
    # https://blender.stackexchange.com/a/280804
    for image in bpy.data.images.values():
        filename = os.path.basename(image.filepath)
        if image.source == "FILE":
            # Eye/Eyebrow pointing to wrong file in wrong directory. Fix that
            if filename == "PolygonFantasyHero_Texture_01.png":
                # Make absolute
                image.filepath = bpy.path.abspath(
                    "//Source_Files/Textures/PolygonFantasyHero_Texture_01.png"
                )

    for material in bpy.data.materials:
        if material.name == 'lambert2':
            material.name = 'POLYGONModularFantasyHeroes_Base'

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
import_weapons()
fix_materials()
cleanup()