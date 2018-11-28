# Простой сервер - обработчик

## Установка:
* Требуется python3.6
* Выполнить: `pip install -r requirements.py`
* Запустить сервер

## Запуск сервера:
```
gunicorn --bind 0.0.0.0:8080 --workers 4 server:app
```

Число воркеров (--workers) нужно подбирать, стандартный рецепт: `2*num_cpu + 1`

Т.е. если на сервере 4 cpu то нужно указать workers = 9

Пример запроса:
```
curl -XPOST -F 'image=@/home/skaledin/1.jpeg' -F 'json_parameters={"key": "value"}' localhost:8080/processImage
```

В случае успеха возвращается 200 код
В случае ошибки возвращается отличный от 200 код и описание ошибки.
Пишется лог в stdout
