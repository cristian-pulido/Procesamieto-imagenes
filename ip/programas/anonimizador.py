import os
import os.path
import patoolib
import nibabel as nib
import pydicom
import math
from pydicom.errors import InvalidDicomError
from nibabel.loadsave import ImageFileError


def walking(folder, applied_function):
    """
    Walks through folder doing an specified function in the second parameter
    :type applied_function: function
    :param folder: the folder to execute the walking
    :param applied_function: specified function to do on the walking
    :return: walking applying the function
    Example walking('/Users/jscs/Downloads/test', print)
    """
    for (root, dirs, files) in os.walk(folder):
        for (file) in files:
            applied_function(os.path.join(root, file))


def recursive_walking(folder):
    if os.path.isfile(folder):
        if dicom_reader(folder):
            dicom_file_anonymizer(folder)
    else:
        for (root, dirs, files) in os.walk(folder):
            for dir in dirs:
                recursive_walking(os.path.join(root, dir))
            for file in files:
                if dicom_reader(os.path.join(root, file)):
                    #print(os.path.join(root, file))
                    dicom_file_anonymizer(os.path.join(root, file))
    return


def read_unpack(file_path):
    """
    Detect and unpack compressed files
    :param file_path: file to unpack
    :return: Message of unpacked in the parent directory or no file detected
    """
    ends = ['.rar', '.7z', '.dmg', '.gz', '.iso', '.tar', '.zip', '.bz2', '.xz', '.wim', '.swm', '.esd', '.cb7', '.cbr',
            '.jar', '.cbz', '.rz', '.z', '.arc', '.ace', '.dmg', '.lz', '.lzma', '.lz', '.lrz', '.iso', '.dms', '.a']
    output_folder = os.path.abspath(os.path.join(file_path, os.pardir))
    if any(file_path.lower().endswith(end) for end in ends):
        try:
            nib.load(file_path)
        except ImageFileError:
            if patoolib.extract_archive(file_path, outdir=output_folder):
                return #print(file_path, "successfully unpacked")
            else:
                raise ValueError('File extension is not supported for your program', file_path)
    else:
        pass


def read_delete(file_path):
    """
    Detect and remove packed files
    :param file_path: file to remove
    :return: Message of deleted packed file, nifti-dicom recognition, or no file detected
    """
    ends = ['.rar', '.7z', '.dmg', '.gz', '.iso', '.tar', '.zip', '.bz2', '.xz', '.wim', '.swm', '.esd', '.cb7', '.cbr',
            '.jar', '.cbz', '.rz', '.z', '.arc', '.ace', '.dmg', '.lz', '.lzma', '.lz', '.lrz', '.iso', '.dms', '.a']
    if any(file_path.lower().endswith(end) for end in ends):
        try:
            nib.load(file_path)
        except ImageFileError:
            try:
                pydicom.dcmread(file_path)
            except InvalidDicomError:
                os.remove(file_path)
                return print('Packed file removed: ', file_path)
            else:
                return #print('Dicom file does not removed: ', file_path)
        else:
            return #print('Nifti file does not removed: ', file_path)
    else:
        pass


def dicom_reader(file_path):
    try:
        pydicom.dcmread(file_path)
    except InvalidDicomError:
        return False
    else:
        return True


def dicom_file_anonymizer(path):
    """Args:
           path(str): The path of the DICOM file
        Returns:
            DICOM file saved without personal information"""

    if dicom_reader(path):
        data_set = pydicom.dcmread(path)
        #print('---> Reading to anonymize: ', path)

        data_elements = ['PatientName', 'PatientID', 'IssuerOfPatientID', 'TypeOfPatientID',
                         'PatientBirthDate', 'PatientBirthTime', 'PatientBirthDateInAlternative',
                         'PatientDeathDateInAlternative', 'PatientDeathDateInAlternative',
                         'PatientSex', 'PatientInsurancePlanCode', 'OtherPatientIDs', 'PatientAge',
                         'PatientSize', 'PatientWeight', 'PatientAddress', 'InsurancePlanIdentification',
                         'MilitaryRank', 'BranchOfService', 'PatientTelephoneNumbers',
                         'AdditionalPatientHistory']

        """
        You can add or remove elements to delete  based on 'keywords' of 
        http://dicom.nema.org/medical/dicom/current/output/pdf/part06.pdf
        (personal information (0010,xxxx) pag. 29-31) 
        """

        for element in data_elements:
            if element in data_set:
                delattr(data_set, element)
                #print('Deleting', element, 'from', path)
            else:
                pass
                #print(element, 'not in', path)
        #print('---> Finished anonymization in ', path)
        return data_set.save_as(path)
    else:
        pass


def dicom_anonymizer(path):
    if os.path.isfile(path):
        if dicom_reader(path):
            print('--> Anonymizing file')
            dicom_file_anonymizer(path)
            return '--> Successful file anonymization'
    else:
        print('--> Searching compressed files and unpacking')
        walking(path, read_unpack)
        print('--> Searching compressed files unpacked and deleting')
        walking(path, read_delete)
        print('--> Searching dicom files and anonymizing')
        walking(path, dicom_file_anonymizer)
        return '--> Successful directory anonymization'


"""
Example:
    >>> directory_path_test = '/Users/jscs/Downloads/test'
    >>> dicom_anonymizer(directory_path_test)
"""


def get_tags_dicom(dicom_dir):
    lista = []
    for path, dirs, files in os.walk(dicom_dir):
        for name in files:
            file_path = os.path.join(path, name)
            if dicom_reader(file_path):
                lista.append(file_path)
    series={}
    for dcm in lista:
        file=pydicom.read_file(dcm)
        if file.SeriesDescription in series:
            for f in file:
                if len(str(f.value)) < 150 and f.keyword != "SeriesDescription":
                    if f.name in series[file.SeriesDescription] :
                        if series[file.SeriesDescription][str(f.name)] != [] and str(f.value) != series[file.SeriesDescription][str(f.name)]["v_tag"]:
                            series[file.SeriesDescription][str(f.name)]=[]
                    else:
                        series[file.SeriesDescription][str(f.name)]={"num_tag":str(f.tag),"name_tag":str(f.keyword),"v_tag":str(f.value) }


        else:
            series[file.SeriesDescription]={}
            for f in file:
                if len(str(f.value)) < 150 and f.keyword != "SeriesDescription":
                    series[file.SeriesDescription][str(f.name)]={"num_tag":str(f.tag),"name_tag":str(f.keyword),"v_tag":str(f.value) }


    for s in series:
        eliminacion=[]
        for tag in series[s]:
            if series[s][tag] == []:
                eliminacion.append(tag)
        for element in eliminacion:
                series[s].pop(element)
    return series

