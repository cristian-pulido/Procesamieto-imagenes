import os, shutil
import sys
import nibabel as nb
sys.path+=[os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"]

path_input = sys.argv[1]
path_output = sys.argv[2]


path_t1 = ""
path_func = ""
for i in os.listdir(path_output):
	if "T1" in os.path.join(path_output,i) :
		path_t1 = os.path.join(path_output,i)
	if "RESTING" in os.path.join(path_output,i) :
		path_func = os.path.join(path_output,i)

folder=os.path.join(path_output,"1")
os.mkdir(folder)
struc=os.path.join(path_output,"struc")
os.mkdir(struc)
folder_t1=os.path.join(struc,"1")
os.mkdir(folder_t1)        
  
shutil.copy(path_t1,os.path.join(folder_t1,"t1.nii.gz"))
path_t1 = os.path.join(folder_t1,"t1.nii.gz")
shutil.copy(path_func,os.path.join(folder,"fmri.nii.gz"))    
path_func = os.path.join(folder,"fmri.nii.gz")
        
os.system("gzip -d "+path_t1)
path_t1=os.path.splitext(path_t1)[0]
os.system("gzip -d "+path_func)
path_func=os.path.splitext(path_func)[0]




img=nb.load(path_func)

tr=img.header.get_zooms()[-1]

from tareas.fmri.run import run

run(path_output,tr)

for i in os.listdir(path_output):
    if i != "output":
        path=os.path.join(path_output,i)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
            
output=os.path.join(path_output,"output")
sub1=os.path.join(output,"datasink","preprocessing","sub-1")
out=os.path.join(path_output,"out")
shutil.copytree(sub1,out)
shutil.rmtree(output)

print(out)
