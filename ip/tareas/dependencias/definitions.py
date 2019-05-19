__author__ = 'Jrudascas'

import os
from django.conf import settings
base=settings.BASE_DIR
atlas_path=os.path.join(os.path.dirname(base),"Atlas")

atlas = os.path.join(atlas_path,'1mm/AAN_1mm.nii')
aan_atlas = os.path.join(atlas_path,'1mm/AAN.nii')
morel_atlas = os.path.join(atlas_path,'1mm/ThalamicNucleiMorelAtlas.nii')
harvard_oxford_cort_atlas = os.path.join(atlas_path,'1mm/HarvardOxfordCort.nii')
hypothalamus_atlas = os.path.join(atlas_path,'1mm/Hypothalamus.nii')
tpm=os.path.join(atlas_path,'TPM.nii')

standard_t2 = os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T1_1mm_brain.nii.gz')
standard_t1 = os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T1_1mm_brain.nii.gz')
brain_mask_nmi = os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T1_1mm_brain_mask.nii.gz')

default_b0_ref = 0
extension = '.nii.gz'
pre_diffusion_images = 'diffus/'
pre_functional_images = 'func/'
pre_anatomica_images = 'anat/'

id_eddy_correct = '_EddyCorrect'
id_reslice = '_Reslice'
id_non_local_mean = '_NonLocalMean'
id_median_otsu = '_MedianOtsu'
id_bet = '_BET'
id_evecs = '_DTIEvecs'
id_evals = '_DTIEvals'
separador = '    - '
vox_sz = 1.0
threshold = 100
median_radius = 4
num_pass = 4
