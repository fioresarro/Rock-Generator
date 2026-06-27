# Paul "BrikBot" Marshall
# Created: October 12, 2011
# Updated for Modern Blender (v4.0+): 2026
#
# ##### BEGIN GPL LICENSE BLOCK #####
# GPL License text...
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import math

def toList(string_data):
    """
    Prende una stringa di numeri separati da virgole o spazi 
    e la converte in una lista pulita di float.
    Risolve le instabilità di parsing del vecchio modulo string.
    """
    if not string_data:
        return []
        
    # Sostituisce eventuali parentesi quadre o graffe se presenti nell'XML
    clean_string = string_data.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    
    # Se i dati sono separati da virgola
    if ',' in clean_string:
        split_data = clean_string.split(',')
    else:
        # Altrimenti separa per spazi vuoti generici
        split_data = clean_string.split()
        
    result = []
    for x in split_data:
        item = x.strip()
        if item:
            try:
                result.append(float(item))
            except ValueError:
                # Salta in modo sicuro elementi non numerici o testuali errati
                continue
                
    return result

def checkMatrix(matrix):
    """
    Verifica la validità strutturale di una matrice di trasformazione.
    """
    if not matrix:
        return False
    for row in matrix:
        if len(row) < 3:
            return False
    return True
