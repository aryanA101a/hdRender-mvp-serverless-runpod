import bpy
import sys
import datetime
import math

#Get Email
email = sys.argv[5]

#Get Desired Resolution
Resolution = sys.argv[6]
resolution_float = float(Resolution)
resolution_integer = int(resolution_float)

# For Delete Default Objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Replace the filepath with the location of your GLB file
filepath = "Assets/GLB_Files/" + email + ".glb"

# Import the GLB file
bpy.ops.import_scene.gltf(filepath=filepath)

# Specify the name of the object to be deleted
object_name = "temp001_4"

# Check if the object exists
if object_name in bpy.data.objects:
    obj = bpy.data.objects[object_name]

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object to delete
    obj.select_set(True)

    # Delete the selected object
    bpy.ops.object.delete()

# Define the object name and emission increase value
emissive_object = 'temp001_7'  # Replace with your object's name

def modify_material(material):
    if material.use_nodes:
        # Access the existing node tree
        node_tree = material.node_tree

        # Find or create the Principled BSDF node
        principled_bsdf = node_tree.nodes.get("Principled BSDF")
        if not principled_bsdf:
            principled_bsdf = node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            principled_bsdf.location = (0, 0)

        # Find or create the Transparent BSDF node
        transparent_bsdf = node_tree.nodes.get("Transparent BSDF")
        if not transparent_bsdf:
            transparent_bsdf = node_tree.nodes.new('ShaderNodeBsdfTransparent')
            transparent_bsdf.location = (0, 200)

        # Find or create the Mix Shader node
        mix_shader = node_tree.nodes.get("Mix Shader")
        if not mix_shader:
            mix_shader = node_tree.nodes.new('ShaderNodeMixShader')
            mix_shader.location = (400, 0)

        # Find or create the Geometry node
        geometry_node = node_tree.nodes.get("Geometry")
        if not geometry_node:
            geometry_node = node_tree.nodes.new('ShaderNodeNewGeometry')
            geometry_node.location = (-200, 400)

        # Connect the shaders to the mix shader node
        node_tree.links.new(principled_bsdf.outputs['BSDF'], mix_shader.inputs[1])
        node_tree.links.new(transparent_bsdf.outputs['BSDF'], mix_shader.inputs[2])

        # Connect the Geometry node to the factor input of the mix shader
        node_tree.links.new(geometry_node.outputs['Backfacing'], mix_shader.inputs['Fac'])

        # Find or create the Material Output node
        material_output = node_tree.nodes.get("Material Output")
        if not material_output:
            material_output = node_tree.nodes.new('ShaderNodeOutputMaterial')
            material_output.location = (800, 0)

        # Connect the Mix Shader node to the Material Output node
        node_tree.links.new(mix_shader.outputs['Shader'], material_output.inputs['Surface'])
    else:
        print("Material does not have a node tree.")


# Get the material names to modify
material_names = ["Main_wall1", "wall1", "wall2", "Main_wall2","wall3","Main_wall3"]

for material_name in material_names:
    material = bpy.data.materials.get(material_name)
    if material:
        modify_material(material)
        print("Material modified: {}".format(material_name))
    else:
        print("Material not found: {}".format(material_name))

# Get the sunlight object (assuming you have only one sun lamp)
sunlight = next((lamp for lamp in bpy.data.lights if lamp.type == 'SUN'), None)

if sunlight and sunlight.energy <= 0:
    # Adding Area Light
    bpy.ops.object.light_add(type='AREA', location=(0.000792, -0.061875, 2.98937))
    arealight = bpy.context.object
    arealight.scale = (6.5, 8.125, 6.5)
    arealight.rotation_euler = (math.radians(0), math.radians(0), math.radians(0))
    arealight.data.energy = 0.5

    # Find the object by name
    obj = bpy.data.objects.get(emissive_object)

    if obj is not None:
        # Check if the object has a material
        if obj.data.materials:
            # Assume we're working with the first material assigned to the object
            material = obj.data.materials[0]

            # Find the Principled BSDF shader node in the material's node tree
            principled_node = None
            for node in material.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    principled_node = node
                    break

            if principled_node:
                # Increase the emission strength value of the Principled BSDF shader
                principled_node.inputs['Emission Strength'].default_value = 25.0

                print(
                    f"Emission strength in material of object '{emissive_object}' increased by 5")
            else:
                print(f"No Principled BSDF shader node found in the material of object '{emissive_object}'")
        else:
            print(f"No material assigned to object '{emissive_object}'")
    else:
        print(f"Object '{emissive_object}' not found")

