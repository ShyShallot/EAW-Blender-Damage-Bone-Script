import bpy
import mathutils
import time
import threading

# Define the string to include
inlcude_string = "HP"

# Function to create child bones for a specific armature object
def create_child_bones_for_armature(armature):
    # Check if the given armature is valid
    if armature and armature.type == 'ARMATURE':
        # Create a set to store the names of newly created bones
        created_bones = set()


        # Get the current time (used to track bone creation time)
        current_time = time.time()

        bones_list = frozenset(armature.data.edit_bones)
        
        # Iterate through all bones in the armature
        for bone in bones_list:
            # Check if the bone name contains the exclude_string
            if inlcude_string in bone.name:
                print(bone.name)
                # Calculate the direction vector of the bone
                bone_direction = (bone.tail - bone.head).normalized()

                # Calculate the new bone's head and tail locations
                new_bone_head = bone.head + 1.0 * bone_direction
                new_bone_tail = new_bone_head + (bone.tail - bone.head)

                # Create a new bone in front of the current bone
                new_bone_name = bone.name + "_EMIT"
                new_bone = armature.data.edit_bones.new(new_bone_name)
                new_bone.head = new_bone_head
                new_bone.tail = new_bone_tail

                # Make the new bone a child of the current bone
                new_bone.parent = bone

                # Add the name of the newly created bone to the set
                created_bones.add(new_bone_name)

                time.sleep(0.05)

        # Exit Edit Mode (in the main thread)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Re-enter Edit Mode to continue working with bones
        bpy.ops.object.mode_set(mode='EDIT')

        # Exit Edit Mode (in the main thread)
        bpy.ops.object.mode_set(mode='OBJECT')

    else:
        print("The provided object is not a valid armature.")

# Find the selected armature object
selected_objects = bpy.context.selected_objects
selected_armatures = [obj for obj in selected_objects if obj.type == 'ARMATURE']

# Check if there's a selected armature
if selected_armatures:
    # Take the first selected armature as the active armature
    active_armature = selected_armatures[0]

    # Set the armature as the active object
    bpy.context.view_layer.objects.active = active_armature

    # Enter Edit Mode (in the main thread)
    bpy.ops.object.mode_set(mode='EDIT')

    # Create child bones
    create_child_bones_for_armature(active_armature)

    # Exit Edit Mode (in the main thread)
    bpy.ops.object.mode_set(mode='OBJECT')


else:
    print("Please select an armature object in the 3D view.")
