import os, shutil
import nibabel as nib
from numpy import prod
import numpy as np

def np2str(a):
    line = "["
    for e in a:
        line += " " + str(e) + ","
    line = line[:-1] + "]"
    return line

def grafics_plot(arrays, direccion, legends, Title, labelaxes, myDiv):
    file = direccion
    f = open(file, "w+")
    traces = []
    for i in range(len(arrays)):
        traces.append("traces" + str(i))
        f.write("var " + traces[i] + " = { \n")
        f.write("y: " + np2str(arrays[i]) + ",\n")
        f.write("name: '" + legends[i] + "', \n")
        f.write("type: 'scatter' \n };\n")
    f.write("var data = " + np2str(traces) + ";\n")
    f.write("var layout = { \n title: '" + Title + "',\n 'titlefont': { \n 'size': 36, \n }, \n xaxis: { \n title: '" +
            labelaxes[0] + "', \n  titlefont: { \n")
    f.write("family: 'Courier New, monospace', \n size: 18, \n color: '#7f7f7f' \n   } \n  }, \n ")
    f.write(" yaxis: { \n  title: '" + labelaxes[
        1] + "', \n  titlefont: { \n  family: 'Courier New, monospace', \n size: 18, \n color: '#7f7f7f' \n } \n } \n }; \n")
    f.write("Plotly.newPlot('" + myDiv + "', data, layout);")

    f.close()


def func_motion_correct(dir_func, dir_result, img_name, tipoimg):
    if os.path.exists(dir_result):
        shutil.rmtree(dir_result)
    os.mkdir(dir_result)
    folder_temp=os.path.join(dir_result,"folder_temp")
    os.mkdir(folder_temp)
    img_out=os.path.join(folder_temp,"out")
    os.system("mcflirt -in "+dir_func+" -out "+img_out+" -plots -rmsabs -rmsrel")
    shutil.copy(img_out+".nii.gz", os.path.join(dir_result, os.path.basename(dir_func)))
    abs_mean_file = os.path.join(folder_temp,"out_abs_mean.rms")
    file = open(abs_mean_file, "r")
    absolute = float(file.read()[:4])
    file.close()
    relative_mean_file = os.path.join(folder_temp,"out_rel_mean.rms")
    file = open(relative_mean_file, "r")
    relative = float(file.read()[:4])
    file.close()
    abs_values_file = os.path.join(folder_temp,"out_abs.rms")
    abs_values = []
    with open(abs_values_file) as f:
        for line in f:
            abs_values.append(float(line))
    relative_values_file = os.path.join(folder_temp,"out_rel.rms")
    relative_values = []
    with open(relative_values_file) as f:
        for line in f:
            relative_values.append(float(line))
    paths_html = {}
    paths_html["desplazamiento"] = dir_result + "/desplazamiento.js"
    grafics_plot([abs_values, relative_values],
                 paths_html["desplazamiento"],
                 ["Absoluto", "Relativo"],
                 "Desplazamiento Medio Imagen " + img_name,
                 ["Tiempo (volumenes)", "Distancia (mm)"],
                 "div_"+tipoimg+"_desplazamiento")

    rot_n_tra_path =  os.path.join(folder_temp,"out.par")
    rot_n_tra = np.loadtxt(rot_n_tra_path)
    rot = rot_n_tra[:, :3]
    tra = rot_n_tra[:, 3:]
    paths_html["rotaciones"] = dir_result + "/rotacion.js"
    grafics_plot(arrays=[rot[:, 0], rot[:, 1], rot[:, 2]],
                 direccion=paths_html["rotaciones"],
                 legends=["x", "y", "z"],
                 Title="Rotaciones",
                 labelaxes=["Tiempo (Volumenes)", "Radianes"],
                 myDiv="div_" + tipoimg + "_rotaciones")
    paths_html["traslaciones"] = dir_result + "/traslacion.js"
    grafics_plot(arrays=[tra[:, 0], tra[:, 1], tra[:, 2]],
                 direccion=paths_html["traslaciones"],
                 legends=["x", "y", "z"],
                 Title="Traslaciones",
                 labelaxes=["Tiempo (Volumenes)", "mm"],
                 myDiv="div_" + tipoimg + "_traslaciones")

    shutil.rmtree(folder_temp)
    for path in paths_html:
        ind = paths_html[path].index("/media")
        paths_html[path]=paths_html[path][ind:]


    return absolute, relative, paths_html