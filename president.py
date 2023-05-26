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


@app.route('/president')
def get_president_by_country():
    country_arg = request.args.get('country')
    db_presidente = President.objects(country=country_arg).first()
    if not db_presidente:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify({'presidente': db_presidente.presidente})


class President(db.Document):
    country = db.StringField()
    presidente = db.StringField()

    def to_json(self):
        return {"Country": self.country,
                "Presidente": self.presidente}


if __name__ == "__main__":
    app.run(debug=True, host='10.100.239.163', port=6300)
