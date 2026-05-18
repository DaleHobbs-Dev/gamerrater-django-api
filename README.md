# Gamer Rater API

Gamer Rater is a REST API for cataloging and rating board games. Users can add games, assign categories, upload action images, and leave ratings and reviews. This repository is the **Django REST Framework back end**.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-A30000?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

---

## Documentation

Project docs live in [`dev-docs/`](dev-docs/):

| File | Description |
| ---- | ----------- |
| [PRD.md](dev-docs/PRD.md) | Project requirements, scope, and learning goals |
| [ARCHITECTURE.md](dev-docs/ARCHITECTURE.md) | System overview, codebase map, API endpoints, and key technical decisions |
| [ERD.dbml](raterapi/docs/ERD.dbml) | Full database schema in DBML format |

---

## Features

- **Authentication** — register and log in with token-based auth
- **Games** — browse, search, filter by category or designer, create, edit, and delete games
- **Categories** — view all categories; create and manage them as an admin
- **Ratings** — leave a rating and review for any game, one per user per game
- **Pictures** — upload and view action images attached to games

---

## Setup & Installation

### Prerequisites

- Python 3.12+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

### Steps

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd gamerrater-django-api
   ```

2. Install dependencies:

   ```bash
   pipenv install
   ```

   > **Note:** You can also use the included `requirements.txt` instead:
   >
   > ```bash
   > python3 -m venv gamerrater-env
   > source gamerrater-env/bin/activate
   > pip install -r requirements.txt
   > ```

<!-- markdownlint-disable MD029 -->
3. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

4. Run migrations and load starter data:

   ```bash
   ./seed_database.sh
   ```

5. Open the project in VS Code.
6. Ensure the correct Python interpreter is selected.
7. Start the debugger. The server runs at `http://127.0.0.1:8000`.
<!-- markdownlint-enable MD029 -->

---

## User Authentication

Look in the `users.json` fixture file for available usernames. While the passwords in the fixture are encrypted, the source password for every user is `Admin8*`.

---

## Resetting the Database

Run `./seed_database.sh` any time you want to roll back your data to its original state. It deletes the database, removes existing migrations, recreates the schema from your current models, and reloads all fixture data.

---

## Contributors

| Name | GitHub |
| ---- | ------ |
| Dale Hobbs | [@DaleHobbs-Dev](https://github.com/DaleHobbs-Dev) |
