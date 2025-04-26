from flask import Blueprint, request, jsonify
from models.pool import Pool
from db import db

pools_bp = Blueprint('pools', __name__)

@pools_bp.route('/api/pools/<tournament_id>', methods=['GET'])
def get_pools(tournament_id):
    try:
        pool = Pool.query.filter_by(tournament_id=tournament_id).first()
        if pool:
            return jsonify(pool.to_dict()), 200
        return jsonify({'pools': []}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pools_bp.route('/api/pools', methods=['POST'])
def save_pools():
    try:
        data = request.get_json()
        tournament_id = data.get('tournament_id')
        pools_data = data.get('pools', [])

        pool = Pool.query.filter_by(tournament_id=tournament_id).first()
        if pool:
            pool.set_data(pools_data)
        else:
            pool = Pool(tournament_id=tournament_id)
            pool.set_data(pools_data)
            db.session.add(pool)

        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
