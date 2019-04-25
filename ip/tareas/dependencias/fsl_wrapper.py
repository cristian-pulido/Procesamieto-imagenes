__author__ = 'Jrudascas'

import os


def flirt(file_in, file_out, ref, omat):
    command = 'flirt -in ' + file_in + ' -out ' + file_out + ' -ref ' + ref + ' -omat ' + omat + ' -dof 6'
    os.system(command)

    return file_out, omat


def flirt_xfm(file_in, file_out, ref, omat):
    command = 'flirt -in ' + file_in + ' -out ' + file_out + ' -ref ' + ref + ' -init ' + omat + ' -applyxfm'
    os.system(command)

    return file_out, omat


def bet(file_in, file_out, parameters):
    command = 'bet ' + file_in + ' ' + file_out + ' ' + parameters
    os.system(command)


def eddy_correct(file_in, file_out, referenceNo):
    command = 'eddy_correct ' + file_in + ' ' + file_out + ' ' + referenceNo
    os.system(command)


def hex_to_dec(file, file_out):
    command = 'sh /home/jrudascas/Desktop/DWITest/Additionals/Scripts/hexTodec ' + file + ' > ' + file_out
    os.system(command)