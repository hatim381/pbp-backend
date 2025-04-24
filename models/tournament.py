from db import db
import json

class Tournament(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    pools = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_pools(self, pools_data):
        self.pools = json.dumps(pools_data)

    def get_pools(self):
        return json.loads(self.pools)

    def to_dict(self):
        return {
            "id": self.id,
            "pools": self.get_pools(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
