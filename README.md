# Tic-Tac-Toe API

This is a Tic-Tac-Toe API built using Flask for the backend and SQLite for the database.
The API allows users to register, log in, create a new game, update the game's move data, and declare a winner.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running the test suite](#running-the-test-suite)
- [API Endpoints](#api-endpoints)
- [Takehome prompt](#takehome-prompt)


## Features

- User Registration and Authentication
- Create Games
- Stores the moves in the game
- Declare a winner
- Track wins per user

## Tech Stack

- **Backend:** Flask
- **Database:** SQLite
- **Testing tool:** pytest

This project uses [venv](https://docs.python.org/3/library/venv.html#module-venv)

## Installation

### Prerequisites

- Python 3.8+
- SQLite

### Setup steps

1. Clone the repository:

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    . .venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```
4. Spin up a SQLite DB based on the preconfigured schema:
    ```bash
    python -m flask init-db
    ```


## Running the Application

1. Start the Flask server:
    ```bash
    python -m flask run
    ```

## Running the test suite

1. Run the pytest test suite using this command:
    ```bash
    python -m pytest
    ```
    Note: if you have trouble with this command, make sure you've activated venv

## API Endpoints

### Ping for uptime
- **URL:** `/ping`
- **Method:** `GET`
- **Request Body:** {}
- **Response Status & Body:**
    - `200` on success
        ```json
        {
            "message": "pong!"
        }
        ```

### User Registration

- **URL:** `/auth/register`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
- **Response Status & Body:**
    - `201 Created` on success
        ```json
        {
            "message": "success message",
            "user": {
                "id": "user_id",
                "username": "your_username",
                "wins": "number of wins for the user. should be 0 when you register"
        }
        ```
    - `400 Bad Request` if username already exists or fields are missing
        ```json
        {
            "message": "error message"
        }
        ```

### User Login

- **URL:** `/auth/login`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
- **Response Status & Body:**
    - `200 OK` on success
        ```json
        {
            "status": "success status",
            "token": "JWT needed for future requests. 30 min expiration",
            "user": {
                "id": "your user id",
                "username": "your username",
                "wins": "user's number of wins"
            }
        }
        ```
    - `401 Unauthorized` if credentials are incorrect
        ```json
        {
            "status": "error status"
        }
        ```

### Create Game

- **URL:** `/game`
- **Method:** `POST`
- **Request Header:**
    ```json
    {
        "Authorization": "JWT issued from login"
    }
    ```
- **Request Body:**
    ```json
    {
    }
    ```
- **Response:**
    - `200 OK` with `game_id`

### Make Move

- **URL:** `/game/move`
- **Method:** `POST`
- **Request Header:**
    ```json
    {
        "Authorization": "JWT issued from login"
    }
    ```
- **Request Body:**
    ```json
    {
        "game_id": "game_id",
        "move": "location of the move on the board (int 0-8)"
    }
    ```
- **Response Status & Body:**
    - `200 OK` on success
    - `400 Bad Request` if the request content is invalid, the game has a winner already, or the move is invalid
    ```json
    {
        "game_id": "game_id",
        "board": "game_id",
        "winner": "returns the winning user X/O or None if there is no winner"
    }
    ```

## Takehome prompt
Currently, the API has no backend tests and your task is to write tests in Pytest for code coverage.
Files have been added to the `./tests/` directory where you can write tests. Here are the requirements:
- We are asking you to write both unit tests and integration/functional/API tests. Show us that you can do both!
- You must use Pytest. We use that framework here at Wisp.
- You may make updates to the `conftest.py` file, write your own test helpers, or add additional dependencies (e.g., Factory Boy).
- In general, try to avoid refactoring any of the API code except in cases where it makes testing the code easier.
- Limit yourself to 2 hours of work. That means you should prioritize key features that should have test coverage! Don't worry too much
  about getting to 100% coverage. We care more about the quality of your work than your quantity.

### Project Submission
Please submit your test code as a Pull Request.

- Within the PR, please include:
  - Any decisions you made and your reasoning. Examples:
      - Refactored the "Make Move" endpoint because...
      - Added a new dependency because...
  - Any test cases you couldn't get to, but would like to in the future.

Once you open your PR, reach back out to the hiring manager for review.

### Evaluation

We’ll review your code submission for the following:

- Functionality: Do the tests cover relevant functional areas, are they are flaky, and are they performant.
- Test find-ability, organization and maintainability.
- General coding practices including naming, code structure, and readability.
