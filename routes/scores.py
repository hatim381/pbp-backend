from flask import Blueprint, request, jsonify
from models.score import Score
from db import db

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('/api/scores/<tournament_id>', methods=['GET'])
def get_tournament_scores(tournament_id):
    try:
        scores = Score.query.filter_by(tournament_id=tournament_id).all()
        return jsonify([score.to_dict() for score in scores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/api/scores', methods=['POST'])
def save_tournament_scores():
    try:
        data = request.get_json()
        tournament_id = data.get('tournamentId')
        scores = data.get('scores', {})

        # Supprimer les anciens scores
        Score.query.filter_by(tournament_id=tournament_id).delete()

        # Ajouter les nouveaux scores
        for score_key, score_data in scores.items():
            pool_name, match_key = score_key.split('-')
            new_score = Score(
                tournament_id=tournament_id,
                pool_name=pool_name,
                match_key=match_key,
                score1=score_data.get('score1'),
                score2=score_data.get('score2')
            )
            db.session.add(new_score)

        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
