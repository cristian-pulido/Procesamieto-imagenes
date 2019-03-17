import sys
import os,shutil

path_input = sys.argv[1]
path_output = sys.argv[2]


base =os.path.dirname(path_output)
temp =os.path.join(base ,"temp_first")

if os.path.exists(temp):
    shutil.rmtree(temp)
out = os.path.join(temp, os.path.basename(path_output))
os.system("run_first_all -i  " +path_input +" -o  " +out)

result =""
for archive in os.listdir(temp):
    if "firstseg" in archive:
        result =archive

shutil.move(os.path.join(temp ,result) ,os.path.join(base ,"first.nii.gz"))
shutil.rmtree(temp)

print(os.path.join(base ,result))

