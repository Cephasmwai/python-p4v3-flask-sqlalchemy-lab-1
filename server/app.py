from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return make_response({'message': 'Flask SQLAlchemy Lab 1'}, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return make_response(earthquake.to_dict(), 200)
    else:
        return make_response({'message': f"Earthquake {id} not found."}, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [quake.to_dict() for quake in earthquakes]

    return make_response({
        "count": len(quakes_list),
        "quakes": quakes_list
    }, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
