# Paul "BrikBot" Marshall
# Created: July 1, 2011
# Original Homepage: http://post.darkarsenic.com/
#
# Modern Porting & Remix Author: Fiorentino Sarro/Orras (2026)
# Thanks to Gemini AI for structural adaptation to Blender 4.2+ / 5.0+ API.
#
# Thanks to Meta-Androco, RickyBlender, Ace Dragon, and PKHG for original testing.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Rock Generator",
    "author": "Paul Marshall (brikbot)",
    "version": (2, 0, 0),
    "blender": (4, 2, 0),  # Configurato per la compatibilità con Blender 4.2+ e 5.0
    "location": "View3D > Add > Mesh > Rock Generator",
    "description": "Adds a mesh rock to the Add Mesh menu",
    "doc_url": "https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Rock_Generator",
    "category": "Add Mesh"
}

# Gestione corretta del ricaricamento dei moduli interni dell'add-on
if "bpy" in locals():
    from importlib import reload
    if "rockgen" in locals():
        reload(rockgen)
else:
    from . import rockgen

import bpy

def menu_func(self, context):
    """Funzione di disegno per iniettare la voce nel menu Add > Mesh"""
    # Chiama l'ID operatore corretto registrato dentro rockgen
    layout = self.layout
    layout.operator("mesh.generate_rocks", text="Rock Generator", icon='MESH_ICOSPHERE')

def register():
    # 1. Registra le classi interne (l'operatore)
    rockgen.register()
    
    # 2. Aggancia la funzione al menu Add > Mesh di Blender
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    # 1. Rimuove il collegamento dal menu
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    
    # 2. Rimuove le classi interne
    rockgen.unregister()

if __name__ == "__main__":
    register()