# Get all the lights from the scene
lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']

# Increase the power of each light
for light in lights:
    light.data.energy *= 100  # Adjust the multiplication factor as desired

    # Get the light data
    light_data = light.data

    # Set the light radius to 0.25m
    light_data.shadow_soft_size = 0.25

    # Enable nodes for the light data
    light_data.use_nodes = True

    # Get the light node tree
    tree = light_data.node_tree

    # Clear existing nodes
    tree.nodes.clear()

    # Add the Blackbody node
    blackbody_node = tree.nodes.new(type='ShaderNodeBlackbody')

    # Set the desired temperature for the blackbody color
    temperature = 5500  # Adjust the temperature as desired
    blackbody_node.inputs['Temperature'].default_value = temperature

    # Add the Emission node
    emission_node = tree.nodes.new(type='ShaderNodeEmission')
    emission_node.inputs['Strength'].default_value = 10  # Set the emission strength to 10

    # Add the Surface node
    surface_node = tree.nodes.new(type='ShaderNodeOutputWorld')

    # Connect the Blackbody node output to the Emission node input
    tree.links.new(blackbody_node.outputs['Color'], emission_node.inputs['Color'])

    # Connect the Emission node output to the Surface node input
    tree.links.new(emission_node.outputs['Emission'], surface_node.inputs['Surface'])

# Find Spot lights by name
light_names = ["Spot001", "Spot002", "Spot003"]
lights_to_change = [bpy.data.objects[name] for name in light_names if name in bpy.data.objects]

# Set the new shadow soft size for the lights
new_shadow_soft_size = 0.05

# Change the shadow soft size for each light
for light in lights_to_change:
    if light.type == 'LIGHT':
        light.data.shadow_soft_size = new_shadow_soft_size

def create_world():
    # Check if a world already exists, if not, create one
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new('World')

