# Pokémon Manager

Pokémon Manager is a Flask-based web application that allows users to manage their Pokémon card collections. Users can view their cards, transfer cards to other users, and perform other account-related actions. The application uses SQLite as its database and includes features like CSRF protection, secure authentication, and dynamic templates.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Security Features](#security-features)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Authentication**: Secure login system with hashed passwords.
- **Card Management**: View Pokémon cards owned by a user.
- **Card Transfer**: Transfer Pokémon cards between users with validation.
- **Dynamic Templates**: Responsive and interactive UI using Jinja2 templates.
- **CSRF Protection**: Ensures secure form submissions.
- **Database Management**: Predefined scripts for setting up and populating the database.

---

## Project Structure

```
├── app.py                     # Main Flask application
├── bank.db                    # SQLite database file (auto-generated)
├── card_service.py            # Card-related database operations
├── user_service.py            # User-related database operations
├── bin/                       # Scripts for database setup and population
│   ├── createdb.py            # Script to create the users table
│   ├── makeaccounts.py        # Script to create accounts table
│   ├── populatecards.py       # Script to populate user_cards table
│   └── pokemon_setup/         # Pokémon database setup
│       ├── create_and_populate_pokemon_db.py # Script to populate Pokémon data
│       └── pokemon_base_set.csv             # Pokémon data in CSV format
├── templates/                 # HTML templates for the web app
│   ├── base.html              # Base template
│   ├── dashboard.html         # Dashboard page
│   ├── details.html           # Card details page
│   ├── login.html             # Login page
│   ├── transfer.html          # Transfer form
│   └── transfer_success.html  # Transfer success page
├── .vscode/                   # VS Code settings
│   └── settings.json          # Editor configuration
├── .pylintrc                  # Pylint configuration
├── .gitignore                 # Git ignore rules
└── requirements.txt           # Python dependencies
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- SQLite
- Flask and required Python packages (see `requirements.txt`)

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python bin/createdb.py
    python bin/makeaccounts.py
    python bin/pokemon_setup/create_and_populate_pokemon_db.py
    python bin/populatecards.py
    ```

4. Run the application:
    ```bash
    flask run
    ```

5. Open the app in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

### Login

Use the following credentials to log in:
- **Email**: `alice@example.com`
- **Password**: `123456`

### Features

- **Dashboard**: View available actions.
- **Details**: View your Pokémon card collection.
- **Transfer**: Transfer cards to another user.

---

## API Endpoints

### `/`
- **Method**: GET  
- **Description**: Redirects to the login page if not logged in, otherwise redirects to the dashboard.

### `/login`
- **Method**: POST  
- **Description**: Authenticates the user and sets a secure cookie.

### `/dashboard`
- **Method**: GET  
- **Description**: Displays the user's dashboard with available actions.

### `/details`
- **Method**: GET  
- **Description**: Displays the Pokémon cards owned by the user.

### `/transfer`
- **Method**: GET, POST  
- **Description**: Allows the user to transfer Pokémon cards to another user.

### `/logout`
- **Method**: GET  
- **Description**: Logs the user out by deleting the authentication cookie.

---

## Security Features

- **Password Hashing**: Passwords are hashed using `pbkdf2_sha256` before storage.
- **CSRF Protection**: All forms are protected against CSRF attacks using Flask-WTF.
- **Input Validation**: User inputs are validated to prevent SQL injection and XSS attacks.
- **Secure Cookies**: Authentication tokens are stored in secure cookies.

---

## Database Schema

### Tables

#### `users`
- `email` (TEXT, Primary Key)  
- `name` (TEXT)  
- `password` (TEXT)  

#### `accounts`
- `id` (TEXT, Primary Key)  
- `owner` (TEXT, Foreign Key to `users.email`)  
- `balance` (INTEGER)  

#### `pokemon_base_set`
- `id` (INTEGER, Primary Key)  
- `name` (TEXT)  
- `type` (TEXT)  
- `hp` (INTEGER)  
- `rarity` (TEXT)  

#### `user_cards`
- `owner` (TEXT, Foreign Key to `users.email`)  
- `card_id` (INTEGER, Foreign Key to `pokemon_base_set.id`)  
- `card_count` (INTEGER)  