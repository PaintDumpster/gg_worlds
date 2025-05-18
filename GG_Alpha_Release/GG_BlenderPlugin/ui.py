
import bpy
import webbrowser

class GGPanel(bpy.types.Panel):
    bl_label = "GG Worlds (Alpha)"
    bl_idname = "VIEW3D_PT_gg"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GG'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("gg.connect_discord", text="Connect To Discord Server", icon="URL")

        # Updated progress bar label
        row = layout.row()
        row.label(text="● Topography  ───  ○ Streets (TBA)")

        layout.operator("gg.generate_base_plane", text="Generate Base Plane")

        layout.label(text="Topography Generation")
        layout.prop(scene, "gg_prompt", text="")

        layout.operator("gg.generate_topography", text="Generate")

        if scene.gg_show_preview:
            layout.template_ID_preview(scene, "gg_preview_image_1", hide_buttons=True)
            layout.operator("gg.preview_heightmap", text="Preview")
            layout.operator("gg.apply_heightmap", text="Apply")

class ConnectDiscordOperator(bpy.types.Operator):
    bl_idname = "gg.connect_discord"
    bl_label = "Connect to Discord"

    def execute(self, context):
        webbrowser.open("https://discord.gg/Dw23W5j5")
        return {'FINISHED'}
