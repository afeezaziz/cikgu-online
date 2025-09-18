#!/usr/bin/env python3
"""
Database initialization script for Cikgu application
Creates all database tables and initializes with sample data
"""

import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from models import db, User, Subject, Chapter, Section, Assessment, Question
from hello import app

def init_database():
    """Initialize database with all tables and sample data"""

    print("Initializing database...")

    # Create all tables
    with app.app_context():
        db.create_all()
        print("✓ All database tables created successfully")

        # Check if we need to add sample subjects
        if Subject.query.count() == 0:
            print("Adding sample subjects...")

            # Sample subjects for SPM
            subjects = [
                {
                    'name': 'Biologi',
                    'code': 'BIO',
                    'description': 'Kajian tentang hidupan dan organisma hidup'
                },
                {
                    'name': 'Kimia',
                    'code': 'KIM',
                    'description': 'Kajian tentang jirim, sifat, dan tindak balas kimia'
                },
                {
                    'name': 'Fizik',
                    'code': 'FIZ',
                    'description': 'Kajian tentang jirim, tenaga, dan daya'
                },
                {
                    'name': 'Matematik',
                    'code': 'MAT',
                    'description': 'Kajian tentang nombor, bentuk, dan ruang'
                },
                {
                    'name': 'Bahasa Melayu',
                    'code': 'BM',
                    'description': 'Penguasaan bahasa Melayu dan sastera'
                },
                {
                    'name': 'English',
                    'code': 'EN',
                    'description': 'English language proficiency and literature'
                }
            ]

            for subject_data in subjects:
                subject = Subject(**subject_data)
                db.session.add(subject)

            db.session.commit()
            print(f"✓ Added {len(subjects)} sample subjects")

            # Add sample chapters for Biology
            biology_subject = Subject.query.filter_by(name='Biologi').first()
            if biology_subject:
                chapters = [
                    {
                        'subject_id': biology_subject.id,
                        'title': 'Pengenalan kepada Biologi',
                        'description': 'Asas-asas biologi dan konsep penting dalam sains hidup',
                        'content': 'Biologi adalah kajian tentang hidupan dan organisma hidup.',
                        'order': 1,
                        'estimated_time': 45
                    },
                    {
                        'subject_id': biology_subject.id,
                        'title': 'Sel dan Struktur Sel',
                        'description': 'Struktur dan fungsi sel sebagai unit asas kehidupan',
                        'content': 'Sel adalah unit asas semua organisma hidup.',
                        'order': 2,
                        'estimated_time': 60
                    },
                    {
                        'subject_id': biology_subject.id,
                        'title': 'Biologi Molekul',
                        'description': 'Struktur dan fungsi molekul dalam biologi',
                        'content': 'Biologi molekul mengkaji biologi pada peringkat molekul.',
                        'order': 3,
                        'estimated_time': 90
                    }
                ]

                for chapter_data in chapters:
                    chapter = Chapter(**chapter_data)
                    db.session.add(chapter)

                db.session.commit()
                print(f"✓ Added {len(chapters)} sample chapters for Biology")

                # Add sample sections for first chapter
                first_chapter = Chapter.query.filter_by(subject_id=biology_subject.id, order=1).first()
                if first_chapter:
                    sections = [
                        {
                            'chapter_id': first_chapter.id,
                            'title': 'Definisi Biologi',
                            'content': '<p>Biologi adalah kajian tentang hidupan dan organisma hidup. Ia merangkumi pelbagai aspek kehidupan dari peringkat molekul hingga ekosistem.</p>',
                            'key_points': '["Biologi berasal dari perkataan Greek", "Merupakan sains yang mengkaji organisma hidup", "Meliputi pelbagai bidang seperti botani, zoologi, dan genetik"]',
                            'order': 1
                        },
                        {
                            'chapter_id': first_chapter.id,
                            'title': 'Ciri-ciri Hidupan',
                            'content': '<p>Semua organisma hidup mempunyai ciri-ciri tertentu yang membezakannya daripada benda bukan hidup.</p>',
                            'key_points': '["Organisma hidup memerlukan makanan dan tenaga", "Berupaya membesar dan berkembang", "Boleh membiak dan bertindak balas terhadap rangsangan"]',
                            'order': 2
                        }
                    ]

                    for section_data in sections:
                        section = Section(**section_data)
                        db.session.add(section)

                    db.session.commit()
                    print(f"✓ Added {len(sections)} sample sections")

        print("\n🎉 Database initialization completed successfully!")
        print("\nDatabase tables created:")
        tables = [
            'User', 'Subject', 'Chapter', 'Section', 'Assessment', 'Question',
            'Progress', 'Upload', 'StudySession', 'PushSubscription',
            'AssessmentAttempt', 'Answer'
        ]
        for table in tables:
            print(f"  ✓ {table}")

if __name__ == '__main__':
    init_database()