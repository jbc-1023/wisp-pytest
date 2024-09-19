import pytest
from tests.funcs import *

"""
Add functional tests here to test the auth endpoints using the specs/requirements in the README
The auth endpoint files are located in app/routes/auth.py
"""


# -----------------------------------------------------------------------------------
# Description: Register and validate by login
# Verifies:
# ✅ User can register
# ✅ User can login
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.account_Registration
@pytest.mark.account_Login
def test_register_login_sanity(client):
    # Register ----------------------------------------------------
    # Register with a random username and password
    response, username, password = register(client)

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=201)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Set the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string"
            },
            "user": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "username": {
                        "type": "string"
                    },
                    "wins": {
                        "type": "integer"
                    }
                },
                "required": ["id", "username", "wins"]
            }
        },
        "required": ["message", "user"]
    }

    # ✅ Check response data format against expected schema
    validate_json_schema(response_body, expected_schema)

    # ✅ Check response data
    msg = "User registered successfully!"
    assert response_body['message'] == msg, \
        f"Response value for \"message\" is incorrect. Expected \"{msg}\" but got \"{response_body['message']}\"."
    assert response_body['user']['id'] >= 1, "Response value for \"user:id\" should not be negative or zero."
    assert response_body['user']['username'] == username, \
        f"Response value for \"user:username\" is incorrect. Expected \"{username}\" but got \"{response_body['user']['username']}\""
    assert response_body['user']['wins'] >= 0, "Expected \"user:wins\" to not be negative"

    # Save user id for login test later
    user_id = response_body['user']['id']

    # Save wins for login test later
    user_wins = response_body['user']['wins']

    # Login ------------------------------------------------------------
    # Send request
    response = login(client, username, password)

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=200)

    # ✅ Check response data format
    response_body = check_valid_json(response)

    # Set the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string"
            },
            "token": {
                "type": "string"
            },
            "user": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "username": {
                        "type": "string"
                    },
                    "wins": {
                        "type": "integer"
                    }
                },
                "required": ["id", "username", "wins"]
            }
        },
        "required": ["status", "token", "user"]
    }

    # ✅ Check response data format against expected schema
    validate_json_schema(response_body, expected_schema)

    # ✅ Check response data
    msg = "success"
    assert response_body['status'] == msg, \
        f"Response value for \"status\" is incorrect. Expected \"{msg}\" but got \"{response_body['status']}\"."
    assert response_body['token'] is not "", "Response value for \"token\" should not be empty."
    check_token(response_body['token'])
    assert response_body['user']['id'] == user_id, \
        f"Response value for \"user:id\" is incorrect. Expected \"{user_id}\" but got \"response_body['user']['id']\""
    assert response_body['user']['username'] == username, \
        f"Response value for \"user:username\" is incorrect. Expected \"{username}\" but got \"{response_body['user']['username']}\""
    assert response_body['user']['wins'] == user_wins, \
        f"REsponse value for \"user:wins\" is incorrect. Expected \"{user_wins}\" but got \"response_body['user']['wins']\""


# -----------------------------------------------------------------------------------
# Description: Attempt to login with bad or invalid credentials
# and verify not logged in.
#
# Note: Emoji, UTF-8, Special chars in password is not tested as passwords are presumed
# converted to hash. Unsure expected outcome, need to review spec before writing test.
#
# Verifies user logging in with username/password combos:
# ✅ Non-existing user
# ✅ Blanks
# ✅ Space char only (trim)
# ✅ Emoji
# ✅ UTF-8
# ✅ Special chars
#
# -----------------------------------------------------------------------------------
@pytest.mark.type_ErrorHandling
@pytest.mark.type_Regression
@pytest.mark.account_Login
def test_login_invalid(client):
    checks = [
        # ✅ Non-existing user
        [random_str(length=20), random_str(), 403],  # Making username long to avoid accidentally land on an existing

        # ✅ Blank password
        [random_str(), "", 400],

        # ✅ Blank username
        ["", random_str(), 400],

        # ✅ Blank both username and password
        ["", "", 400],

        # ✅ Space char username
        [" ", random_str(), 403],

        # ✅ Space char password
        [" ", random_str(), 403],

        # ✅ Space char username and password
        [" ", " ", 403],

        # ✅ Emoji in username
        ["❤️", random_str(), 403],
        ["❤️Josh", random_str(), 403],
        ["️Jo❤sh", random_str(), 403],
        ["️Josh❤", random_str(), 403],

        # ✅ UTF-8 char in username
        ["ö", random_str(), 403],
        ["Jösh", random_str(), 403],
        ["これは日本語です", random_str(), 403],

        # ✅ Special chars (mixed inside username)
        [f"{random_str()}!'#%&()*+-.:;<>=[]|_~{random_str()}", random_str(), 403],
    ]

    for check in checks:
        bad_login(client,
                  username=check[0],
                  password=check[1],
                  expected_code=check[2]
                  )


