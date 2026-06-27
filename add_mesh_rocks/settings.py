# Original Author: Paul "BrikBot" Marshall (2011)
# Modern Settings & Preset Bridge: Fiorentino Sarro/Orras (2026)
# Updated for compatibility with Blender 4.2 and Blender 5.0+ Extended Architecture.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#  Licensed under the GNU General Public License, version 3 (GPLv3).
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import os
import shutil
import bpy
from xml.dom import minidom

# Calcolo dei percorsi compatibile con il sistema di add-on moderno di Blender
basePath = os.path.dirname(__file__)
path = os.path.join(basePath, "add_mesh_rocks.xml")

# Gestione del file di configurazione
try:
    source = minidom.parse(path)
    print("Rock generator settings file found:\n" + path)
except Exception:
    print("Rock generator settings file not found. Creating settings file from factory defaults.")
    factory_path = os.path.join(basePath, "factory.xml")
    if os.path.exists(factory_path):
        shutil.copy(factory_path, path)
        try:
            source = minidom.parse(path)
        except Exception as e:
            print(f"Error parsing factory file: {e}")
            source = None
    else:
        print("Critical Error: factory.xml not found!")
        source = None

default = []
presets = []

# ----- Gets and Sets -----#

def getDefault():
    global default
    return default

def getPresetLists():
    global presets
    return presets

def getPreset(ID=0):
    global presets
    try:
        return presets[ID]
    except IndexError:
        return default

# ---------- Core ----------#

def parse():
    global source, default, presets
    if not source:
        return {'CANCELLED'}

    # Reset delle liste per evitare duplicazioni in caso di ricaricamento
    presets = []
    
    xmlDefault = source.getElementsByTagName('default')
    if xmlDefault:
        default = parseNode(xmlDefault[0], title=False)

    xmlPresets = source.getElementsByTagName('preset')
    for setting in xmlPresets:
        presets.append(parseNode(setting, title=True))

    return {'FINISHED'}

def get_text_from_tag(parent, tag_name, default_val="0.0"):
    """Funzione helper per estrarre in modo sicuro il testo da un tag specifico"""
    elements = parent.getElementsByTagName(tag_name)
    if elements and elements[0].firstChild:
        return elements[0].firstChild.data.strip()
    return default_val

def parseNode(setting, title=True):
    """
    Sito di estrazione sicuro basato sui nomi dei tag.
    Risolve definitivamente la fragilità dei nodi childNodes numerici del 2011.
    """
    parsed = []
    
    if title:
        # Estrae il nome del preset
        name_tag = setting.getElementsByTagName('name')
        preset_title = name_tag[0].firstChild.data.strip() if name_tag and name_tag[0].firstChild else "Unnamed Preset"
        parsed.append(preset_title)

    # --- Sezione Size/Scale ---
    # Cerchiamo i blocchi min/max in modo robusto tramite i tag dedicati
    def get_min_max(axis_tag_name):
        axis_element = setting.getElementsByTagName(axis_tag_name)
        if axis_element:
            v_min = float(get_text_from_tag(axis_element[0], 'min', '1.0'))
            v_max = float(get_text_from_tag(axis_element[0], 'max', '1.0'))
            return [v_min, v_max]
        return [1.0, 1.0]

    scaleX = get_min_max('scaleX')
    scaleY = get_min_max('scaleY')
    scaleZ = get_min_max('scaleZ')
    
    skewX = float(get_text_from_tag(setting, 'skewX', '0.0'))
    skewY = float(get_text_from_tag(setting, 'skewY', '0.0'))
    skewZ = float(get_text_from_tag(setting, 'skewZ', '0.0'))
    
    use_scale_dis = get_text_from_tag(setting, 'use_scale_dis', 'False') == 'True'
    
    # Gestione sicura della conversione della stringa in lista (es: "1,2,3")
    scale_fac_str = get_text_from_tag(setting, 'scale_fac', '1.0,1.0,1.0')
    scale_fac = [float(x) for x in scale_fac_str.split(',') if x.strip()]

    parsed.extend([scaleX, scaleY, scaleZ, skewX, skewY, skewZ, use_scale_dis, scale_fac])

    # --- Sezione Shape ---
    deform = float(get_text_from_tag(setting, 'deform', '0.3'))
    rough = float(get_text_from_tag(setting, 'rough', '2.0'))
    detail = int(get_text_from_tag(setting, 'detail', '3'))
    display_detail = int(get_text_from_tag(setting, 'display_detail', '3'))
    smooth_fac = float(get_text_from_tag(setting, 'smooth_fac', '0.5'))
    smooth_it = int(get_text_from_tag(setting, 'smooth_it', '1'))

    parsed.extend([deform, rough, detail, display_detail, smooth_fac, smooth_it])

    # --- Sezione Random / Seed ---
    use_generate = get_text_from_tag(setting, 'use_generate', 'True') == 'True'
    use_random_seed = get_text_from_tag(setting, 'use_random_seed', 'True') == 'True'
    user_seed = int(get_text_from_tag(setting, 'user_seed', '0'))

    parsed.extend([use_generate, use_random_seed, user_seed])

    return parsed

def save():
    # Lasciato come stub per compatibilità con la vecchia architettura dell'add-on
    return {'FINISHED'}

def _print():
    for i in presets:
        print(i)
    return {'FINISHED'}
