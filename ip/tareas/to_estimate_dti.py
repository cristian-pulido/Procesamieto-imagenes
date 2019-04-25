import os
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


from tareas.dependencias import definitions as d
from tareas.dependencias import utils

import nibabel as nib
import numpy as np
import dipy.reconst.dti as dti
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table


###################
folder_sujeto=path_output
for l in os.listdir(folder_sujeto):
    if "TENSOR" in l and "bval" in l:
        fbval=os.path.join(folder_sujeto,l)
    if "TENSOR" in l and "bvec" in l:
        fbvec=os.path.join(folder_sujeto,l)



#################

folder=os.path.dirname(path_input)
file_inMask=""
for i in os.listdir(folder):
    if "masked_mask" in i:
        file_inMask=os.path.join(folder,i)

#def to_estimate_dti(file_in, file_inMask, outPath, fbval, fbvec):
print(d.separador + 'building DTI Model...')

ref_name = utils.to_extract_filename(path_input)
file_evecs=os.path.join(path_output,ref_name + d.id_evecs + d.extension)
file_evals=os.path.join(path_output,ref_name + d.id_evals + d.extension)

if (not (os.path.exists(file_evecs))) | (
        not (os.path.exists(file_evals))):
    try:
        os.remove(file_evecs)
        os.remove(file_evals)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    img = nib.load(path_input)
    data = img.get_data()
    mask = nib.load(file_inMask)
    mask = mask.get_data()

    bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
    gtab = gradient_table(bvals, bvecs)

    tensor_model = dti.TensorModel(gtab)
    tensor_fitted = tensor_model.fit(data, mask)

    nib.save(nib.Nifti1Image(tensor_fitted.evecs.astype(np.float32), img.affine),
             file_evecs)
    nib.save(nib.Nifti1Image(tensor_fitted.evals.astype(np.float32), img.affine),
             file_evals)

print(file_evecs)
print(file_evals)
print(path_input)