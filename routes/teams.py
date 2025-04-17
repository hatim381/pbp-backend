from flask import Blueprint, request, jsonify
from models.team import Team
from db import db

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        all_teams = Team.query.all()
        return jsonify([team.to_dict() for team in all_teams]), 200
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération', 'details': str(e)}), 500

@teams_bp.route('/api/teams', methods=['POST'])
def add_team():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('members'):
        return jsonify({'error': 'Les champs "name" et "members" sont obligatoires'}), 400

    new_team = Team(
        name=data['name'],
        members=data['members'],
        email=data.get('email', ''),
        phone=data.get('phone', '')
    )

    try:
        db.session.add(new_team)
        db.session.commit()
        return jsonify(new_team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de l'ajout", "details": str(e)}), 500

@teams_bp.route('/api/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Équipe non trouvée'}), 404

    try:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Équipe supprimée'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la suppression', 'details': str(e)}), 500

@teams_bp.route('/api/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Équipe non trouvée'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Aucune donnée reçue'}), 400

    try:
        team.name = data.get('name', team.name)
        team.members = data.get('members', team.members)
        team.email = data.get('email', team.email)
        team.phone = data.get('phone', team.phone)
        db.session.commit()
        return jsonify(team.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour', 'details': str(e)}), 500
