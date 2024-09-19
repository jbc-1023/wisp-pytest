import pytest
from tests.funcs import *

"""
Add functional tests here to test the game endpoints using the specs/requirements in the README
The auth endpoint files are located in app/routes/game.py
"""


# -----------------------------------------------------------------------------------
# Description: With a new user, create a game
# Verifies:
# ✅ A new game be created
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.game_CreateGame
def test_game_create(client, context):
    # Create a new user and login to get token
    user_data = new_user_setup(client, context)

    # Create a new game
    response = create_game(client, user_data['token'])

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Set the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "game_id": {
                "type": "integer"
            }
        },
        "required": ["game_id"]
    }

    # ✅ Check response data format against expected schema
    validate_json_schema(response_body, expected_schema)

    # ✅ Check response data
    assert 'game_id' in response_body, "Expected 'game_id' in the response body, was not there."
    assert response_body['game_id'] > 0, "Game id should be greater than 0"
    game_id_1 = response_body['game_id']

    # Create another new game
    response = create_game(client, user_data['token'])

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # ✅ Check response data
    assert 'game_id' in response_body, "Expected 'game_id' in the response body, was not there."
    assert response_body['game_id'] > game_id_1, "New game_id should be greater than the previous"


# -----------------------------------------------------------------------------------
# Description: Try to create a game with a bad token
# Verifies:
# ✅ A new game cannot be created with a bad token
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_ErrorHandling
@pytest.mark.game_CreateGame
@pytest.mark.bug
def test_game_create_bad_token(client):
    # Create a new game
    response = create_game(client, "bad_token")

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # This results in a 500 which should never happen and so this is a bug that should be addressed


# -----------------------------------------------------------------------------------
# Description: Attempt to create a game with no token
# Verifies:
# ✅ A new game cannot be created with no token
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_ErrorHandling
@pytest.mark.game_CreateGame
def test_game_create_no_token(client):
    # Create a new game
    response = create_game(client, "")

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=403)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Set the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": ["null", "object"]
            },
            "error": {
                "type": "string"
            },
            "message": {
                "type": "string"
            }
        },
        "required": ["data", "error", "message"]
    }

    # ✅ Check response data format against expected schema
    validate_json_schema(response_body, expected_schema)

    # ✅ Check response data
    assert response_body['data'] is None, "Data should have been None or Null"
    msg = "Unauthorized"
    assert response_body['error'] == msg, f"Error message should have been \"{msg}\" but got \"{response_body['error']}\""
    msg = "Authentication Token is missing!"
    assert response_body["message"] == msg, f"Error message should have been \"{msg}\" but got  \"{response_body['error']}\""


# -----------------------------------------------------------------------------------
# Description: Make a single move
# Verifies:
# ✅ A game can be created
# ✅ A user can make a (random) valid move
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.game_Move
def test_game_move(client, context):
    # Create a new user and login to get token
    user_data = new_user_setup(client, context)

    # Create a new game
    response = create_game(client, user_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # Make a random move
    move_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random_move = random.choice(move_list)
    response = make_move(client=client, move=random_move, game_id=game_id, token=user_data['token'])

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Set the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "board": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [" ", "X", "O"]
                },
                "minItems": 9,
                "maxItems": 9
            },
            "game_id": {
                "type": "integer"
            },
            "winner": {
                "type": ["null", "string"],
                "enum": [None, "X", "O"]
            }
        },
        "required": ["board", "game_id", "winner"]
    }

    # ✅ Check response data format against expected schema
    validate_json_schema(response_body, expected_schema)

    # ✅ Response data
    assert 'winner' in response_body, "The \"winner\" key was not present in the response."
    assert response_body['winner'] is None, "User should not have won."
    assert "board" in response_body, "The \"board\" key was not present in the response."
    assert response_body['board'][random_move] == "X", f"Move was expected at {random_move} but was not seen."


