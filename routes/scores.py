from flask import Blueprint, request, jsonify
from models.score import Score
from db import db

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('/api/scores/<tournament_id>', methods=['GET'])
def get_scores(tournament_id):
    try:
        scores = Score.query.filter_by(tournament_id=tournament_id).all()
        return jsonify([score.to_dict() for score in scores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/api/scores', methods=['POST'])
def save_score():
    data = request.get_json()
    
    # Vérifier si le score existe déjà
    existing_score = Score.query.filter_by(
        tournament_id=data['tournament_id'],
        pool_name=data['pool_name'],
        match_key=data['match_key']
    ).first()

    try:
        if existing_score:
            # Mettre à jour le score existant
            existing_score.score1 = data['score1']
            existing_score.score2 = data['score2']
        else:
            # Créer un nouveau score
            new_score = Score(
                tournament_id=data['tournament_id'],
                pool_name=data['pool_name'],
                match_key=data['match_key'],
                score1=data['score1'],
                score2=data['score2']
            )
            db.session.add(new_score)

        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
