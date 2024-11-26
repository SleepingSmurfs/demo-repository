from flask import request, jsonify
from models import User, Window
from database import db





def setup_routes(app):
    @app.route('/windows', methods=['POST'])
    def create_window():
        data = request.json
        new_window = Window(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_window)
        db.session.commit()
        return jsonify({'message': 'Window created', 'id': new_window.id}), 201

    @app.route('/windows/<int:user_id>', methods=['GET'])
    def get_windows(user_id):
        windows = Window.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': w.id, 'title': w.title, 'content': w.content} for w in windows]), 200