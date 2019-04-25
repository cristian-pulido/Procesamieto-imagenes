import os
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


import nibabel as nib
from dipy.core.gradients import gradient_table
from dipy.io.trackvis import save_trk
###################
folder=os.path.dirname(path_input)
file_inMask=""
for i in os.listdir(folder):
    if "masked_mask" in i:
        file_inMask=os.path.join(folder,i)
    if "Reslice.nii.gz" in i:
    	os.remove(os.path.join(folder,i))



folder_sujeto=path_output
for l in os.listdir(folder_sujeto):
    if "TENSOR" in l and "bval" in l:
        fbval=os.path.join(folder_sujeto, l)
    if "TENSOR" in l and "bvec" in l:
        fbvec=os.path.join(folder_sujeto, l)


#################





# def to_generate_tractography(path_dwi_input, path_binary_mask, path_out, path_bval, path_bvec):
from dipy.reconst.shm import CsaOdfModel
from dipy.data import default_sphere
from dipy.direction import peaks_from_model
from dipy.tracking.local import LocalTracking
from dipy.tracking import utils
from dipy.tracking.local import ThresholdTissueClassifier

print('    - Starting reconstruction of Tractography...')

if not os.path.exists(os.path.join(path_output , '_tractography_CsaOdf' + '.trk')):
    dwi_img = nib.load(path_input)
    dwi_data = dwi_img.get_data()
    dwi_affine = dwi_img.affine

    dwi_mask_data = nib.load(file_inMask).get_data()

    g_tab = gradient_table(fbval, fbvec)

    csa_model = CsaOdfModel(g_tab, sh_order=6)

    csa_peaks = peaks_from_model(csa_model, dwi_data, default_sphere, sh_order=6,
                                 relative_peak_threshold=.85,
                                 min_separation_angle=35, mask=dwi_mask_data.astype(bool))

    classifier = ThresholdTissueClassifier(csa_peaks.gfa, .2)

    seeds = utils.seeds_from_mask(dwi_mask_data.astype(bool), density=[1, 1, 1], affine=dwi_affine)

    streamlines = LocalTracking(csa_peaks, classifier, seeds, dwi_affine, step_size=3)

    streamlines = [s for s in streamlines if s.shape[0] > 30]

    streamlines = list(streamlines)

    save_trk(os.path.join(path_output , '_tractography_CsaOdf' + '.trk'), streamlines, dwi_affine, dwi_mask_data.shape)

print('    - Ending reconstruction of Tractography...')
print(path_input)