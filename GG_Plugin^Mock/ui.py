import bpy

class GGPanel(bpy.types.Panel):
    bl_label = "GG Worlds"
    bl_idname = "VIEW3D_PT_gg"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GG'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("gg.connect_discord", text="Connect To Discord Server", icon="URL")

        layout.label(text="Personalized Path")
        row = layout.row(align=True)
        row.label(text="● Topography")
        row.label(text="───")
        row.label(text="○ Streets")
        row.label(text="───")
        row.label(text="○ Buildings")
        row.label(text="───")
        row.label(text="○ Landmarks")

        layout.operator("gg.generate_base_plane", text="Generate Base Plane")

        layout.separator()
        layout.label(text="Topography Generation")
        layout.prop(scene, "gg_prompt", text="")

        col = layout.column(align=True)
        col.operator("gg.generate_topography", text="Generate")
        col.operator("gg.get_topography_3d", text="Get 3D")
        col.operator("gg.next_phase", text="Next")
        layout.prop(scene, "gg_displacement_height", slider=True)

        if scene.gg_show_preview:
            layout.separator()
            layout.label(text="Heightmap Preview Gallery")
            row = layout.row()
            for i in range(1, 6):
                img = getattr(scene, f"gg_preview_image_{i}", None)
                if img:
                    col = row.column()
                    col.template_ID_preview(scene, f"gg_preview_image_{i}", new="", open="")
                    op = col.operator("gg.apply_heightmap", text="Apply")
                    op.image_name = img.name

            row = layout.row(align=True)
            row.operator("gg.edit_image", text="Edit Image")
            row.operator("gg.save_image", text="Save")
            row.operator("gg.ok_image", text="OK")
            layout.operator("gg.close_preview", text="Close Preview", icon="X")

        if scene.gg_show_street_preview:
            layout.separator()
            layout.label(text="Street Network Generation")
            layout.prop(scene, "gg_street_prompt", text="")
            col = layout.column(align=True)
            col.operator("gg.generate_streets", text="Generate Streets")
            col.operator("gg.get_streets_3d", text="Get 3D Streets")

            layout.label(text="Street Preview Gallery")
            row = layout.row()
            for i in range(1, 6):
                img = getattr(scene, f"gg_street_preview_image_{i}", None)
                if img:
                    col = row.column()
                    col.template_ID_preview(scene, f"gg_street_preview_image_{i}", new="", open="")
                    op = col.operator("gg.apply_streetmap", text="Apply")
                    op.image_name = img.name
