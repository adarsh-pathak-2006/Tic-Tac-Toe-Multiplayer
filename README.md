# Multiplayer Tic-Tac-Toe Backend (Django + Channels)

This is the backend repository for the **Multiplayer Tic-Tac-Toe** platform, built with **Django**, **Django REST Framework (DRF)**, and **Django Channels (WebSockets)** to support seamless real-time gameplay.

## 🚀 Key Features
- **Real-Time WebSockets**: Powered by Django Channels and Redis (via InMemoryChannelLayer for dev) to transmit game moves instantaneously.
- **JWT Authentication**: Secure API endpoints and WebSocket handshakes using JSON Web Tokens (via `rest_framework_simplejwt`).
- **RESTful API**: Standardized endpoints for User Registration, Authentication, Profile Management, and Matchmaking.
- **Async Consumer**: Asynchronous Django Channels Consumer (`TicTacToeConsumer`) ensuring zero blocking threads during high-concurrency matches.

## 🛠 Tech Stack
- **Framework**: Django 5.2
- **API**: Django REST Framework (DRF)
- **Real-Time**: Django Channels, ASGI (Daphne)
- **Database**: SQLite (Development) / PostgreSQL Ready (Production)
- **Authentication**: JWT (JSON Web Tokens)

## 📦 Local Setup & Deployment

### 1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

*(Note: If `requirements.txt` is missing, you can install the core dependencies via: `pip install django djangorestframework djangorestframework-simplejwt channels daphne django-cors-headers python-dotenv`)*

### 2. Environment Variables
This project uses `python-dotenv` for managing environment secrets.
Create a `.env` file in the root directory (where `manage.py` is located) by copying the example:

```bash
cp .env.example .env
```

**Ensure you update your `.env` file with appropriate secure values for production:**
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=api.yourdomain.com,localhost
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 3. Database Migrations
Run the standard Django migrations to set up your database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the ASGI Server
Since this app relies heavily on WebSockets, you **must** run it using an ASGI server (like Daphne or Uvicorn), rather than standard WSGI.

```bash
# Development
python manage.py runserver

# Production (using Daphne)
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

## 🔌 API Endpoints
- `POST /auth/register/` - Register a new player
- `POST /auth/login/` - Obtain JWT access & refresh tokens
- `GET /auth/profile/me/` - Retrieve logged-in player profile
- `GET /auth/profile/all/` - Retrieve all available players for matchmaking
- `GET /logic/games/` - Retrieve player's match history
- `POST /logic/games/` - Challenge another player to a new game (Requires `player2` ID)

## 📡 WebSockets
**Connection URL:** `ws://<domain>/ws/game/<game_id>?token=<jwt_access_token>`

The client can send JSON messages in this format to play a move:
```json
{
    "move": "H1V1" 
}
```
*Note: Valid grids are H1V1 to H3V3 (Row vs Column).*

---
*Built with ❤️ for real-time web experiences.*
