from db import db
from datetime import datetime

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(100), nullable=False)
    pool_name = db.Column(db.String(50), nullable=False)
    match_key = db.Column(db.String(50), nullable=False)
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'pool_name': self.pool_name,
            'match_key': self.match_key,
            'score1': self.score1,
            'score2': self.score2
        }
