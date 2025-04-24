from flask import Blueprint, request, jsonify
from models.tournament import Tournament
from db import db

tournaments_bp = Blueprint('tournaments', __name__)

@tournaments_bp.route('/api/tournaments/<tournament_id>', methods=['GET'])
def get_tournament(tournament_id):
    try:
        tournament = Tournament.query.get(tournament_id)
        if tournament:
            return jsonify(tournament.to_dict()), 200
        return jsonify({'error': 'Tournament not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tournaments_bp.route('/api/tournaments', methods=['POST'])
def save_tournament():
    data = request.get_json()
    try:
        tournament = Tournament.query.get(data['id'])
        if tournament:
            tournament.set_pools(data['pools'])
        else:
            tournament = Tournament(id=data['id'])
            tournament.set_pools(data['pools'])
            db.session.add(tournament)
        
        db.session.commit()
        return jsonify(tournament.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