# -----------------------------------------------------------------------------------
# Description: Have a back and forth between 2 users. X is the first user. Have X win
#
# Verifies:
# ✅ Can X move
# ✅ Can O move
# ✅ Can X win
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.game_Move
def test_game_single_game_with_winner_sanity(client, context):
    # Create a new users and login to get token
    user1_data = new_user_setup(client, context)
    user2_data = new_user_setup(client, context)

    # User 1 Create a new game
    response = create_game(client, user1_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=4, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [0] [1] [2]
    # [3] [X] [O]
    # [6] [7] [8]
    assert make_move_user(client, move=5, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [O]
    # [6] [7] [X]
    assert make_move_user(client, move=8, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [0] [1] [2]
    # [3] [X] [O]
    # [6] [7] [X]
    assert make_move_user(client, move=0, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [O]
    # [6] [X] [X]
    assert make_move_user(client, move=7, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [0] [0] [2]
    # [3] [X] [O]
    # [6] [X] [X]
    assert make_move_user(client, move=1, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # ✅ User 1 (X) make a move and win
    # [0] [0] [2]
    # [3] [X] [O]
    # [X]-[X]-[X] 👈
    assert make_move_user(client, move=6, game_id=game_id, token=user1_data['token'], expected_flair="X") is "X", \
        "X should have won"

# -----------------------------------------------------------------------------------
# Description: Have a back and forth between 2 users. Have game end in draw
#
# Verifies:
# ✅ Game can result in draw
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.game_Move
def test_game_single_game_with_draw_sanity(client, context):
    # Create a new users and login to get token
    user1_data = new_user_setup(client, context)
    user2_data = new_user_setup(client, context)

    # User 1 Create a new game
    response = create_game(client, user1_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=4, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [0] [1] [O]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=2, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # User 1 (X) make a move
    # [0] [1] [O]
    # [3] [X] [5]
    # [6] [7] [X]
    assert make_move_user(client, move=8, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [O] [1] [O]
    # [3] [X] [5]
    # [6] [7] [X]
    assert make_move_user(client, move=0, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # User 1 (X) make a move
    # [O] [X] [O]
    # [3] [X] [5]
    # [6] [7] [X]
    assert make_move_user(client, move=1, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [O] [X] [O]
    # [3] [X] [5]
    # [6] [O] [X]
    assert make_move_user(client, move=7, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # User 1 (X) make a move
    # [O] [X] [O]
    # [3] [X] [X]
    # [6] [O] [X]
    assert make_move_user(client, move=5, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [O] [X] [O]
    # [O] [X] [X]
    # [6] [O] [X]
    assert make_move_user(client, move=3, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # ✅ User 1 (X) make a move and draw
    # [O] [X] [O]
    # [O] [X] [X]
    # [X] [O] [X]
    assert make_move_user(client, move=6, game_id=game_id, token=user1_data['token'], expected_flair="X") == "Draw", \
        "Should have been a draw game"


# -----------------------------------------------------------------------------------
# Description: A user cannot make a move on a square that already been occupied
#
# Verifies:
# ✅ Can't move to an occupied space by another user
# ✅ Can't move to an occupied space by your previous move
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_ErrorHandling
@pytest.mark.game_Move
def test_game_single_game_same_space(client, context):
    # Create a new users and login to get token
    user1_data = new_user_setup(client, context)
    user2_data = new_user_setup(client, context)

    # User 1 Create a new game
    response = create_game(client, user1_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=4, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # ✅ User 2 (O) can't make a move onto a space where X already has occupied
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    response = make_move(client, move=4, game_id=game_id, token=user2_data['token'])
    response_body = check_valid_json(response)
    check_code(gotten_code=response.status_code, expect=400, message="User shouldn't be able to move to an occupied space.")
    msg = "Invalid move"
    assert response_body['message'] == "Invalid move", \
        f"Expected message \"{msg}\" but got \"{response_body['message']}\" instead."

    # User 2 (O) make a move
    # [0] [1] [O]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=2, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # ✅ User 1 (X) can't make a move onto its own space
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    response = make_move(client, move=4, game_id=game_id, token=user1_data['token'])
    response_body = check_valid_json(response)
    check_code(gotten_code=response.status_code, expect=400, message="User shouldn't move onto it's own occupied space")
    msg = "Invalid move"
    assert response_body['message'] == "Invalid move", \
        f"Expected message \"{msg}\" but got \"{response_body['message']}\" instead."

# -----------------------------------------------------------------------------------
# Description: A user cannot go twice in a row
#
# Verifies:
# ✅ Can't go again if just went
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_ErrorHandling
@pytest.mark.game_Move
@pytest.mark.bug
def test_game_single_game_user_twice(client, context):
    # Create a new users and login to get token
    user1_data = new_user_setup(client, context)
    user2_data = new_user_setup(client, context)

    # User 1 Create a new game
    response = create_game(client, user1_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=4, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # ✅ User 1 (X) can't make a move again
    response = make_move(client, move=4, game_id=game_id, token=user2_data['token'])
    response_body = check_valid_json(response)
    check_code(gotten_code=response.status_code, expect=400, message="User shouldn't be able to go twice in a row.")
    msg = "Invalid move"
    assert response_body['message'] == "Invalid move", \
        f"Expected message \"{msg}\" but got \"{response_body['message']}\" instead."


# -----------------------------------------------------------------------------------
# Description: Only 2 users allowed to be in a game.
#
# Verifies:
# ✅ Can't allow a 3rd user to join when 2 users are already in play
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_ErrorHandling
@pytest.mark.game_Move
@pytest.mark.bug
def test_game_single_game_user_twice(client, context):
    # Create a new users and login to get token
    user1_data = new_user_setup(client, context)
    user2_data = new_user_setup(client, context)
    user3_data = new_user_setup(client, context)

    # User 1 Create a new game
    response = create_game(client, user1_data['token'])
    response_body = check_valid_json(response)
    game_id = response_body['game_id']

    # User 1 (X) make a move
    # [0] [1] [2]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=4, game_id=game_id, token=user1_data['token'], expected_flair="X") is None, \
        "Should have a winner yet"

    # User 2 (O) make a move
    # [0] [1] [O]
    # [3] [X] [5]
    # [6] [7] [8]
    assert make_move_user(client, move=2, game_id=game_id, token=user2_data['token'], expected_flair="O") is None, \
        "Should have a winner yet"

    # ✅ User 3 not allowed to join
    response = make_move(client, move=0, game_id=game_id, token=user3_data['token'])
    response_body = check_valid_json(response)
    check_code(gotten_code=response.status_code, expect=400, message="A 3rd user shouldn't be able to join.")
    msg = "Invalid move"
    assert response_body['message'] == "Invalid move", \
        f"Expected message \"{msg}\" but got \"{response_body['message']}\" instead."
