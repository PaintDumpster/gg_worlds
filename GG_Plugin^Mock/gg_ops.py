import bpy
import os

class GenerateTopographyOperator(bpy.types.Operator):
    bl_idname = "gg.generate_topography"
    bl_label = "Generate Topography"

    def execute(self, context):
        print("🟣 [GG_09] Generate button is working!")
        scene = context.scene
        scene.gg_show_preview = True

        addon_dir = os.path.dirname(__file__)
        asset_path = os.path.join(addon_dir, "assets")

        for i in range(1, 6):
            img_name = f"{i:02d}.jpg"
            img_path = os.path.join(asset_path, img_name)
            try:
                image = bpy.data.images.load(img_path, check_existing=True)
                setattr(scene, f"gg_preview_image_{i}", image)
                print(f"✅ Loaded and assigned: {img_path}")
            except Exception as e:
                print(f"❌ Failed to load {img_path} — {e}")
        return {'FINISHED'}

class GetTopography3DOperator(bpy.types.Operator):
    bl_idname = "gg.get_topography_3d"
    bl_label = "Get 3D"

    def execute(self, context):
        print("🔧 Applying heightmap to plane (mock)...")
        return {'FINISHED'}

class NextPhaseOperator(bpy.types.Operator):
    bl_idname = "gg.next_phase"
    bl_label = "Next Phase"

    def execute(self, context):
        context.scene.gg_show_street_preview = True
        print("➡️ Next phase triggered: Street preview visible.")
        return {'FINISHED'}

class EditImageOperator(bpy.types.Operator):
    bl_idname = "gg.edit_image"
    bl_label = "Edit Image"

    def execute(self, context):
        print("✏️ Edit image placeholder.")
        return {'FINISHED'}

class SaveImageOperator(bpy.types.Operator):
    bl_idname = "gg.save_image"
    bl_label = "Save"

    def execute(self, context):
        print("💾 Save image placeholder.")
        return {'FINISHED'}

class OkImageOperator(bpy.types.Operator):
    bl_idname = "gg.ok_image"
    bl_label = "OK"

    def execute(self, context):
        print("✅ OK clicked.")
        return {'FINISHED'}

class ClosePreviewOperator(bpy.types.Operator):
    bl_idname = "gg.close_preview"
    bl_label = "Close Preview"

    def execute(self, context):
        context.scene.gg_show_preview = False
        print("🧹 Preview closed.")
        return {'FINISHED'}

class GenerateBasePlaneOperator(bpy.types.Operator):
    bl_idname = "gg.generate_base_plane"
    bl_label = "Generate Base Plane"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
        plane = bpy.context.active_object
        plane.name = "GG_Plane"

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=200)
        bpy.ops.object.mode_set(mode='OBJECT')

        subsurf = plane.modifiers.new(name="GG_Subdivision", type='SUBSURF')
        subsurf.levels = 5
        subsurf.render_levels = 5
        subsurf.subdivision_type = 'SIMPLE'

        print("📐 Base plane created with high mesh and Subsurf (Simple, 5 levels).")
        return {'FINISHED'}

class ApplyHeightmapOperator(bpy.types.Operator):
    bl_idname = "gg.apply_heightmap"
    bl_label = "Apply Heightmap"

    image_name: bpy.props.StringProperty()

    def execute(self, context):
        plane = bpy.data.objects.get("GG_Plane")
        if not plane:
            self.report({'ERROR'}, "Base plane 'GG_Plane' not found.")
            return {'CANCELLED'}

        image = bpy.data.images.get(self.image_name)
        if not image:
            self.report({'ERROR'}, f"Image '{self.image_name}' not found.")
            return {'CANCELLED'}

        tex = bpy.data.textures.new(name="GG_Heightmap_Texture", type='IMAGE')
        tex.image = image

        mod = plane.modifiers.new(name="GG_Displace", type='DISPLACE')
        mod.texture = tex
        mod.strength = context.scene.gg_displacement_height
        mod.texture_coords = 'UV'

        self.report({'INFO'}, f"Applied {self.image_name} as displacement.")
        print(f"🟣 Displacement applied using {self.image_name}")
        return {'FINISHED'}

class ConnectDiscordOperator(bpy.types.Operator):
    bl_idname = "gg.connect_discord"
    bl_label = "Connect To Discord Server"

    def execute(self, context):
        import webbrowser
        webbrowser.open("https://discord.gg/SMTw2Fjy")
        self.report({'INFO'}, "Redirecting to Discord...")
        return {'FINISHED'}


class GenerateStreetsOperator(bpy.types.Operator):
    bl_idname = "gg.generate_streets"
    bl_label = "Generate Streets"

    def execute(self, context):
        print("🛣️ Generate Streets button clicked")
        scene = context.scene
        scene.gg_show_street_preview = True
        addon_dir = os.path.dirname(__file__)
        asset_path = os.path.join(addon_dir, "assets")

        for i in range(1, 6):
            img_name = f"street_{i:02d}.png"
            img_path = os.path.join(asset_path, img_name)
            try:
                image = bpy.data.images.load(img_path, check_existing=True)
                setattr(scene, f"gg_street_preview_image_{i}", image)
                print(f"✅ Loaded and assigned street map: {img_path}")
            except Exception as e:
                print(f"❌ Failed to load {img_path} — {e}")
        return {'FINISHED'}

class GetStreets3DOperator(bpy.types.Operator):
    bl_idname = "gg.get_streets_3d"
    bl_label = "Get 3D Streets"

    def execute(self, context):
        print("🚧 3D Streets placeholder triggered.")
        return {'FINISHED'}

class ApplyStreetmapOperator(bpy.types.Operator):
    bl_idname = "gg.apply_streetmap"
    bl_label = "Apply Streetmap"

    image_name: bpy.props.StringProperty()

    def execute(self, context):
        plane = bpy.data.objects.get("GG_Plane")
        if not plane:
            self.report({'ERROR'}, "Base plane 'GG_Plane' not found.")
            return {'CANCELLED'}

        image = bpy.data.images.get(self.image_name)
        if not image:
            self.report({'ERROR'}, f"Street image '{self.image_name}' not found.")
            return {'CANCELLED'}

        tex = bpy.data.textures.new(name="GG_Street_Texture", type='IMAGE')
        tex.image = image

        mod = plane.modifiers.new(name="GG_Street_Displace", type='DISPLACE')
        mod.texture = tex
        mod.strength = 0.2
        mod.texture_coords = 'UV'

        self.report({'INFO'}, f"Applied street image: {self.image_name}")
        print(f"🛣️ Applied {self.image_name} as street displacement.")
        return {'FINISHED'}
