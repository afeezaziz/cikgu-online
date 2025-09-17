from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
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

# Chapter and assessment routes
@app.route('/subjects/<subject>/chapter/<int:chapter>')
@login_required
def chapter(subject, chapter):
    # Sample chapter data - in a real app, this would come from a database
    chapter_data = {
        1: {
            'title': 'Pengenalan kepada Biologi',
            'description': 'Asas-asas biologi dan konsep penting dalam sains hidup',
            'estimated_time': 45,
            'sections': [
                {
                    'title': 'Definisi Biologi',
                    'content': '<p>Biologi adalah kajian tentang hidupan dan organisma hidup. Ia merangkumi pelbagai aspek kehidupan dari peringkat molekul hingga ekosistem.</p>',
                    'key_points': [
                        'Biologi berasal dari perkataan Greek "bios" (hidup) dan "logos" (kajian)',
                        'Merupakan sains yang mengkaji organisma hidup',
                        'Meliputi pelbagai bidang seperti botani, zoologi, dan genetik'
                    ],
                    'examples': [
                        {'question': 'Apakah definisi biologi?', 'answer': 'Kajian tentang hidupan dan organisma hidup'}
                    ]
                },
                {
                    'title': 'Ciri-ciri Hidupan',
                    'content': '<p>Semua organisma hidup mempunyai ciri-ciri tertentu yang membezakannya daripada benda bukan hidup.</p>',
                    'key_points': [
                        'Organisma hidup memerlukan makanan dan tenaga',
                        'Berupaya membesar dan berkembang',
                        'Boleh membiak dan bertindak balas terhadap rangsangan'
                    ],
                    'examples': [
                        {'question': 'Berikan 3 ciri hidupan', 'answer': 'Memerlukan makanan, boleh membiak, dan boleh bergerak'}
                    ]
                }
            ]
        }
    }

    data = chapter_data.get(chapter, chapter_data[1])

    return render_template('chapter.html',
                         subject=subject,
                         chapter_number=chapter,
                         chapter_title=data['title'],
                         chapter_description=data['description'],
                         estimated_time=data['estimated_time'],
                         sections=data['sections'],
                         progress_percentage=65,
                         completed_subtopics=1,
                         total_subtopics=2,
                         previous_chapter=chapter-1 if chapter > 1 else None,
                         next_chapter=chapter+1 if chapter < 5 else None)

@app.route('/subjects/<subject>/chapter/<int:chapter>/mcq')
@login_required
def mcq_assessment(subject, chapter):
    # Sample MCQ questions - in a real app, this would come from a database
    questions = [
        {
            'id': 1,
            'question': 'Apakah definisi biologi?',
            'options': [
                {'key': 'A', 'text': 'Kajian tentang batu dan mineral'},
                {'key': 'B', 'text': 'Kajian tentang hidupan dan organisma hidup'},
                {'key': 'C', 'text': 'Kajian tentang nombor dan persamaan'},
                {'key': 'D', 'text': 'Kajian tentang sejarah tamadun'}
            ],
            'explanation': 'Biologi berasal dari perkataan Greek "bios" (hidup) dan "logos" (kajian), yang membawa maksud kajian tentang hidupan dan organisma hidup.'
        },
        {
            'id': 2,
            'question': 'Manakah antara berikut BUKAN ciri hidupan?',
            'options': [
                {'key': 'A', 'text': 'Memerlukan makanan'},
                {'key': 'B', 'text': 'Boleh membiak'},
                {'key': 'C', 'text': 'Mempunyai nukleus'},
                {'key': 'D', 'text': 'Boleh bergerak'}
            ],
            'explanation': 'Mempunyai nukleus bukanlah ciri semua hidupan (contohnya, bakteria tidak mempunyai nukleus yang sebenar).'
        },
        {
            'id': 3,
            'question': 'Apakah perbezaan antara sel prokariotik dan eukariotik?',
            'options': [
                {'key': 'A', 'text': 'Saiz sel sahaja'},
                {'key': 'B', 'text': 'Kehadiran nukleus'},
                {'key': 'C', 'text': 'Jenis makanan'},
                {'key': 'D', 'text': 'Tempat tinggal'}
            ],
            'explanation': 'Perbezaan utama ialah sel eukariotik mempunyai nukleus yang sebenar manakala sel prokariotik tidak.'
        }
    ]

    return render_template('mcq_assessment.html',
                         subject=subject,
                         chapter=chapter,
                         questions=questions,
                         total_questions=len(questions),
                         time_limit=30)

@app.route('/subjects/<subject>/chapter/<int:chapter>/subjective')
@login_required
def subjective_assessment(subject, chapter):
    # Sample subjective questions - in a real app, this would come from a database
    essay_question = {
        'title': 'Kepentingan Biologi dalam Kehidupan Harian',
        'prompt': 'Huraikan bagaimana pengetahuan biologi dapat membantu kita dalam kehidupan harian. Berikan contoh-contoh yang relevan.',
        'marks': 30,
        'guidelines': [
            'Pastikan karangan anda mempunyai pengenalan, isi, dan kesimpulan',
            'Berikan sekurang-kurangnya 3 contoh aplikasi biologi dalam kehidupan harian',
            'Gunakan bahasa yang formal dan jelas',
            'Panjang karangan: 250-300 patah perkataan'
        ]
    }

    subjective_questions = [
        {
            'id': 1,
            'question': 'Terangkan mengapa air penting untuk organisma hidup.',
            'type': 'paragraph',
            'marks': 10,
            'min_words': 50,
            'max_words': 100,
            'tips': [
                'Fokus kepada fungsi air dalam badan',
                'Sebutkan proses-proses yang memerlukan air',
                'Berikan contoh kesan kekurangan air'
            ]
        },
        {
            'id': 2,
            'question': 'Apakah yang dimaksudkan dengan metabolisme? Berikan dua jenis metabolisme.',
            'type': 'short',
            'marks': 5
        },
        {
            'id': 3,
            'question': 'Bandingkan antara respirasi aerobik dan respirasi anaerobik.',
            'type': 'essay',
            'marks': 15,
            'min_words': 80,
            'max_words': 150,
            'context': 'Respirasi adalah proses penting dalam pengeluaran tenaga untuk organisma hidup.',
            'tips': [
                'Terangkan kedua-dua jenis respirasi',
                'Bandingkan dari segi penggunaan oksigen',
                'Nyatakan hasil setiap jenis respirasi',
                'Berikan contoh organisma yang menjalani setiap jenis'
            ]
        }
    ]

    return render_template('subjective_assessment.html',
                         subject=subject,
                         chapter=chapter,
                         essay_question=essay_question,
                         subjective_questions=subjective_questions,
                         total_questions=len(subjective_questions) + (1 if essay_question else 0),
                         time_limit=60)

# API routes for handling assessments
@app.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    data = request.json
    # In a real app, save progress to database
    return jsonify({'success': True, 'message': 'Progress saved'})

@app.route('/api/submit-mcq', methods=['POST'])
@login_required
def submit_mcq():
    data = request.json
    # In a real app, save MCQ results to database
    attempt_id = str(uuid.uuid4())
    return jsonify({'success': True, 'attempt_id': attempt_id})

@app.route('/api/submit-subjective', methods=['POST'])
@login_required
def submit_subjective():
    data = request.json
    # In a real app, save subjective answers to database
    attempt_id = str(uuid.uuid4())
    return jsonify({'success': True, 'attempt_id': attempt_id})

@app.route('/api/save-subjective-draft', methods=['POST'])
@login_required
def save_subjective_draft():
    data = request.json
    # In a real app, save draft to database
    return jsonify({'success': True})

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