# -----------------------------------------------------------------------------------
# Description: Attempt to register with bad or invalid credentials
# and verify register not successful and verify can't login after unsuccessful register
#
# Note: Emoji, UTF-8, Special chars in password is not tested as passwords are presumed
# converted to hash. Unsure expected outcome, need to review spec before writing test.
#
# Verifies user register in with username/password combos:
# ✅ Non-existing user
# ✅ Blanks
# ✅ Space char only (trim)
# ✅ Emoji
# ✅ UTF-8
# ✅ Special chars
# -----------------------------------------------------------------------------------
@pytest.mark.type_ErrorHandling
@pytest.mark.type_Regression
@pytest.mark.account_Login
def test_register_invalid(client):
    """
    Not going to spend time repeating. Generally same format as test_login_invalid()
    """
    assert True


# -----------------------------------------------------------------------------------
# Description: Create account with maximum amount of chars
# for username and/or password
# -----------------------------------------------------------------------------------
@pytest.mark.type_Boundary
@pytest.mark.account_Registration
@pytest.mark.account_Login
@pytest.mark.bug
def test_register_boundary(client):
    # Generate a random username and password
    username = random_str(length=40960)
    password = random_str()

    # Register ----------------------------------------------------
    # Send request
    response = client.post(
        '/auth/register',
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type='application/json'
    )

    # ✅ Check response code
    check_code(gotten_code=response.status_code, expect=403)

    """
    There appears to be no upper boundary and was successfully able to create up to 40960 chars.
    I would have advised to cap this to a sane length in the backend 
    to avoid unpredictable behavior or a bad actor attempts to crash the server 
    with a long ass username/password.

    Additionally, what ever limit is set in backend must be matched by front end.
    """


# -----------------------------------------------------------------------------------
# Description: Cannot create an account when the password security
# strength requirement isn't met.
# -----------------------------------------------------------------------------------
@pytest.mark.account_Registration
@pytest.mark.account_Login
def test_register_password_strength(client):
    """
    There appears to be no security strength requirement so this is left blank.
    If there were, the test to validate that would go here.
    """
    pass


# -----------------------------------------------------------------------------------
# Description: Cannot create an account that exists already.
#
# Verifies
# ✅ An account of the same name can't be created again
# -----------------------------------------------------------------------------------
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.account_Registration
def test_register_exists(client):
    # Generate a random username and password
    username = random_str()
    password = random_str()

    # Register first time
    response = client.post(
        '/auth/register',
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type='application/json'
    )
    check_code(gotten_code=response.status_code, expect=201)

    # Register second time
    response = client.post(
        '/auth/register',
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type='application/json'
    )

    # ✅ Check response data format and response code
    response_body = check_valid_json(response)
    check_code(gotten_code=response.status_code, expect=400)

    # ✅ Check response data
    msg = "Username already exists!"
    assert response_body['message'] == msg, \
        f"Response value for \"message\" is incorrect. Expected \"{msg}\" but got \"{response_body['message']}\"."
    assert "user" not in response_body, "User should not be in response"


