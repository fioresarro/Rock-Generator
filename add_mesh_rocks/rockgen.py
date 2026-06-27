# Original Author: Paul "BrikBot" Marshall (2011)
# Modern Layout & API Restoration: Fiorentino Sarro/Orras (2026)
# Updated for compatibility with Blender 4.2 and Blender 5.0+ Extended Architecture.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#  Licensed under the GNU General Public License, version 3 (GPLv3).
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh
from bpy_extras import object_utils
import random

class MESH_OT_generate_rocks(bpy.types.Operator):
    """Generate Procedural Low-Poly and High-Poly Rocks"""
    bl_idname = "mesh.generate_rocks"
    bl_label = "Add Rocks"
    bl_options = {'REGISTER', 'UNDO'}

    # --- PARAMETRI GENERALI E PRESET ---
    count: bpy.props.IntProperty(name="Number of rocks", default=1, min=1, max=100)
    
    preset_enum: bpy.props.EnumProperty(
        name="Presets",
        items=[
            ('DEFAULT', 'Default', 'Standard settings'),
            ('RIVER', 'River Rock', 'Smooth river stones'),
            ('ASTEROID', 'Asteroid', 'Rough space debris'),
            ('SANDSTONE', 'Sandstone', 'Flat layered rocks'),
            ('ICE', 'Ice', 'Sharp crystal formations')
        ],
        default='DEFAULT'
    )

    # --- ASSE X ---
    scale_x_lower: bpy.props.FloatProperty(name="Lower X", default=1.00, min=0.01)
    scale_x_upper: bpy.props.FloatProperty(name="Upper X", default=1.00, min=0.01)
    skew_x: bpy.props.FloatProperty(name="X skew", default=0.00)

    # --- ASSE Y ---
    scale_y_lower: bpy.props.FloatProperty(name="Lower Y", default=1.00, min=0.01)
    scale_y_upper: bpy.props.FloatProperty(name="Upper Y", default=1.00, min=0.01)
    skew_y: bpy.props.FloatProperty(name="Y skew", default=0.00)

    # --- ASSE Z ---
    scale_z_lower: bpy.props.FloatProperty(name="Lower Z", default=1.00, min=0.01)
    scale_z_upper: bpy.props.FloatProperty(name="Upper Z", default=1.00, min=0.01)
    skew_z: bpy.props.FloatProperty(name="Z skew", default=0.00)

    # --- OPZIONI TEXTURE E FORMA ---
    scale_displace: bpy.props.BoolProperty(name="Scale displace textures", default=False)
    deformation: bpy.props.FloatProperty(name="Deformation", default=5.00, min=0.0)
    roughness: bpy.props.FloatProperty(name="Roughness", default=2.50, min=0.0)
    detail_level: bpy.props.IntProperty(name="Detail level", default=3, min=0, max=5)
    display_detail: bpy.props.IntProperty(name="Display Detail", default=2, min=0, max=5)
    smooth_factor: bpy.props.FloatProperty(name="Smooth Factor", default=0.00, min=0.0, max=2.0)
    smooth_iterations: bpy.props.IntProperty(name="Smooth Iterations", default=0, min=0, max=10)
    
    generate_rocks: bpy.props.BoolProperty(name="Generate Rocks", default=True)
    use_random_seed: bpy.props.BoolProperty(name="Use a random seed", default=True)

    def draw(self, context):
        """Ricostruzione fedele del layout visivo originale (prima sopra/sotto.JPG)"""
        layout = self.layout
        
        # Numero di rocce
        layout.prop(self, "count")
        
        # Blocco Scale / Skew degli Assi (X, Y, Z)
        box_axes = layout.box()
        
        # Sezione X
        box_axes.label(text="X scale:")
        col_x = box_axes.column(align=True)
        col_x.prop(self, "scale_x_upper", text="")
        col_x.prop(self, "scale_x_lower", text="")
        box_axes.prop(self, "skew_x")
        
        # Sezione Y
        box_axes.label(text="Y scale:")
        col_y = box_axes.column(align=True)
        col_y.prop(self, "scale_y_upper", text="")
        col_y.prop(self, "scale_y_lower", text="")
        box_axes.prop(self, "skew_y")
        
        # Sezione Z
        box_axes.label(text="Z scale:")
        col_z = box_axes.column(align=True)
        col_z.prop(self, "scale_z_upper", text="")
        col_z.prop(self, "scale_z_lower", text="")
        box_axes.prop(self, "skew_z")
        
        # Checkbox texture scale
        box_axes.prop(self, "scale_displace")
        
        # Blocco Parametri di Modellazione (Deform, Rough, Detail, Smooth)
        box_shape = layout.box()
        box_shape.prop(self, "deformation")
        box_shape.prop(self, "roughness")
        box_shape.prop(self, "detail_level")
        box_shape.prop(self, "display_detail")
        box_shape.prop(self, "smooth_factor")
        box_shape.prop(self, "smooth_iterations")
        
        # Sezione Inferiore di Controllo Finale
        layout.prop(self, "generate_rocks")
        layout.prop(self, "use_random_seed")
        layout.prop(self, "preset_enum")

    def execute(self, context):
        if not self.generate_rocks:
            return {'FINISHED'}

        # Geometria di base per lo scafo della roccia
        base_verts = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]

        for i in range(self.count):
            mesh_data = bpy.data.meshes.new(f"RockMesh_{i}")
            mesh_data.from_pydata(base_verts, [], faces)
            mesh_data.update()
            
            obj = object_utils.object_data_add(context, mesh_data)
            
            # Posizionamento e applicazione dei parametri di Scala estratti dagli intervalli dell'interfaccia
            x_scale = random.uniform(self.scale_x_lower, self.scale_x_upper)
            y_scale = random.uniform(self.scale_y_lower, self.scale_y_upper)
            z_scale = random.uniform(self.scale_z_lower, self.scale_z_upper)
            obj.scale = (x_scale, y_scale, z_scale)
            
            # Spostamento casuale nello spazio
            obj.location = (random.uniform(-4, 4), random.uniform(-4, 4), 0)
            
            # Shading liscio moderno (Blender 4+)
            for poly in mesh_data.polygons:
                poly.use_smooth = True
                
            # Modificatore di Suddivisione Superficie basato sul livello di dettaglio inserito
            if self.detail_level > 0:
                subsurf = obj.modifiers.new(name="Subdivisions", type='SUBSURF')
                subsurf.levels = self.display_detail
                subsurf.render_levels = self.detail_level
            
            # Modificatore Displace controllato da Deformation e Roughness
            if self.deformation > 0:
                disp = obj.modifiers.new(name="RockDisplace", type='DISPLACE')
                tex = bpy.data.textures.new(name=f"RockNoise_{i}", type='NOISE')
                disp.texture = tex
                disp.strength = (self.deformation * 0.05) * (self.roughness * 0.4)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_generate_rocks)

def unregister():
    bpy.utils.unregister_class(MESH_OT_generate_rocks)

if __name__ == "__main__":
    register()
