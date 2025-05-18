
bl_info = {
    "name": "GG Worlds Alpha",
    "author": "Amoebas Inc.",
    "version": (0, 12),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GG",
    "description": "Simulated 3D environment generator with previewable topography",
    "category": "3D View",
}

import bpy
from . import ui, gg_ops

classes = (
    gg_ops.GenerateTopographyOperator,
    gg_ops.GenerateBasePlaneOperator,
    gg_ops.PreviewHeightmapOperator,
    gg_ops.ApplyHeightmapOperator,
    ui.ConnectDiscordOperator,
    ui.GGPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.gg_prompt = bpy.props.StringProperty(name="Prompt", default="Describe your topography")
    bpy.types.Scene.gg_processing = bpy.props.BoolProperty(name="Processing", default=False)
    bpy.types.Scene.gg_show_preview = bpy.props.BoolProperty(name="Show Preview", default=False)
    bpy.types.Scene.gg_preview_image_1 = bpy.props.PointerProperty(type=bpy.types.Image)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.gg_prompt
    del bpy.types.Scene.gg_processing
    del bpy.types.Scene.gg_show_preview
    del bpy.types.Scene.gg_preview_image_1

if __name__ == "__main__":
    register()
