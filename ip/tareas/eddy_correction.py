
import sys
import os

sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]
from tareas.dependencias import utils
from tareas.dependencias import definitions as d
from tareas.dependencias import fsl_wrapper as fsl
import shutil

path_input = sys.argv[1]
path_output = sys.argv[2]

"""
Prueba documental.
In:
file_in: akakakakka
outPath: kakakasjdjdlllf kklkd
ref_bo. kskskdejien skkd  dllkd
Out:
"""
ref_bo = '0'
print('    - running Eddy Correction...')


refNameOnly = utils.to_extract_filename(path_input)
final_name=os.path.join(path_output,refNameOnly + d.id_eddy_correct + d.extension)

if not os.path.exists(final_name):
    refName = utils.to_extract_filename_extention(path_input)
    path_temporal=os.path.join(path_output,"temp_eddy")
    os.mkdir(path_temporal)
    os.system('cp ' + path_input + ' ' + path_temporal)  # Copiamos archivo de difusion a la carpeta temporal
    fsl.eddy_correct(path_temporal +"/"+ refName, path_temporal +"/"+ refNameOnly + d.id_eddy_correct + '.nii', ref_bo)
    os.system('cp ' + os.path.join(path_temporal, refNameOnly + d.id_eddy_correct + d.extension) + ' ' + path_output)  # Copiamos archivo de difusion desde carpeta temporal
    shutil.rmtree(path_temporal)
print(final_name)