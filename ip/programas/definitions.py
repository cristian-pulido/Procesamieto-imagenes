import os
from django.conf import settings

base=settings.BASE_DIR
results=os.path.join(settings.MEDIA_ROOT,"results")


path_dcm2niix = os.path.join(os.path.dirname(base),"dcm2niix/dcm2niix")
templete_T1=os.path.join(os.environ['FSLDIR'], 'data/standard/MNI152_T1_2mm.nii.gz')
