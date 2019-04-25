

import sys
import os

sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]


from tareas.dependencias import utils
from tareas.dependencias import definitions as d
import nibabel as nib
from dipy.align.reslice import reslice

path_input = sys.argv[1]
path_output = sys.argv[2]

vox_sz=d.vox_sz
print('    - runnning Reslice...')

finalFileName = os.path.join(path_output, utils.to_extract_filename(path_input) + d.id_reslice + d.extension)
if not (os.path.exists(finalFileName)):
    img = nib.load(path_input)
    data = img.get_data()
    affine = img.affine

    old_vox_sz = img.header.get_zooms()[:3]

    new_vox_sz = (vox_sz, vox_sz, vox_sz)

    # Si el tamano del voxel es isotropico, no es necesario hacer el reslice

    data, affine = reslice(data, affine, old_vox_sz, new_vox_sz)

    nib.save(nib.Nifti1Image(data, affine), finalFileName)
print(finalFileName)