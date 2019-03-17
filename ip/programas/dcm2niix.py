import os, shutil
import programas.definitions as defi

def convertir_dcm_2_nii(folder_dicom, folder_nii):
    ## ubicacion ejecutable dcm2niix
    print("Convirtiendo Dicom a Nifty ...")
    ejecutable = defi.path_dcm2niix
    options = '-b y -z y -f %f_%p -o'  # Json, zipped, name folder_process
    if len(os.listdir(folder_nii)) == 0:
        os.system(ejecutable + " " + options + " " + folder_nii + " " + folder_dicom)
    print("Finalizado")


def T1_path(folder):
    lista = os.listdir(folder)
    path = ""
    for l in lista:
        if "T1" in l and "3D" in l and os.path.splitext(l)[1] == ".gz":
            path = os.path.join(folder, l)
            break
    return path

def DWI_path(folder, b=True):
    lista = os.listdir(folder)
    path = []
    for l in lista:
        if "TENSOR" in l and os.path.splitext(l)[1] != ".json":
            path.append(os.path.join(folder, l))
    if b == True:
        return path
    else:
        img = ""
        for item in path:
            if os.path.splitext(item)[1] != ".bvec" and os.path.splitext(item)[1] != ".bval":
                img = item
        return img

def rest_path(folder):
    lista = os.listdir(folder)
    path = ""
    for l in lista:
        if "RESTING" in l and os.path.splitext(l)[1] == ".gz":
            path = os.path.join(folder, l)
            break
    return path