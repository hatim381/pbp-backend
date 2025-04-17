from flask import Flask
from flask_cors import CORS  # Ajout pour le CORS
from db import db
from routes.teams import teams_bp
import os

app = Flask(__name__)
CORS(app)  # Active les requêtes cross-origin (ex: React -> Flask)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'teams.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crée le dossier 'instance' s'il n'existe pas (pour SQLite)
os.makedirs("instance", exist_ok=True)

db.init_app(app)

with app.app_context():
    from models.team import Team
    db.create_all()

app.register_blueprint(teams_bp)

if __name__ == '__main__':
    app.run(debug=True)
