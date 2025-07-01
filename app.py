from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS soundscape_reviews (
                    id SERIAL PRIMARY KEY,
                    audio_file VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_session VARCHAR(255),
                    ip_address INET
                );
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully!")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")

# Sample audio data - replace with your actual audio files
AUDIO_FILES = [
    {"id": 1, "title": "Deep Relaxing Ambient Music", "filename": "test-DeepRelaxingAmbientMusic-100.wav"},
    {"id": 2, "title": "Forest Rain", "filename": "test-ForestBath-100.wav"},
    {"id": 3, "title": "Rain and Animal Sound", "filename": "test-RainSoundAndAnimalSound-100.wav"},
    {"id": 4, "title": "Soothing Soundscape For Deep Sleep", "filename": "test-SoothingSoundscapeForDeepSleepInsomniaRelief-100.wav"},
    {"id": 5, "title": "Stillness and Innerpeace", "filename": "test-StillnessAndInnerPeace100.wav"},
    # {"id": 6, "title": "Desert Wind and Sand", "filename": "desert_wind.mp3"},
    # {"id": 7, "title": "Jungle Sounds with Insects", "filename": "jungle_insects.mp3"},
    # {"id": 8, "title": "Snowfall in Pine Forest", "filename": "snow_forest.mp3"},
    # {"id": 9, "title": "Campfire Crackling", "filename": "campfire.mp3"},
    # {"id": 10, "title": "Underwater Bubbles", "filename": "underwater.mp3"}
]

@app.route('/')
def index():
    """Main page with audio files for review"""
    return render_template('index.html', audio_files=AUDIO_FILES)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Submit review for an audio file"""
    try:
        data = request.get_json()
        audio_file = data.get('audio_file')
        title = data.get('title')
        rating = int(data.get('rating'))
        
        # Validate rating
        if rating < 0 or rating > 5:
            return jsonify({'error': 'Rating must be between 0 and 5'}), 400
            
        # Get user info
        user_session = request.headers.get('User-Agent', 'unknown')[:255]
        ip_address = request.remote_addr
        
        # Insert into database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO soundscape_reviews (audio_file, title, rating, user_session, ip_address)
            VALUES (%s, %s, %s, %s, %s)
        ''', (audio_file, title, rating, user_session, ip_address))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Review submitted successfully!'}), 200
        
    except Exception as e:
        logging.error(f"Error submitting review: {e}")
        return jsonify({'error': 'Failed to submit review'}), 500

@app.route('/reviews')
def get_reviews():
    """Get all reviews (for admin purposes)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT audio_file, title, rating, created_at, ip_address
            FROM soundscape_reviews
            ORDER BY created_at DESC
        ''')
        
        reviews = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert datetime to string for JSON serialization
        for review in reviews:
            review['created_at'] = review['created_at'].isoformat()
            
        return jsonify(reviews), 200
        
    except Exception as e:
        logging.error(f"Error getting reviews: {e}")
        return jsonify({'error': 'Failed to get reviews'}), 500

@app.route('/stats')
def get_stats():
    """Get basic statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT 
                COUNT(*) as total_reviews,
                AVG(rating) as average_rating,
                audio_file,
                title,
                AVG(rating) as avg_rating,
                COUNT(*) as review_count
            FROM soundscape_reviews
            GROUP BY audio_file, title
            ORDER BY avg_rating DESC
        ''')
        
        stats = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logging.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)