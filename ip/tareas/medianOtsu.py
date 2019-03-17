import sys
import os

sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]


path_input = sys.argv[1]
path_output = sys.argv[2]

from tareas.dependencias import utils
from tareas.dependencias import definitions as d
from dipy.segment.mask import median_otsu
import nibabel as nib
import numpy as np
median_radius = 4
num_pass = 4
# print('    - running Median Otsu algoritm...')

finalFileName = path_output + utils.to_extract_filename(path_input) + d.id_median_otsu + '_maskedVolume' + d.extension
binaryMaskFileName = path_output + utils.to_extract_filename(path_input) + d.id_median_otsu + '_binaryMask' + d.extension
b0MaskedFileName = path_output + utils.to_extract_filename(path_input) + d.id_median_otsu + '_b0Masked' + d.extension

if not (os.path.exists(finalFileName)):
    img = nib.load(path_input)
    data = img.get_data()
    maskedvolume, mask = median_otsu(data, median_radius, num_pass)

    nib.save(nib.Nifti1Image(maskedvolume.astype(np.float16), img.affine), finalFileName)
    nib.save(nib.Nifti1Image(mask.astype(np.float16), img.affine), binaryMaskFileName)
    nib.save(nib.Nifti1Image(maskedvolume[:, :, :, d.default_b0_ref].astype(np.float16), img.affine),
             b0MaskedFileName)

# return finalFileName, binaryMaskFileName
print(finalFileName)