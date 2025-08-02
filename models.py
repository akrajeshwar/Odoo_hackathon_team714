from app import db
from datetime import datetime
from werkzeug.security import check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user, agent, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with tickets
    tickets = db.relationship('Ticket', backref='creator', lazy=True)
    
    def __init__(self, username, email, password_hash, role='user'):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_user(self):
        return self.role == 'user'
    
    def is_agent(self):
        return self.role == 'agent'
    
    def is_admin(self):
        return self.role == 'admin'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')  # Open, In Progress, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, subject, description, user_id, status='Open'):
        self.subject = subject
        self.description = description
        self.user_id = user_id
        self.status = status
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.subject}>'
