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


@app.route('/pbi')
def get_pbi_by_country():
    country_arg = request.args.get('country')
    db_pbi = Pbi.objects(country=country_arg).first()
    if not db_pbi:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify({'valor': db_pbi.valor})


class Pbi(db.Document):
    country = db.StringField()
    valor = db.StringField()

    def to_json(self):
        return {"Country": self.country,
                "Valor": self.valor}


if __name__ == "__main__":
    app.run(debug=True, host='10.100.239.163', port=6200)
