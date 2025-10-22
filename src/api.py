from flask import Flask, request, jsonify
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_handler import DatabaseHandler
from src.utils.matchmaker import Matchmaker
from src.models.user import User

app = Flask(__name__, static_folder='../static', static_url_path='/static')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

db_path = os.environ.get('DATABASE_PATH', 'peer_exchange.db')
db = DatabaseHandler(db_path)
db.initialize_database()
matchmaker = Matchmaker(db)

@app.route('/')
def home():
    with open(os.path.join(static_dir, 'index.html')) as f:
        return f.read()

@app.route('/api/users', methods=['GET'])
def get_users():
    users = db.get_all_users()
    result = []
    for u in users:
        result.append(u.to_dict())
    return jsonify(result)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    if not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            skills_offered=data.get('skills_offered', []),
            skills_needed=data.get('skills_needed', [])
        )
        user_id = db.add_user(new_user)
        new_user.user_id = user_id
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>/matches', methods=['GET'])
def get_matches(user_id):
    user = db.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    matches = matchmaker.find_matches(user_id)
    match_list = []
    
    for match_id, score in matches:
        match_user = db.get_user(match_id)
        match_details = matchmaker.get_match_details(user_id, match_id)
        
        match_list.append({
            'user': match_user.to_dict(),
            'score': score,
            'can_learn': match_details['user1_can_learn'],
            'can_teach': match_details['user2_can_learn'],
            'mutual': match_details['is_mutual_exchange']
        })
    
    return jsonify(match_list)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

