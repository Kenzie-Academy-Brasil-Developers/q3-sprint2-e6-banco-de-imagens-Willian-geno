from http import HTTPStatus
from unittest import result
from flask import Flask, jsonify, request, send_file;
from werkzeug.exceptions import RequestHeaderFieldsTooLarge
import os

from app.kenzie.image import download_by_name, get_list,liste_by_extencion,upload_image

MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")

app = Flask(__name__);

app.config["MAX_CONTENT_LENGTH"] = int(MAX_CONTENT_LENGTH)

@app.errorhandler(413)
@app.errorhandler(RequestHeaderFieldsTooLarge)
def app_handle_413(e):
    return jsonify({"msg":"Arquivo maior que o permitido. Tamanho máximo:1MB"}), HTTPStatus.REQUEST_ENTITY_TOO_LARGE


@app.post("/upload")
def upload():
    result = ''

    files = request.files.values()

    for file in files:  
        result = upload_image(file)

    if result == "existe":
        return jsonify ({'msg':"Já exixte um arquivo com esse nome"}), HTTPStatus.CONFLICT
    
    if result == "not extencion":
        return jsonify({"msg":"Extenção não suportada"}), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    return jsonify({"msg":"Arquivo criado"}),HTTPStatus.CREATED


@app.get("/files/<extension>")
def list_files_by_extension(extension:str):
    result = liste_by_extencion(extension)

    if result == "error":
        return jsonify({"mag":"extenção não exixtente"}), 404 

    return jsonify(result),200

@app.get("/files")
def list_files():
    
    result = get_list()

    return jsonify(result),200


@app.get("/download-zip")
def download_dir_as_zip():
    ...


@app.get("/download/<file_name>")
def download(file_name:str):
    result = download_by_name(file_name)

    if result == "error":
        return jsonify("arquivo não exixtente"), 404 

    return send_file(result, as_attachment=True), 200
