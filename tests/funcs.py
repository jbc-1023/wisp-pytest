import itertools
import json
import random
from jsonschema import validate


# -------------------------------------------------------------------------------------------------
# Generate a random string of a specific length
# that contains caps and/or lower case and/or numbers and/or special chars
# -------------------------------------------------------------------------------------------------
def random_str(length: int = 12, caps: bool = True, lower: bool = True, numbers: bool = True,
               special: bool = False) -> str:

    # Error handling
    if length <= 0:
        raise ValueError('Length must be greater than or equal to 0')

    # Pool of chars
    allowed_chars = []
    if caps:
        allowed_chars += ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    if lower:
        allowed_chars += ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    if numbers:
        allowed_chars += ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if special:
        allowed_chars += ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=",
                          ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "{", "~"]

    # Generate a random string of specific length from the char pool
    output_char = ""
    for i in range(length):
        output_char += random.choice(allowed_chars)

    return output_char


# -------------------------------------------------------------------------------------------------
# Login with a specific username and password
# -------------------------------------------------------------------------------------------------
def login(client, username: str, password: str) -> object:
    return client.post(
        '/auth/login',
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type='application/json'
    )


# -------------------------------------------------------------------------------------------------
# Check response code matches what is expected
# -------------------------------------------------------------------------------------------------
def check_code(gotten_code: int, expect: int, message: str = ""):
    assert gotten_code == expect, f"Request expected return code {expect}, but got {gotten_code} instead. {message}"


# -------------------------------------------------------------------------------------------------
# Check if the response is a valid JSON
# -------------------------------------------------------------------------------------------------
def check_valid_json(response):
    try:
        response_body = response.json
    except ValueError:
        assert False, "Response body is not valid JSON"
    return response_body


# -------------------------------------------------------------------------------------------------
# Validate JSON matches schema
# -------------------------------------------------------------------------------------------------
def validate_json_schema(in_json: dict, schema: dict):
    assert validate(instance=in_json, schema=schema) is None, "Response body schema not match expected"


# -------------------------------------------------------------------------------------------------
# Bad login routine, where the login is not expected to succeed.
# -------------------------------------------------------------------------------------------------
def bad_login(client, username: str, password: str, expected_code: int):
    # Send request
    response = login(client, username, password)

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=expected_code)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # If no credentials are given
    if username == "" or password == "":
        # Set the expected schema
        expected_schema = {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string"
                }
            },
            "required": ["message"]
        }

        # ✅ Check response data format against expected schema
        validate_json_schema(response_body, expected_schema)

        # ✅ Check response data
        msg = "Username and password are required"
        assert response_body['message'] == msg, \
            f"Response value for \"message\" is incorrect. Expected \"{msg}\" but got \"{response_body['status']}\"."
    # If invalid credentials are given
    else:
        # Set the expected schema
        expected_schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string"
                }
            },
            "required": ["status"]
        }

        # ✅ Check response data format against expected schema
        validate_json_schema(response_body, expected_schema)

        # ✅ Check response data
        msg = "failed"
        assert response_body['status'] == msg, \
            f"Response value for \"status\" is incorrect. Expected \"{msg}\" but got \"{response_body['status']}\"."

    # ✅ Check response data
    assert 'token' not in response_body, "Response should not contain \"token\"."
    assert 'user' not in response_body, "Response should not contain \"user\"."
    assert 'wins' not in response_body, "Response should not contain \"wins\"."


# -------------------------------------------------------------------------------------------------
# Check validity of token
# -------------------------------------------------------------------------------------------------
def check_token(token: str):
    """
    This is where token key is obtained from a secret (probably from CI)
    and used to parse to validate it is indeed a valid token and
    that the expiration time is as expected
    """

    ## Obtained from env var set by CI
    # secret_or_public_key = os.getenv('jwt_token')
    #
    # try:
    #     decoded_token = jwt.decode(token, secret_or_public_key, algorithms=["HS256"])
    #     print(decoded_token)
    #
    # except jwt.ExpiredSignatureError:
    #     assert False, "Gotten token is expired"
    # except jwt.InvalidTokenError:
    #     assert False, "Gotten token is invalid"

    pass


# -------------------------------------------------------------------------------------------------
# Register with a username and password if manual.
# Default is generate random string for username and password.
# Does not check for validity
# -------------------------------------------------------------------------------------------------
def register(client, username="", password="", manual_set=False):
    # If not manually setting, generate a random username and password
    if not manual_set:
        username = random_str()
        password = random_str()

    # Send request to register
    response = client.post(
        '/auth/register',
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type='application/json'
    )

    return response, username, password


# -------------------------------------------------------------------------------------------------
# Setup a new user with a random username and password
# Then login and then return token, wins, and response
# -------------------------------------------------------------------------------------------------
def new_user_setup(client, context):
    # Register with a random username and password
    response, username, password = register(client)
    check_code(gotten_code=response.status_code, expect=201)

    # Login
    response = login(client, username, password)
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Get token
    token = response_body['token']

    # Get wins
    wins = response_body['user']['wins']

    # Update context fixture so these can be used elsewhere if needed
    context["user"] = {
        "username": username,
        "password": password,
        "token": token,
        "wins": wins
    }

    return context["user"]


# -------------------------------------------------------------------------------------------------
# Create a new game with a given token
# -------------------------------------------------------------------------------------------------
def create_game(client, token: str):
    # Create a new game
    response = client.post(
        '/game',
        headers={
            'Authorization': token
        }
    )
    return response


# -------------------------------------------------------------------------------------------------
# Make a move to a specific spot
# -------------------------------------------------------------------------------------------------
def make_move(client, move: int, game_id: int, token: str):
    # Make a move
    response = client.post(
        '/game/move',
        headers={
            'Authorization': token
        },
        data=json.dumps({
            "game_id": game_id,
            "move": move
        }),
        content_type='application/json'
    )
    return response


# -------------------------------------------------------------------------------------------------
# Make a move and return if there was a winner
# -------------------------------------------------------------------------------------------------
def make_move_user(client, move: int, game_id: int, token: str, expected_flair: str):
    response = make_move(client, move, game_id, token)
    response_body = check_valid_json(response)

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check move was made correctly
    assert response_body['board'][move] == expected_flair, \
        f"The move \"{move}\" was expected to be \"{expected_flair}\" but got \"{response_body['board'][move]}\""

    # Return winner response
    return response_body['winner']


# -------------------------------------------------------------------------------------------------
# Return all possibilities of the board.
# There are 3 possibilities with 9 places = 3^9 = 19,683 possibilities
# -------------------------------------------------------------------------------------------------
def get_all_board_combinations():
    # Possible chars
    chars = [" ", "X", "O"]

    # Get all the combos
    combos = [''.join(p).ljust(9) for p in itertools.product(chars, repeat=9)]

    # Separate all combos into individual arrays
    all_combinations = []
    for combo in combos:
        all_combinations.append(list(combo))

    return all_combinations

