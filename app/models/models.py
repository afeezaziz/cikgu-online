from flask_login import UserMixin
from datetime import datetime
import enum
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(200))
    role = db.Column(db.String(20), default='student')  # student, teacher, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')
    uploads = db.relationship('Upload', backref='user', lazy=True, cascade='all, delete-orphan')
    study_sessions = db.relationship('StudySession', backref='user', lazy=True, cascade='all, delete-orphan')
    push_subscriptions = db.relationship('PushSubscription', backref='user', lazy=True, cascade='all, delete-orphan')
    assessment_attempts = db.relationship('AssessmentAttempt', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float, default=0.0)
    time_spent = db.Column(db.Integer, default=0)  # in minutes
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Progress {self.user_id} - {self.subject}>'

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Upload {self.original_filename}>'

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    topics_covered = db.Column(db.Text)
    notes = db.Column(db.Text)
    session_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StudySession {self.user_id} - {self.subject}>'

class PushSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    endpoint = db.Column(db.Text, nullable=False)
    p256dh_key = db.Column(db.Text, nullable=False)
    auth_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<PushSubscription {self.user_id}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(10), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='subject', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=1)
    estimated_time = db.Column(db.Integer, default=30)  # in minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sections = db.relationship('Section', backref='chapter', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='chapter', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Chapter {self.title}>'

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    key_points = db.Column(db.Text)  # JSON format
    examples = db.Column(db.Text)    # JSON format
    order = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Section {self.title}>'

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = 'multiple_choice'
    SHORT_ANSWER = 'short_answer'
    ESSAY = 'essay'
    TRUE_FALSE = 'true_false'

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    time_limit = db.Column(db.Integer, default=30)  # in minutes
    total_marks = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    questions = db.relationship('Question', backref='assessment', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('AssessmentAttempt', backref='assessment', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Assessment {self.title}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)  # JSON format for multiple choice
    correct_answer = db.Column(db.Text)
    explanation = db.Column(db.Text)
    marks = db.Column(db.Integer, default=1)
    order = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question {self.id}>'

class AssessmentAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    total_marks = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0)
    time_taken = db.Column(db.Integer, default=0)  # in seconds
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, submitted
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<AssessmentAttempt {self.id}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessment_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    marks_obtained = db.Column(db.Float, default=0)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Answer {self.id}>'