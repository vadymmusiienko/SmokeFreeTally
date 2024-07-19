# SmokeFreeTally

SmokeFreeTally is a web application designed to help individuals who are quitting smoking. It provides users with tools to track their progress, log smoke-free days, and visualize their achievements.

## Watch the Introduction Video

[![Watch the video](https://img.youtube.com/vi/FWr6OR4Z1yc/maxresdefault.jpg)](https://youtu.be/FWr6OR4Z1yc)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Database](#database)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and authentication.
- Tracking of smoke-free days.
- Logging of daily progress.
- Visualization of achievements and statistics.
- Customizable user settings.

## Installation

### Prerequisites
- Python 3.x
- Flask
- SQLite

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/vadymmusiienko/SmokeFreeTally.git
    cd smokefreetally
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    flask run
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Register for a new account.
3. Update your personal information on the settings page.
4. Navigate to the home page to log a smoke-free day.
5. Log in every day and track your progress.


## Routes

- `/`: Home page
- `/register`: User registration
- `/login`: User login
- `/settings`: User settings (personal information)
- `/resetpassword`: Reset your password
- `/about`: A page about te creator (me)

## Database

The application uses SQLite to store user data. The following tables are included:

### `users`
- `id`: Integer, primary key
- `username`: Text, unique
- `password_hash`: Text

### `user_info`
- `user_id`: Integer, primary key, foreign key to `users.id`
- `first_name`: Text
- `last_name`: Text
- `email`: Text
- `cigarettes_per_day`: Integer
- `pack_cost`: Real
- `gender`: Text

### `log_history`
- `user_id`: Integer, primary key, foreign key to `users.id`
- `first_log_date`: DateTime
- `last_log_date`: DateTime
- `total_days_logged`: Integer
- `streak`: Integer

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
