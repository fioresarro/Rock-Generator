# Original Author: Paul "BrikBot" Marshall (2011)
# Modern Geometric Utilities Adaptation: Fiorentino Sarro/Orras (2026)
# Updated for compatibility with Blender 4.2 and Blender 5.0+ Extended Architecture.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#  Licensed under the GNU General Public License, version 3 (GPLv3).
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh
from bpy_extras import object_utils
import random

def update_preset(self, context):
    """Funzione di callback: quando l'utente cambia preset, aggiorna i valori nel pannello"""
    preset = self.preset_enum
    
    if preset == 'DEFAULT':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 1.0, 1.0, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 1.0, 1.0, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 1.0, 1.0, 0.0
        self.deformation, self.roughness, self.detail_level = 5.0, 2.5, 3
    elif preset == 'RIVER':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 1.5, 1.0, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 1.2, 0.8, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 0.4, 0.2, 0.0
        self.deformation, self.roughness, self.detail_level = 1.5, 0.5, 4
    elif preset == 'ASTEROID':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 2.0, 1.0, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 1.8, 0.9, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 1.5, 0.8, 0.0
        self.deformation, self.roughness, self.detail_level = 8.0, 4.5, 3
    elif preset == 'SANDSTONE':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 2.5, 1.5, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 2.5, 1.5, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 0.3, 0.1, 0.0
        self.deformation, self.roughness, self.detail_level = 3.0, 1.8, 3
    elif preset == 'ICE':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 1.2, 0.6, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 1.2, 0.6, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 2.5, 1.5, 0.0
        self.deformation, self.roughness, self.detail_level = 6.0, 5.0, 2
    elif preset == 'FAKE_OCEAN':
        self.scale_x_upper, self.scale_x_lower, self.skew_x = 4.0, 3.0, 0.0
        self.scale_y_upper, self.scale_y_lower, self.skew_y = 4.0, 3.0, 0.0
        self.scale_z_upper, self.scale_z_lower, self.skew_z = 0.5, 0.2, 0.0
        self.deformation, self.roughness, self.detail_level = 9.0, 1.5, 4

