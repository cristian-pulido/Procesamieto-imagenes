import os
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


import nibabel as nib
import numpy as np
from tareas.dependencias import definitions as d
from tareas.dependencias import utils
from dipy.reconst.dti import color_fa, fractional_anisotropy, quantize_evecs
import dipy.reconst.dti as dti
from dipy.data import get_sphere
from dipy.tracking.eudx import EuDX
###################
folder=os.path.dirname(path_input)
file_tensor_fitevals=""
for i in os.listdir(folder):
    if "DTIEvals" in i:
        file_tensor_fitevals=os.path.join(folder,i)

file_tensor_fitevecs=""
for i in os.listdir(folder):
    if "DTIEvecs" in i:
        file_tensor_fitevecs=os.path.join(folder,i)

folder_sujeto=path_output
for l in os.listdir(folder_sujeto):
    if "TENSOR" in l and "bval" in l:
        fbval=os.path.join(folder_sujeto, l)
    if "TENSOR" in l and "bvec" in l:
        fbvec=os.path.join(folder_sujeto, l)


#################


if not os.path.exists(os.path.join(folder,"list_maps.txt")):


    # def to_estimate_dti_maps(path_dwi_input, path_output, file_tensor_fitevecs, file_tensor_fitevals):
    ref_name_only = utils.to_extract_filename(file_tensor_fitevecs)
    ref_name_only = ref_name_only[:-9]

    list_maps = []

    img_tensorFitevecs = nib.load(file_tensor_fitevecs)
    img_tensorFitevals = nib.load(file_tensor_fitevals)

    evecs = img_tensorFitevecs.get_data()
    evals = img_tensorFitevals.get_data()

    affine = img_tensorFitevecs.affine

    print(d.separador + d.separador + 'computing of FA map')
    FA = fractional_anisotropy(evals)
    FA[np.isnan(FA)] = 0
    nib.save(nib.Nifti1Image(FA.astype(np.float32), affine), os.path.join(path_output, ref_name_only + '_FA' + d.extension))

    list_maps.append(os.path.join(path_output,  ref_name_only + '_FA' + d.extension))

    print(d.separador + d.separador + 'computing of Color FA map')
    FA2 = np.clip(FA, 0, 1)
    RGB = color_fa(FA2, evecs)
    nib.save(nib.Nifti1Image(np.array(255 * RGB, 'uint8'), affine),
             os.path.join(path_output, ref_name_only + '_FA_RGB' + d.extension))

    print(d.separador + d.separador + 'computing of MD map')
    MD = dti.mean_diffusivity(evals)
    nib.save(nib.Nifti1Image(MD.astype(np.float32), affine), os.path.join(path_output,  ref_name_only + '_MD' + d.extension))

    list_maps.append(os.path.join(path_output, ref_name_only + '_MD' + d.extension))

    print(d.separador + d.separador + 'computing of AD map')
    AD = dti.axial_diffusivity(evals)
    nib.save(nib.Nifti1Image(AD.astype(np.float32), affine), os.path.join(path_output ,ref_name_only + '_AD' + d.extension))

    list_maps.append(os.path.join(path_output , ref_name_only + '_AD' + d.extension))

    print(d.separador + d.separador + 'computing of RD map')
    RD = dti.radial_diffusivity(evals)
    nib.save(nib.Nifti1Image(RD.astype(np.float32), affine), os.path.join(path_output, ref_name_only + '_RD' + d.extension))

    list_maps.append(os.path.join(path_output , ref_name_only + '_RD' + d.extension))

    sphere = get_sphere('symmetric724')
    peak_indices = quantize_evecs(evecs, sphere.vertices)

    eu = EuDX(FA.astype('f8'), peak_indices, seeds=300000, odf_vertices=sphere.vertices, a_low=0.15)
    tensor_streamlines = [streamline for streamline in eu]

    hdr = nib.trackvis.empty_header()
    hdr['voxel_size'] = nib.load(path_input).get_header().get_zooms()[:3]
    hdr['voxel_order'] = 'LAS'
    hdr['dim'] = FA.shape

    tensor_streamlines_trk = ((sl, None, None) for sl in tensor_streamlines)

    nib.trackvis.write(os.path.join(path_output, ref_name_only + '_tractography_EuDx.trk'), tensor_streamlines_trk, hdr,
                       points_space='voxel')

    print(list_maps)
    with open(os.path.join(path_output, "list_maps.txt"), "w") as f:
        for s in list_maps:
            f.write(str(s) + "\n")

print(path_input)