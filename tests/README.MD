<h1>Summary</h1>

<details>
    <summary><b>General ideas</b></summary>
    <ul>
        <li>Tests are written with minimal dup code. When a sequence of steps is needed in multiple tests, it's extrapolated into a function in <code>funcs.py</code></li>
        <li>Tests have markers for easy selective execution later.</li>
        <li>Tests have descriptions.</li>
        <li>Every test start with a known state by registering a new user. Unless specifically requires pre-existing data. This is with the assumption that test env doesn't care for extra test data.</li>
        <li>To run all tests without the reported bugs <code>python -m pytest -m "not bug"</code></li>
        <li>Thanks for reading! ~Josh</li>
    </ul>
</details>
<details>
    <summary><b>Added tests</b></summary>
    <details>
        <summary><code>test_auth.py</code></summary>
        <ul>
            <li>Register and login</li>
            <li>Invalid login</li>
            <li>Invalid registration</li>
            <li>Boundary of registration input</li>
            <li>Password strength</li>
            <li>Register a user that already exists</li>
        </ul>
    </details>
    <details>
        <summary><code>test_game.py</code></summary>
        <ul>
            <li>Create a game</li>
            <li>Attempt to create a game with invalid token</li>
            <li>Attempt to create a game with blank token</li>
            <li>Make one move in a game</li>
            <li>Play one happy path game with a winner</li>
            <li>Play one happy path game that ends in a draw</li>
            <li>A user cannot make a move on an occupied space</li>
            <li>A user cannot go twice in a row</li>
            <li>Only 2 users allowed to be in a game</li>
        </ul>
    </details>
    <details>
        <summary><code>test_util.py</code></summary>
        <ul>
            <li>Smoke spot checks on 4 board combinations that results in all possible results</li>
            <li>Exhaustive test on all possible combinations</li>
            <li>Bad input data or data type</li>
        </ul>
    </details>
</details>
<details>
    <summary><b>Added Markers</b></summary>
    See <code>pytest.ini</code> for details
</details>
<details>
    <summary><b>🐛Bugs🐛</b></summary>
    <ul>
        <li>No limit on username length when registration, potential attack vector to hang the BE.</li>
        <li>Wrong bad token resulted in 500 error.</li>
        <li>Wrong token format in header resulted in error in app.</li>
        <li>No validation of users. More than 2 users can be making moves on the same game.</li>
        <li>check_winner() does not raise error when extra elements are passed</li>
    </ul>
    
</details>