class MESH_OT_generate_rocks(bpy.types.Operator):
    """Generate Procedural Low-Poly and High-Poly Rocks"""
    bl_idname = "mesh.generate_rocks"
    bl_label = "Add Rocks"
    bl_options = {'REGISTER', 'UNDO'}

    count: bpy.props.IntProperty(name="Number of rocks", default=1, min=1, max=100)
    
    preset_enum: bpy.props.EnumProperty(
        name="Presets",
        items=[
            ('DEFAULT', 'Default', 'Standard settings'),
            ('RIVER', 'River Rock', 'Smooth river stones'),
            ('ASTEROID', 'Asteroid', 'Rough space debris'),
            ('SANDSTONE', 'Sandstone', 'Flat layered rocks'),
            ('ICE', 'Ice', 'Sharp crystal formations'),
            ('FAKE_OCEAN', 'Fake Ocean', 'Large flat layered displacements')
        ],
        default='DEFAULT',
        update=update_preset
    )

    # --- ASSE X ---
    scale_x_upper: bpy.props.FloatProperty(name="Upper X", default=1.00, min=0.01)
    scale_x_lower: bpy.props.FloatProperty(name="Lower X", default=1.00, min=0.01)
    skew_x: bpy.props.FloatProperty(name="X skew", default=0.00)

    # --- ASSE Y ---
    scale_y_upper: bpy.props.FloatProperty(name="Upper Y", default=1.00, min=0.01)
    scale_y_lower: bpy.props.FloatProperty(name="Lower Y", default=1.00, min=0.01)
    skew_y: bpy.props.FloatProperty(name="Y skew", default=0.00)

    # --- ASSE Z ---
    scale_z_upper: bpy.props.FloatProperty(name="Upper Z", default=1.00, min=0.01)
    scale_z_lower: bpy.props.FloatProperty(name="Lower Z", default=1.00, min=0.01)
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
        layout = self.layout
        layout.prop(self, "count")
        
        box_axes = layout.box()
        
        box_axes.label(text="X scale:")
        col_x = box_axes.column(align=True)
        col_x.prop(self, "scale_x_upper", text="")
        col_x.prop(self, "scale_x_lower", text="")
        box_axes.prop(self, "skew_x")
        
        box_axes.label(text="Y scale:")
        col_y = box_axes.column(align=True)
        col_y.prop(self, "scale_y_upper", text="")
        col_y.prop(self, "scale_y_lower", text="")
        box_axes.prop(self, "skew_y")
        
        box_axes.label(text="Z scale:")
        col_z = box_axes.column(align=True)
        col_z.prop(self, "scale_z_upper", text="")
        col_z.prop(self, "scale_z_lower", text="")
        box_axes.prop(self, "skew_z")
        
        box_axes.prop(self, "scale_displace")
        
        box_shape = layout.box()
        box_shape.prop(self, "deformation")
        box_shape.prop(self, "roughness")
        box_shape.prop(self, "detail_level")
        box_shape.prop(self, "display_detail")
        box_shape.prop(self, "smooth_factor")
        box_shape.prop(self, "smooth_iterations")
        
        layout.prop(self, "generate_rocks")
        layout.prop(self, "use_random_seed")
        layout.prop(self, "preset_enum")

    def execute(self, context):
        if not self.generate_rocks:
            return {'FINISHED'}

        base_verts = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]

        for i in range(self.count):
            mesh_data = bpy.data.meshes.new(f"RockMesh_{i}")
            mesh_data.from_pydata(base_verts, [], faces)
            mesh_data.update()
            
            obj = object_utils.object_data_add(context, mesh_data)
            
            x_scale = random.uniform(min(self.scale_x_lower, self.scale_x_upper), max(self.scale_x_lower, self.scale_x_upper))
            y_scale = random.uniform(min(self.scale_y_lower, self.scale_y_upper), max(self.scale_y_lower, self.scale_y_upper))
            z_scale = random.uniform(min(self.scale_z_lower, self.scale_z_upper), max(self.scale_z_lower, self.scale_z_upper))
            
            obj.scale = (x_scale, y_scale, z_scale)
            
            if self.count > 1:
                obj.location = (random.uniform(-4, 4), random.uniform(-4, 4), 0)
            else:
                obj.location = context.scene.cursor.location
            
            for poly in mesh_data.polygons:
                poly.use_smooth = True

            # =========================================================================
            # CATENA COMPLETA DI MODIFICATORI DA CODICE ORIGINALE (3 Displace, 2 Subsurf)
            # =========================================================================
            
            # --- LIVELLO 1: Sottodivisione Iniziale (Base Hull) ---
            if self.detail_level > 0:
                subsurf1 = obj.modifiers.new(name="RockSubsurf_1", type='SUBSURF')
                subsurf1.levels = max(1, self.display_detail - 1)
                subsurf1.render_levels = max(1, self.detail_level - 1)

            # --- LIVELLO 2: Primo Displace (Macro-deformazione a bassa frequenza) ---
            if self.deformation > 0:
                disp1 = obj.modifiers.new(name="RockDisplace_Macro", type='DISPLACE')
                tex1 = bpy.data.textures.new(name=f"RockTex_Macro_{i}", type='NOISE')
                disp1.texture = tex1
                disp1.strength = self.deformation * 0.15
                if self.scale_displace:
                    disp1.texture_coords = 'LOCAL'
                else:
                    disp1.texture_coords = 'GLOBAL'

            # --- LIVELLO 3: Seconda Sottodivisione (Genera densità per il dettaglio medio) ---
            if self.detail_level > 1:
                subsurf2 = obj.modifiers.new(name="RockSubsurf_2", type='SUBSURF')
                subsurf2.levels = 1
                subsurf2.render_levels = 1

            # --- LIVELLO 4: Secondo Displace (Forme medie e fessure) ---
            if self.deformation > 0:
                disp2 = obj.modifiers.new(name="RockDisplace_Medium", type='DISPLACE')
                tex2 = bpy.data.textures.new(name=f"RockTex_Medium_{i}", type='MARBLE')
                tex2.noise_scale = 0.5
                disp2.texture = tex2
                disp2.strength = self.deformation * 0.05
                if self.scale_displace:
                    disp2.texture_coords = 'LOCAL'
                else:
                    disp2.texture_coords = 'GLOBAL'

            # --- LIVELLO 5: Modificatore Smooth (Filtro erosione) ---
            if self.smooth_iterations > 0 or self.preset_enum == 'RIVER':
                smooth_mod = obj.modifiers.new(name="RockSmooth", type='SMOOTH')
                smooth_mod.factor = self.smooth_factor if self.smooth_factor > 0 else 0.4
                smooth_mod.iterations = self.smooth_iterations if self.smooth_iterations > 0 else 3

            # --- LIVELLO 6: Terzo Displace (Micro-rugosità e porosità superficiale) ---
            if self.roughness > 0:
                disp3 = obj.modifiers.new(name="RockDisplace_Micro", type='DISPLACE')
                tex3 = bpy.data.textures.new(name=f"RockTex_Micro_{i}", type='VORONOI')
                tex3.noise_scale = 0.15
                disp3.texture = tex3
                disp3.strength = self.roughness * 0.03
                if self.scale_displace:
                    disp3.texture_coords = 'LOCAL'
                else:
                    disp3.texture_coords = 'GLOBAL'

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_generate_rocks)

def unregister():
    bpy.utils.unregister_class(MESH_OT_generate_rocks)

if __name__ == "__main__":
    register()
