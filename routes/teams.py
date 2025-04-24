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
    if not data or not data.get('members'):
        return jsonify({'error': 'Le champ "members" est obligatoire'}), 400

    new_team = Team(
        name=data.get('name', data['members']),  # Utilise 'name' si fourni, sinon 'members'
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
        # met à jour uniquement ce qui est fourni
        team.members = data.get('members', team.members)
        team.name = data.get('members', team.name)  # optionnel : suivre members
        team.email = data.get('email', team.email)
        team.phone = data.get('phone', team.phone)
        db.session.commit()
        return jsonify(team.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour', 'details': str(e)}), 500

@teams_bp.route('/api/teams/generate-pools', methods=['POST'])
def generate_pools():
    data = request.get_json()
    if not data or not isinstance(data.get('teams'), list):
        return jsonify({'error': 'Une liste d\'équipes est requise'}), 400

    teams = data['teams']
    shuffled = teams[:]  # Copie de la liste des équipes
    result = []
    waiting_list = []

    # Répartir les équipes en poules de 4 tant que possible
    while len(shuffled) >= 4:
        result.append(shuffled[:4])
        shuffled = shuffled[4:]

    # Répartir les équipes en poules de 3 si possible
    while len(shuffled) >= 3:
        result.append(shuffled[:3])
        shuffled = shuffled[3:]

    # Si une équipe reste seule, elle est mise en liste d'attente
    if len(shuffled) == 1:
        waiting_list.append(shuffled[0])

    return jsonify({
        'pools': result,
        'waiting_list': waiting_list
    }), 200
