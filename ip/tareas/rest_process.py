import os, shutil
import sys
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


path_t1 = ""
path_func = ""
for i in os.listdir(path_output):
	if "T1" in os.path.join(path_output,i) :
		path_t1 = os.path.join(path_output,i)
	else:
		path_func = os.path.join(path_output,i)

os.system("gzip -d "+path_t1)
path_t1=os.path.splitext(path_t1)[0]
os.system("gzip -d "+path_func)
path_func=os.path.splitext(path_func)[0]

folder=os.path.join(path_output,"1")
os.mkdir(folder)
struc=os.path.join(path_output,"struc")
os.mkdir(struc)
folder_t1=os.path.join(struc,"1")
os.mkdir(folder_t1)
shutil.copy(path_t1,os.path.join(folder_t1,"t1.nii"))
shutil.copy(path_func,os.path.join(folder,"fmri.nii"))



from tareas.fmri.run import run

run(path_output)

print(path_input)
