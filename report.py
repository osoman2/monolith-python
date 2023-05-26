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


@app.route('/report')
def get_report_by_country():
    country_arg = request.args.get('country')

    # PBI
    url_pbi = "http://10.100.239.163:6200/pbi?country={}".format(country_arg)
    response_pbi = urllib.request.urlopen(url_pbi)
    data_pbi = response_pbi.read()
    pbi = json.loads(data_pbi)["valor"]

    # President
    url_president = "http://10.100.239.163:6300/president?country={}".format(country_arg)
    response_president = urllib.request.urlopen(url_president)
    data_president = response_president.read()
    president = json.loads(data_president)["presidente"]

    # Holidays
    url_holidays = "http://10.100.239.163:6400/holiday?country={}".format(country_arg)
    response_holidays = urllib.request.urlopen(url_holidays)
    data_holidays = response_holidays.read()
    holidays = json.loads(data_holidays)

    report = Report(country_arg, pbi, president, holidays)
    return jsonify(report.to_json())


class Report:
    def __init__(self, country, pbi, presidente, feriados) -> None:
        self.country = country
        self.pbi = pbi
        self.presidente = presidente
        self.feriados = feriados

    def to_json(self):
        return {"Country": self.country,
                "PBI": self.pbi,
                "Presidente": self.presidente,
                "Feriados": self.feriados}


if __name__ == "__main__":
    app.run(debug=True, host='10.100.239.163', port=6500)
