from flask import Blueprint, g, request, jsonify
from app.db import get_db
from app.middleware import token_required
from app.util import check_winner

bp = Blueprint('game', __name__, url_prefix='/game')

def initialize_board():
    return [" "] * 9

@bp.route('', methods=['POST'])
@token_required
def create_game(current_user):
    db = get_db()

    board = ''.join(initialize_board())
    cursor = db.execute(
        "INSERT INTO games (user_id, board) VALUES (?, ?)",
        (current_user["id"], board))
    db.commit()

    return jsonify({
        'game_id': cursor.lastrowid
    }), 200

@bp.route('/move', methods=['POST'])
@token_required
def add_move(current_user):
    data = request.get_json()
    game_id = data.get('game_id')
    move = data.get('move')

    if not game_id or move is None:
        return jsonify({'message': 'Game ID, and move are required'}), 400

    db = get_db()

    game = db.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()

    if not game:
        return jsonify({'message': 'Invalid game ID'}), 400

    board = list(game[2])
    current_turn = game[3]
    winner = game[4]
    next_turn = current_turn + 1
    current_turn_is_user = (current_turn % 2) == 1

    if winner:
        return jsonify({'message': 'Game already has a winner', 'board': ''.join(board), 'winner': winner}), 400

    if board[move] != " ":
        return jsonify({'message': 'Invalid move'}), 400

    # Update board to store later
    board[move] = 'X' if current_turn_is_user else 'O'

    winner = check_winner(board)

    # Update win count for user if they won
    if winner and winner != "Draw" and current_turn_is_user:
        db.execute("UPDATE users SET wins = wins + 1 WHERE id = ?", (current_user["id"],))

    update_query = "UPDATE games SET board = ?, current_turn = ?, winner = ? WHERE id = ?"
    db.execute(update_query, (''.join(board), next_turn, winner, game_id))
    db.commit()

    return jsonify({
        'game_id': game_id,
        'board': board,
        'winner': winner
    }), 200

