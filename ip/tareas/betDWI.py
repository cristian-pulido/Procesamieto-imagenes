

import sys
import os

sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]


path_input = sys.argv[1]
path_output = sys.argv[2]


from tareas.dependencias import utils
from tareas.dependencias import definitions as d
from tareas.dependencias import fsl_wrapper as fsl
import nibabel as nib
import numpy as np
print('    - running BET with FSL...')



finalFileName = os.path.join(path_output,utils.to_extract_filename(path_input) + d.id_bet + '_dwi_masked' + d.extension)
binaryMaskFileName = os.path.join(path_output,utils.to_extract_filename(path_input) + d.id_bet + '_b0_masked_mask' + d.extension)
b0MaskedFileName = os.path.join(path_output,utils.to_extract_filename(path_input) + d.id_bet + '_b0_masked' + d.extension)

if not (os.path.exists(finalFileName)):

    fsl.bet(path_input, b0MaskedFileName, '-m -f .4')

    imgMask = nib.load(binaryMaskFileName)
    dataMask = imgMask.get_data()

    img = nib.load(path_input)
    data = img.get_data()

    data[dataMask == 0] = 0
    nib.save(nib.Nifti1Image(data.astype(np.float32), img.affine), finalFileName)

# return finalFileName, binaryMaskFileName, b0MaskedFileName
print("Ejecutando")
print(finalFileName)