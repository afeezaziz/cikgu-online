from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from dotenv import load_dotenv
import os
from auth import google_auth, login_manager, create_or_update_user
from models import db, User, Progress, Upload, StudySession
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cikgu.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    auth_url = google_auth.get_auth_url()
    return render_template('login.html', auth_url=auth_url)

@app.route('/callback')
def callback():
    if 'code' not in request.args:
        flash('Authorization failed', 'error')
        return redirect(url_for('login'))

    try:
        # Get access token
        token_response = google_auth.get_token(request.args['code'])
        if 'error' in token_response:
            flash('Failed to get access token', 'error')
            return redirect(url_for('login'))

        # Get user info
        user_info = google_auth.get_user_info(token_response['access_token'])

        # Create or update user
        user = create_or_update_user(user_info)
        login_user(user)

        flash('Successfully logged in!', 'success')
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f'Login failed: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    total_study_time = db.session.query(db.func.sum(StudySession.duration)).filter_by(user_id=current_user.id).scalar() or 0
    completed_topics = Progress.query.filter_by(user_id=current_user.id, completed=True).count()
    total_uploads = Upload.query.filter_by(user_id=current_user.id).count()

    # Get recent activity
    recent_sessions = StudySession.query.filter_by(user_id=current_user.id).order_by(StudySession.session_date.desc()).limit(5).all()
    recent_uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.uploaded_at.desc()).limit(5).all()

    # Get progress by subject
    progress_by_subject = db.session.query(
        Progress.subject,
        db.func.count(Progress.id).label('total_topics'),
        db.func.sum(db.cast(Progress.completed, db.Integer)).label('completed_topics')
    ).filter_by(user_id=current_user.id).group_by(Progress.subject).all()

    return render_template('dashboard.html',
                         total_study_time=total_study_time,
                         completed_topics=completed_topics,
                         total_uploads=total_uploads,
                         recent_sessions=recent_sessions,
                         recent_uploads=recent_uploads,
                         progress_by_subject=progress_by_subject)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"

            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Get file size
            file_size = os.path.getsize(file_path)

            # Create upload record
            upload = Upload(
                user_id=current_user.id,
                filename=unique_filename,
                original_filename=filename,
                file_type=filename.rsplit('.', 1)[1].lower(),
                file_size=file_size,
                subject=request.form.get('subject', 'General')
            )

            db.session.add(upload)
            db.session.commit()

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('upload.html')

@app.route('/progress')
@login_required
def progress():
    user_progress = Progress.query.filter_by(user_id=current_user.id).all()
    return render_template('progress.html', progress=user_progress)

@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

@app.route('/subjects/<subject>')
def subject_detail(subject):
    return render_template('subject_detail.html', subject=subject)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
