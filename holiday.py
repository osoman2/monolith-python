import json
import urllib.request

from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'middleware',
    'host': '10.100.239.163',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


@app.route('/holiday')
def get_holiday_by_country():
    country_arg = request.args.get('country')
    url = "https://date.nager.at/api/v2/publicholidays/2023/{}".format(country_arg)
    response = urllib.request.urlopen(url)
    data = response.read()
    list_feriados = json.loads(data)
    feriados = []
    for valores in list_feriados:
        feriados.append(Holiday(valores["date"], valores["localName"]).__dict__)
    return jsonify(feriados)


class Holiday:
    def __init__(self, fecha, nombre):
        self.fecha = fecha
        self.nombre = nombre

    def to_json(self):
        return {"Fecha": self.fecha,
                "Nombre": self.nombre}


if __name__ == "__main__":
    app.run(debug=True, host='10.100.239.163', port=6400)
