from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Ticket

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            if user.is_user():
                return redirect(url_for('user_dashboard'))
            elif user.is_agent() or user.is_admin():
                return redirect(url_for('agent_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on role
            if user.is_user():
                return redirect(url_for('user_dashboard'))
            elif user.is_agent() or user.is_admin():
                return redirect(url_for('agent_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Validate role (only user and agent allowed for registration)
        if role not in ['user', 'agent']:
            flash('Invalid role selected', 'error')
            return render_template('register.html')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_user():
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Get user's tickets
    tickets = Ticket.query.filter_by(user_id=user.id).order_by(Ticket.created_at.desc()).all()
    
    return render_template('user_dashboard.html', user=user, tickets=tickets)

@app.route('/agent/dashboard')
def agent_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not (user.is_agent() or user.is_admin()):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Get all tickets for agents/admin
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    
    return render_template('agent_dashboard.html', user=user, tickets=tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_user():
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']
        
        if not subject or not description:
            flash('Subject and description are required', 'error')
            return render_template('create_ticket.html')
        
        ticket = Ticket(
            subject=subject,
            description=description,
            user_id=user.id
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('create_ticket.html')

@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Users can only view their own tickets
    if user.is_user() and ticket.user_id != user.id:
        flash('Access denied', 'error')
        return redirect(url_for('user_dashboard'))
    
    return render_template('view_ticket.html', ticket=ticket, user=user)

@app.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
def update_ticket_status(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not (user.is_agent() or user.is_admin()):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form['status']
    
    # Validate status
    if new_status not in ['Open', 'In Progress', 'Resolved']:
        flash('Invalid status', 'error')
        return redirect(url_for('view_ticket', ticket_id=ticket_id))
    
    ticket.status = new_status
    db.session.commit()
    
    flash(f'Ticket status updated to {new_status}', 'success')
    return redirect(url_for('view_ticket', ticket_id=ticket_id))
