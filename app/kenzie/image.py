from distutils import extension
import os
from traceback import print_tb
from unittest import result

from flask import safe_join

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


def get_list():
    _, dirs,_=next(os.walk("./imagens"))
    list = []
    for dir in dirs:
        *_, files_name = next(os.walk(f'{FILES_DIRECTORY}/{dir}'))
        list = list + files_name

    return list


def liste_by_extencion(extension):
    list = get_list()

    result = []

    for item in list:
        if item.split(".")[1] == extension:
            result.append(item) 
    
    if result == []:
        return "error"

    return(result)


def download_by_name(file:str):
    list = get_list()

    existence = False
    for item in list: 
        if item == file:
            existence = True

    if not existence:
        return "error"    

    name = file
    extencion = file.split(".")[1]

    print(extension)
    print(name)


    result = get_file_path(name, extencion)

    return result


def get_file_path(filename:str, extencion:str):

    abs_path = os.path.abspath(FILES_DIRECTORY+'/'+extencion)
    filepath = safe_join(abs_path, filename)

    return filepath

def upload_image(files):

    name = (files.filename)
    extencion = name.split('.')[1]

    is_extencion = checkin_extencion(extencion)
    if not is_extencion:
        return ("not extencion")

    if os.path.exists(f'{FILES_DIRECTORY}/{extencion}'):
        if os.path.isfile(f'{FILES_DIRECTORY}/{extencion}/{name}'):
            result = ("existe")
            return result

        filepath = get_file_path(name, extencion)

        files.save(filepath)
    else:
        os.mkdir(f'{FILES_DIRECTORY}/{extencion}')
        filepath = get_file_path(name, extencion)

        files.save(filepath)

    result = ("criado")
    return result

def checkin_extencion(extencion):
    extencions = ALLOWED_EXTENSIONS.split(",")

    is_estencion = False

    for item in extencions:
        if item == extencion:
            is_estencion = True
    
    return is_estencion

