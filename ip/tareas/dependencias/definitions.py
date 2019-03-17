__author__ = 'Jrudascas'

import os


atlas = '/home/runlab/data/Atlas/1mm/AAN_1mm.nii'
aan_atlas = '/home/runlab/data/Atlas/1mm/AAN.nii'
morel_atlas = '/home/runlab/data/Atlas/1mm/ThalamicNucleiMorelAtlas.nii'
harvard_oxford_cort_atlas = '/home/runlab/data/Atlas/1mm/HarvardOxfordCort.nii'
hypothalamus_atlas = '/home/runlab/data/Atlas/1mm/Hypothalamus.nii'

standard_t2 = os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T2_1mm_brain.nii.gz')
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
