bl_info = {
    "name": "GG Worlds",
    "author": "Amoebas Inc.",
    "version": (0, 10),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GG",
    "description": "Simulated 3D environment generator with previewable topography and streets",
    "category": "3D View",
}

import bpy
from . import ui, gg_ops

classes = (
    gg_ops.GenerateTopographyOperator,
    gg_ops.GetTopography3DOperator,
    gg_ops.NextPhaseOperator,
    gg_ops.EditImageOperator,
    gg_ops.SaveImageOperator,
    gg_ops.OkImageOperator,
    gg_ops.ClosePreviewOperator,
    gg_ops.GenerateBasePlaneOperator,
    gg_ops.ApplyHeightmapOperator,
    gg_ops.ConnectDiscordOperator,
    gg_ops.GenerateStreetsOperator,
    gg_ops.GetStreets3DOperator,
    gg_ops.ApplyStreetmapOperator,
    ui.GGPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.gg_prompt = bpy.props.StringProperty(name="Prompt", default="Describe your topography")
    bpy.types.Scene.gg_show_preview = bpy.props.BoolProperty(name="Show Preview", default=False)
    bpy.types.Scene.gg_displacement_height = bpy.props.FloatProperty(name="Displacement Height", default=0.5, min=0.0, max=5.0)
    for i in range(1, 6):
        setattr(bpy.types.Scene, f"gg_preview_image_{i}", bpy.props.PointerProperty(type=bpy.types.Image))

    bpy.types.Scene.gg_street_prompt = bpy.props.StringProperty(name="Street Prompt", default="Describe the street layout")
    bpy.types.Scene.gg_show_street_preview = bpy.props.BoolProperty(name="Show Street Preview", default=False)
    for i in range(1, 6):
        setattr(bpy.types.Scene, f"gg_street_preview_image_{i}", bpy.props.PointerProperty(type=bpy.types.Image))

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.gg_prompt
    del bpy.types.Scene.gg_show_preview
    del bpy.types.Scene.gg_displacement_height
    for i in range(1, 6):
        delattr(bpy.types.Scene, f"gg_preview_image_{i}")

    del bpy.types.Scene.gg_street_prompt
    del bpy.types.Scene.gg_show_street_preview
    for i in range(1, 6):
        delattr(bpy.types.Scene, f"gg_street_preview_image_{i}")

if __name__ == "__main__":
    register()
