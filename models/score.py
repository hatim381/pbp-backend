from db import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_name = db.Column(db.String(50), nullable=False)
    match_key = db.Column(db.String(50), nullable=False)
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)
    tournament_id = db.Column(db.String(50), nullable=False)  # Pour identifier les scores d'un même tournoi

    def to_dict(self):
        return {
            "id": self.id,
            "pool_name": self.pool_name,
            "match_key": self.match_key,
            "score1": self.score1,
            "score2": self.score2,
            "tournament_id": self.tournament_id
        }
