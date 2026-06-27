# Original Author: Paul "BrikBot" Marshall (2011)
# Modern Settings & Preset Bridge: Il Tuo Nome/Nickname (2026)
# Updated for compatibility with Blender 4.2 and Blender 5.0+ Extended Architecture.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#  Licensed under the GNU General Public License, version 3 (GPLv3).
# ##### END GPL LICENSE BLOCK #####

try:
    # random_integers è deprecato/rimosso in NumPy moderno, usiamo randint
    from numpy.random import randint
    from numpy.random import normal as gauss
    from numpy.random import (
        beta,
        uniform,
    )
except:
    from random import (
        randint,
        gauss,
        uniform,
    )
    from random import betavariate as beta

from .utils import skewedGauss


def randomizeTexture(texture, level=1):
    '''
    Set the values for a texture from parameters.

    param: texture - bpy.data.texture to modify.
    level   - designated tweaked settings to use
    -> Below 10 is a displacment texture
    -> Between 10 and 20 is a base material texture
    '''
    noises = ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN', 'IMPROVED_PERLIN',
              'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4',
              'VORONOI_F2_F1', 'VORONOI_CRACKLE']
              
    if texture.type == 'CLOUDS':
        if randint(0, 1) == 0:
            texture.noise_type = 'SOFT_NOISE'
        else:
            texture.noise_type = 'HARD_NOISE'
        if level != 11:
            tempInt = randint(0, 6)
        else:
            tempInt = randint(0, 8)
        texture.noise_basis = noises[tempInt]
        texture.noise_depth = 8

        if level == 0:
            texture.noise_scale = gauss(0.625, 1 / 24)
        elif level == 2:
            texture.noise_scale = 0.15
        elif level == 11:
            texture.noise_scale = gauss(0.5, 1 / 24)

            if texture.noise_basis in ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN',
                                       'IMPROVED_PERLIN', 'VORONOI_F1']:
                texture.intensity = gauss(1, 1 / 6)
                texture.contrast = gauss(4, 1 / 3)
            elif texture.noise_basis in ['VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4']:
                texture.intensity = gauss(0.25, 1 / 12)
                texture.contrast = gauss(2, 1 / 6)
            elif texture.noise_basis == 'VORONOI_F2_F1':
                texture.intensity = gauss(0.5, 1 / 6)
                texture.contrast = gauss(2, 1 / 6)
            elif texture.noise_basis == 'VORONOI_CRACKLE':
                texture.intensity = gauss(0.5, 1 / 6)
                texture.contrast = gauss(2, 1 / 6)
                
    elif texture.type == 'MUSGRAVE':
        # Nota: Le texture Musgrave legacy potrebbero non essere supportate a seconda della versione esatta di Blender, 
        # aggiungiamo un controllo di sicurezza per evitare crash se i parametri non esistono più.
        try:
            texture.musgrave_type = 'MULTIFRACTAL'
            texture.dimension_max = abs(gauss(0, 0.6)) + 0.2
            texture.lacunarity = beta(3, 8) * 8.2 + 1.8

            if level == 0:
                texture.noise_scale = gauss(0.625, 1 / 24)
                texture.noise_intensity = 0.2
                texture.octaves = 1.0
            elif level == 2:
                texture.intensity = gauss(1, 1 / 6)
                texture.contrast = 0.2
                texture.noise_scale = 0.15
                texture.octaves = 8.0
            elif level == 10:
                texture.intensity = gauss(0.25, 1 / 12)
                texture.contrast = gauss(1.5, 1 / 6)
                texture.noise_scale = 0.5
                texture.octaves = 8.0
            elif level == 12:
                texture.octaves = uniform(1, 3)
            elif level > 12:
                texture.octaves = uniform(2, 8)
            else:
                texture.intensity = gauss(1, 1 / 6)
                texture.contrast = 0.2
                texture.octaves = 8.0
        except AttributeError:
            # Fallback sicuro se Blender ha rimosso del tutto i parametri Musgrave nativi vecchio stile
            if hasattr(texture, "noise_scale"):
                texture.noise_scale = gauss(0.5, 1 / 24)

    elif texture.type == 'DISTORTED_NOISE':
        tempInt = randint(0, 8)
        texture.noise_distortion = noises[tempInt]
        tempInt = randint(0, 8)
        texture.noise_basis = noises[tempInt]
        texture.distortion = skewedGauss(2.0, 2.6666, (0.0, 10.0), False)

        if level == 0:
            texture.noise_scale = gauss(0.625, 1 / 24)
        elif level == 2:
            texture.noise_scale = 0.15
        elif level >= 12:
            texture.noise_scale = gauss(0.2, 1 / 48)
            
    # L'intero blocco 'STUCCI' è stato rimosso perché la proprietà non esiste più nel bpy moderno.
    
    elif texture.type == 'VORONOI':
        metrics = ['DISTANCE', 'DISTANCE_SQUARED', 'MANHATTAN', 'CHEBYCHEV',
                   'MINKOVSKY_HALF', 'MINKOVSKY_FOUR', 'MINKOVSKY']
        if level == 0:
            tempInt = randint(0, 1)
            texture.distance_metric = metrics[tempInt]
            texture.noise_scale = gauss(0.625, 1 / 24)
            texture.contrast = 0.5
            texture.intensity = 0.7
        elif level == 2:
            texture.noise_scale = 0.15
            tempInt = randint(0, 6)
            texture.distance_metric = metrics[tempInt]
        elif level >= 12:
            tempInt = randint(0, 1)
            texture.distance_metric = metrics[tempInt]
            texture.noise_scale = gauss(0.125, 1 / 48)
            texture.contrast = 0.5
            texture.intensity = 0.7
        else:
            tempInt = randint(0, 6)
            texture.distance_metric = metrics[tempInt]

    return
