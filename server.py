"""
Простой сервер - обработчик

Запуск сервера:

gunicorn --bind 0.0.0.0:8080 --workers 4 server:app

Число воркеров нужно подбирать, стандартный рецепт: 2*num_cpu + 1
Т.е. если на сервере 4 cpu то нужно указать workers = 9

Пример запроса:

curl -XPOST -F 'image=@/home/skaledin/1.jpeg' -F 'json_parameters={"key": "value"}' localhost:8080/processImage

В случае успеха возвращается 200 код

В случае ошибки возвращается отличный от 200 код и описание ошибки.
Пишется лог в stdout


Установка:

* Требуется python3.6
* Выполнить: pip install -r requirements.py
* Запустить сервер

"""
import io
import json
import logging

import time
from PIL import Image
from flask import Flask, jsonify, Response
from flask import globals as g
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

# конфигурируем лог
logging.basicConfig(level="INFO")


def process_image_handler_impl(image: Image.Image, parameters=None):
    """
    :param image: Pillow Image объект
    :param parameters: словарь параметров из запроса
    """
    app.logger.info("Обрабатываю изображение %s с параметрами %s", image, parameters)

    # тут твой код который что то делает и возвращает dict с результатом
    pass


@app.route("/processImage", methods=["POST"])
def process_image_handler():
    start = time.time()

    try:
        image = g.request.files["image"]
        json_parameters = g.request.form["json_parameters"]
    except:
        app.logger.exception("Некорректный запрос: form=%s, files=%s",
                             g.request.form, g.request.files)
        return Response("Некорректный запрос. Требуется multipart запрос с изображением в поле image "
                        "и json строкой в поле json_parameters", status=400)

    try:
        json_parameters = json.loads(json_parameters)
    except:
        app.logger.exception("Не могу распарсить JSON")
        return Response("Не могу распарсить json параметры: {}".format(json_parameters), status=400)

    # я тут открываю картинку с помощью Pillow, можешь переписать
    # и открывать как тебе удобно
    try:
        assert isinstance(image, FileStorage)
        stream = io.BytesIO()
        image.save(stream)
        image = Image.open(stream)
    except:
        app.logger.exception("Не могу открыть переданное изображение %s. Проверьте формат",
                             image)
        return Response("Не могу открыть переданное изображение. Проверьте формат.", status=400)

    output = process_image_handler_impl(image, json_parameters)

    app.logger.info("Успешно обработано изображение за %s секунд", time.time() - start)

    return jsonify(output)

