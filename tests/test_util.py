import pytest
from app.util import check_winner
from tests.funcs import *

"""
Add unit tests here to test the function `check_winner`
"""


# -----------------------------------------------------------------------------------
# Description: Spot check different boards to see outcome
#
# Verifies:
# ✅ Spot check results
# -----------------------------------------------------------------------------------
@pytest.mark.type_Unit
@pytest.mark.type_Smoke
@pytest.mark.type_Regression
@pytest.mark.parametrize("board, expected", [
    (
        [
            "X", "O", " ",
            " ", "X", "O",
            " ", " ", "X",
        ], "X"
    ),
    (
        [
            " ", "X", "O",
            "X", "O", " ",
            "O", "X", " ",
        ], "O"
    ),
    (
        [
            "O", "X", "O",
            "O", "X", "X",
            "X", "O", "X",
        ], "Draw"
    ),
    (
        [
            "O", " ", "X",
            " ", "X", " ",
            " ", " ", " ",
        ], None
    ),

])
def test_check_winner_sanity(board, expected):
    assert check_winner(board) == expected, f"Winner {expected} not raised for board {board}"

# -----------------------------------------------------------------------------------
# Description: An exhaustive test for all the possibilities.
#
# Verifies:
# ✅ All possibilities
# -----------------------------------------------------------------------------------
@pytest.mark.type_Unit
@pytest.mark.type_Regression
def test_check_winner_exhaustive():
    # Define the winning combos and return True if wins
    def has_winning_combo(combo, player):
        # All the winning positions
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        # Loop through each winning position
        for line in winning_positions:
            # Check if all positions are occupied by the same player
            if all(combo[pos] == player for pos in line):
                # If so return true
                return True
        return False

    # Get all the combos
    all_combos = get_all_board_combinations()

    # Loop through all the possible combos
    for combo in all_combos:

        players = {
            "X": has_winning_combo(combo, "X"),  # If has a win, mark True
            "O": has_winning_combo(combo, "O")   # If has a win, mark True
        }

        # Get the
        result = check_winner(combo)

        if players["X"] and not players["O"]:
            assert result == "X", f"Winner X not raised for board {combo}"
        elif not players["X"] and players["O"]:
            assert result == "O", f"Winner O not raised for board {combo}"
        elif players["X"] and players["O"]:
            assert result in ["X", "O"], f"Winner X nor O was not raised for board {combo}"
        elif " " not in combo:
            assert result == "Draw", f"Draw not raised for board {combo}"
        else:
            assert result is None, f"Should have been no winner for board {combo}"


# -----------------------------------------------------------------------------------
# Description: Bad board is passed
#
# Verifies:
# ✅ Bad boards
# -----------------------------------------------------------------------------------
@pytest.mark.type_Unit
@pytest.mark.type_ErrorHandling
@pytest.mark.bug
def test_check_winner_bad_board():
    bad_boards = [
        [],
        [""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    ]

    for board in bad_boards:
        with pytest.raises(IndexError):
            check_winner(board)


# -----------------------------------------------------------------------------------
# Description: Bad board type is passed
#
# Verifies:
# ✅ Bad board types
# -----------------------------------------------------------------------------------
@pytest.mark.type_Unit
@pytest.mark.type_ErrorHandling
def test_check_winner_bad_type():
    with pytest.raises(IndexError):
        check_winner("abc")

    with pytest.raises(KeyError):
        check_winner({})

    with pytest.raises(KeyError):
        check_winner({"a": "b", "c": "d"})

    with pytest.raises(TypeError):
        check_winner({"a", "b", "c", "d"})

    with pytest.raises(TypeError):
        check_winner()

    with pytest.raises(TypeError):
        check_winner(abc="def")