def change_hdri_image(image_path):
    create_world()

    # Get the world environment
    world = bpy.context.scene.world

    # Check the sunlight intensity
    if sunlight and sunlight.energy > 0:
        # Clear existing environment textures
        world.use_nodes = True
        node_tree = world.node_tree
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        for light in lights:
            light.data.energy *= 50  # Adjust the multiplication factor as desired

        # Add a new Environment Texture node
        env_texture_node = node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        env_texture_node.location = (0, 0)

        # Set the HDRI image path
        env_texture_node.image = bpy.data.images.load(image_path)

        # Add a Background node to connect the Environment Texture node to the Background
        bg_node = node_tree.nodes.new(type='ShaderNodeBackground')
        bg_node.location = (400, 0)

        # Connect the Environment Texture node to the Background node
        node_tree.links.new(env_texture_node.outputs['Color'], bg_node.inputs['Color'])

        # Create the "World Output" node if it doesn't exist
        if 'World Output' not in node_tree.nodes:
            world_output = node_tree.nodes.new(type='ShaderNodeOutputWorld')
            world_output.location = (800, 0)

        # Connect the Background node to the "World Output" node
        node_tree.links.new(bg_node.outputs['Background'], node_tree.nodes['World Output'].inputs['Surface'])

        # Add three area lights
        bpy.ops.object.light_add(type='AREA', location=(-3.37597, 2.47, 1.00483))
        light1 = bpy.context.object
        light1.scale = (1.9992, 1.2, 1.2)
        light1.rotation_euler = (math.radians(0), math.radians(-90), math.radians(0))
        light1.data.energy = 100

        bpy.ops.object.light_add(type='AREA', location=(-1.63421, 4.02, 1.00483))
        light2 = bpy.context.object
        light2.scale = (1.9992, 1.2, 1.2)
        light2.rotation_euler = (math.radians(0), math.radians(-90), math.radians(-90))
        light2.data.energy = 100

        bpy.ops.object.light_add(type='AREA', location=(1.36579, 4.02, 1.00483))
        light3 = bpy.context.object
        light3.scale = (1.9992, 1.2, 1.2)
        light3.rotation_euler = (math.radians(0), math.radians(-90), math.radians(-90))
        light3.data.energy = 100

        # Set the location and scale of the cube
        cube_location = (0.0, 0.0, 1.499)  # (X, Y, Z) coordinates
        cube_scale = (3.4986, 4.116, 1.62925)  # (X, Y, Z) scaling factors

        # Add the cube to the scene
        bpy.ops.mesh.primitive_cube_add(location=cube_location, scale=cube_scale)

        # Get the last added object (which is the cube in this case)
        cube = bpy.context.object

        # Rename the cube
        cube.name = "Volumetric_Effect"

        # Create a new material for the cube
        cube_material = bpy.data.materials.new(name="Volumetric_Material")
        cube.data.materials.append(cube_material)

        # Set the material nodes for Volume Scatter shader
        cube_material.use_nodes = True
        nodes = cube_material.node_tree.nodes
        for node in nodes:
            cube_material.node_tree.nodes.remove(node)

        # Add Volume Scatter shader node
        volume_scatter_node = nodes.new(type='ShaderNodeVolumeScatter')

        # Connect nodes
        links = cube_material.node_tree.links

        # Create Material Output node if not exists
        material_output_node = nodes.get("Material Output")
        if material_output_node is None:
            material_output_node = nodes.new(type='ShaderNodeOutputMaterial')

        # Connect Volume Scatter shader to the volume input of the Material Output node
        volume_input = material_output_node.inputs['Volume']
        if volume_input.is_linked:
            for link in volume_input.links[:]:
                cube_material.node_tree.links.remove(link)
        links.new(volume_scatter_node.outputs['Volume'], volume_input)

        # Set Density and Anisotropy values using input sockets
        density_input = volume_scatter_node.inputs['Density']
        anisotropy_input = volume_scatter_node.inputs['Anisotropy']

        # Set Density and Anisotropy values
        density_input.default_value = 0.04
        anisotropy_input.default_value = 0.2

        # Find the object by name
        obj = bpy.data.objects.get(emissive_object)

        if obj is not None:
            # Check if the object has a material
            if obj.data.materials:
                # Assume we're working with the first material assigned to the object
                material = obj.data.materials[0]

                # Find the Principled BSDF shader node in the material's node tree
                principled_node = None
                for node in material.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        principled_node = node
                        break

                if principled_node:
                    # Increase the emission strength value of the Principled BSDF shader
                    principled_node.inputs['Emission Strength'].default_value = 5.0

                    print(
                        f"Emission strength in material of object '{emissive_object}' increased by 5")
                else:
                    print(f"No Principled BSDF shader node found in the material of object '{emissive_object}'")
            else:
                print(f"No material assigned to object '{emissive_object}'")
        else:
            print(f"Object '{emissive_object}' not found")

# Example usage
image_path = "Assets/HDRI/autumn_forest_01_4k.hdr"
change_hdri_image(image_path)

# Find the camera object by type
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        camera_obj = obj
        break

# Assign the camera object to the active scene
bpy.context.scene.camera = camera_obj

# Set the rendering engine to Cycles
bpy.context.scene.render.engine = 'CYCLES'
cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
cycles_prefs.compute_device_type = 'OPTIX'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Set resolution and samples
bpy.context.scene.render.resolution_x = 1175*resolution_integer
bpy.context.scene.render.resolution_y = 1000*resolution_integer
bpy.context.scene.cycles.samples = 100

# Enable denoising
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'

#Performance
bpy.context.scene.cycles.debug_use_spatial_splits = True
bpy.context.scene.render.use_persistent_data = True

# Set view settings
bpy.context.scene.view_settings.look = 'AgX - High Contrast'
bpy.context.scene.view_settings.exposure = 0
bpy.context.scene.cycles.diffuse_bounces = 6
bpy.context.scene.cycles.glossy_bounces = 6
bpy.context.scene.cycles.sample_clamp_direct = 9
bpy.context.scene.cycles.sample_clamp_indirect = 9

# Enable passes
view_layer = bpy.context.view_layer
view_layer.use_pass_ambient_occlusion = True
view_layer.use_pass_shadow = True
view_layer.use_pass_emit = True

# Render the image to a file
current_datetime = datetime.datetime.now().strftime("_%Y/%d-%m/%H-%M_")
output_filename = email.split('@')[0] + current_datetime + 'Render_Image.PNG'
output_path = 'Assets/Render_Images/' + output_filename
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
