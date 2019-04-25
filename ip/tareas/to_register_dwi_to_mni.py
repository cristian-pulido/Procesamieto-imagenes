import os
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]

from tareas.dependencias import definitions as d
from tareas.dependencias import utils
from tareas.dependencias import tools

import nibabel as nib
import numpy as np
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table

###################
folder_sujeto=path_output
for l in os.listdir(folder_sujeto):
    if "TENSOR" in l and "bval" in l:
        fbval=os.path.join(folder_sujeto, l)
    if "TENSOR" in l and "bvec" in l:
        fbvec=os.path.join(folder_sujeto, l)

#################

# def to_register_dwi_to_mni(path_in, path_out, path_bvec, path_bval):
ref_name = utils.to_extract_filename(path_input)

finalname=os.path.join(path_output,ref_name + '_normalized' + d.extension)

if not os.path.exists(finalname ):

    img_DWI = nib.load(path_input)
    data_DWI = img_DWI.get_data()
    affine_DWI = img_DWI.affine

    bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
    gtab = gradient_table(bvals, bvecs)

    b0 = data_DWI[..., gtab.b0s_mask]

    mean_b0 = np.mean(b0, -1)

    mni_t2 = nib.load(d.standard_t2)
    mni_t2_data = mni_t2.get_data()
    MNI_T2_affine = mni_t2.affine

    directionWarped = np.zeros(
        (mni_t2_data.shape[0], mni_t2_data.shape[1], mni_t2_data.shape[2], data_DWI.shape[-1]),dtype=np.float32)
    rangos = range(data_DWI.shape[-1])

    affine, starting_affine = tools.affine_registration(mean_b0, mni_t2_data, moving_grid2world=affine_DWI,
                                                        static_grid2world=MNI_T2_affine)

    warped_moving, mapping = tools.syn_registration(mean_b0, mni_t2_data,
                                                    moving_grid2world=affine_DWI,
                                                    static_grid2world=MNI_T2_affine,
                                                    # step_length=0.1,
                                                    # sigma_diff=2.0,
                                                    metric='CC',
                                                    dim=3, level_iters=[10, 10, 5],
                                                    # prealign=affine.affine)
                                                    prealign=starting_affine)

    for gradientDirection in rangos:
        # print(gradientDirection)
        directionWarped[:, :, :, gradientDirection] = mapping.transform(
            data_DWI[:, :, :, gradientDirection].astype(int), interpolation='nearest')

    nib.save(nib.Nifti1Image(directionWarped, MNI_T2_affine), finalname)

    affine = nib.load(finalname).affine

    list_path_atlas_1 = utils.registration_atlas_to(d.aan_atlas, path_output, affine, mapping)
    with open(os.path.join(path_output,"list_path_atlas_1.txt"), "w") as f:
        for s in list_path_atlas_1:
            f.write(str(s) +"\n")
    list_path_atlas_2 = utils.registration_atlas_to(d.morel_atlas, path_output, affine, mapping)
    with open(os.path.join(path_output,"list_path_atlas_2.txt"), "w") as f:
        for s in list_path_atlas_2:
            f.write(str(s) +"\n")
    list_path_atlas_3 = utils.registration_atlas_to(d.hypothalamus_atlas, path_output, affine, mapping)
    with open(os.path.join(path_output,"list_path_atlas_3.txt"), "w") as f:
        for s in list_path_atlas_3:
            f.write(str(s) +"\n")
    list_path_atlas_4 = utils.registration_atlas_to(d.harvard_oxford_cort_atlas, path_output, affine, mapping)
    with open(os.path.join(path_output,"list_path_atlas_4.txt"), "w") as f:
        for s in list_path_atlas_4:
            f.write(str(s) +"\n")


print(finalname)
print(path_input)


