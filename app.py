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

if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()

with app.app_context():
    from models.team import Team
    db.create_all()

app.register_blueprint(teams_bp)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
