from db import db
import json

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(100), nullable=False)
    pool_data = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_data(self, data):
        self.pool_data = json.dumps(data)

    def get_data(self):
        return json.loads(self.pool_data)

    def to_dict(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'pools': self.get_data()
        }
