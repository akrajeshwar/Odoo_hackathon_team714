# Ticket Management System

A simple web-based ticket issue platform with role-based access control built with Flask and SQLite.

## Features

- **User Authentication**: Login and registration system
- **Role-based Access Control**: 
  - **Users**: Can create and view their own tickets
  - **Agents**: Can view all tickets and update their status
  - **Admin**: Full system access (predefined account)
- **Ticket Management**: Create, view, and manage support tickets
- **Status Tracking**: Open → In Progress → Resolved workflow
- **Modern UI**: Bootstrap dark theme with responsive design

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone or download this project to your local machine
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy Werkzeug email-validator gunicorn
   ```
6. Run the application:
   ```bash
   python main.py
   ```
7. Open your browser and go to `http://localhost:5000`

### Default Admin Account
- **Username**: admin
- **Password**: admin123

## Project Structure

```
ticket-system/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models (User, Ticket)
├── routes.py           # Application routes and views
├── tickets.db          # SQLite database (created automatically)
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── user_dashboard.html      # User dashboard
│   ├── agent_dashboard.html     # Agent/Admin dashboard
│   ├── create_ticket.html       # Ticket creation form
│   └── view_ticket.html         # Ticket details view
└── README.md           # This file
```

## Usage

1. **Registration**: Create new user or agent accounts
2. **Login**: Use credentials to access role-specific dashboards
3. **Create Tickets** (Users): Submit support requests with subject and description
4. **Manage Tickets** (Agents/Admin): View all tickets and update their status
5. **Track Progress**: Monitor ticket status from Open to Resolved

## Database

The application uses SQLite for local development. The database file (`tickets.db`) is created automatically when you first run the application.

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, Bootstrap 5 (Dark Theme), Feather Icons
- **Authentication**: Werkzeug password hashing

## Development

To run in development mode:
```bash
python main.py
```

The application will run on `http://localhost:5000` with debug mode enabled.