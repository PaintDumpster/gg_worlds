
import bpy
import os
import requests
import time

BACKEND_URL = "http://localhost:5000/generate"

class GenerateTopographyOperator(bpy.types.Operator):
    bl_idname = "gg.generate_topography"
    bl_label = "Generate Topography"

    def execute(self, context):
        scene = context.scene
        scene.gg_processing = True
        self.report({'INFO'}, '🌀 Processing Prompt...')
        prompt = scene.gg_prompt

        try:
            response = requests.post(BACKEND_URL, json={"prompt": prompt})
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success" or "image_path" not in data:
                self.report({'ERROR'}, "Backend failed or did not return image path")
                scene.gg_processing = False
                return {'CANCELLED'}

            image_path = data["image_path"]

            for _ in range(10):
                if os.path.exists(image_path):
                    break
                time.sleep(0.5)
            else:
                self.report({'ERROR'}, f"Image not found: {image_path}")
                scene.gg_processing = False
                return {'CANCELLED'}

            image = bpy.data.images.load(image_path, check_existing=True)
            scene.gg_preview_image_1 = image
            scene.gg_show_preview = True
            scene.gg_processing = False
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
            scene.gg_processing = False
            return {'CANCELLED'}

class GenerateBasePlaneOperator(bpy.types.Operator):
    bl_idname = "gg.generate_base_plane"
    bl_label = "Generate Base Plane"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
        plane = bpy.context.active_object
        plane.name = "GG_BasePlane"

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=100)
        bpy.ops.object.mode_set(mode='OBJECT')

        disp = plane.modifiers.new(name="Displace", type='DISPLACE')
        disp.strength = 1
        tex = bpy.data.textures.new("GG_DisplaceTex", type='IMAGE')
        disp.texture = tex
        disp.texture_coords = 'UV'

        subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 4
        subsurf.render_levels = 0

        return {'FINISHED'}

class PreviewHeightmapOperator(bpy.types.Operator):
    bl_idname = "gg.preview_heightmap"
    bl_label = "Preview Heightmap"

    def execute(self, context):
        scene = context.scene
        plane = bpy.data.objects.get("GG_BasePlane")
        if not plane:
            self.report({'ERROR'}, "Base plane not found.")
            return {'CANCELLED'}

        image = scene.gg_preview_image_1
        if not image:
            self.report({'ERROR'}, "No image to preview.")
            return {'CANCELLED'}

        mat = bpy.data.materials.get("GG_Heightmap_Mat")
        if not mat:
            mat = bpy.data.materials.new(name="GG_Heightmap_Mat")
            mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        output = nodes.new(type="ShaderNodeOutputMaterial")
        shader = nodes.new(type="ShaderNodeBsdfPrincipled")
        tex_image = nodes.new(type="ShaderNodeTexImage")
        tex_image.image = image

        links.new(shader.outputs["BSDF"], output.inputs["Surface"])
        links.new(tex_image.outputs["Color"], shader.inputs["Base Color"])

        plane.data.materials.clear()
        plane.data.materials.append(mat)

        return {'FINISHED'}

class ApplyHeightmapOperator(bpy.types.Operator):
    bl_idname = "gg.apply_heightmap"
    bl_label = "Apply Heightmap"

    def execute(self, context):
        scene = context.scene
        image = scene.gg_preview_image_1
        plane = bpy.data.objects.get("GG_BasePlane")
        if not plane or not image:
            self.report({'ERROR'}, "Missing plane or image.")
            return {'CANCELLED'}

        for mod in plane.modifiers:
            if mod.type == 'DISPLACE' and mod.texture:
                mod.texture.image = image

        return {'FINISHED'}
