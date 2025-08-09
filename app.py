from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import requests
import random
import html
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key-here"  # Change this to a secure secret key
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    total_score = db.Column(db.Integer, default=0)
    quizzes_taken = db.Column(db.Integer, default=0)
    last_played = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def score(self):
        return self.total_score
    
    def add_quiz_result(self, score):
        self.total_score += score
        self.quizzes_taken += 1
        self.last_played = datetime.utcnow()
        db.session.commit()

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('quiz_sessions', lazy=True))

# Quiz API Integration
class QuizAPI:
    BASE_URL = "https://opentdb.com/api.php"
    
    @staticmethod
    def get_questions(amount=5, category=None, difficulty=None):
        """Fetch questions from Open Trivia Database API"""
        params = {
            'amount': amount,
            'type': 'multiple',
            'encode': 'url3986'  # URL encoding to handle special characters
        }
        
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
            
        try:
            response = requests.get(QuizAPI.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['response_code'] == 0:
                questions = []
                for q in data['results']:
                    # Decode URL-encoded strings
                    question = {
                        'question': requests.utils.unquote(q['question']),
                        'correct_answer': requests.utils.unquote(q['correct_answer']),
                        'incorrect_answers': [requests.utils.unquote(ans) for ans in q['incorrect_answers']],
                        'category': requests.utils.unquote(q['category']),
                        'difficulty': q['difficulty']
                    }
                    
                    # Create options list and shuffle
                    options = question['incorrect_answers'] + [question['correct_answer']]
                    random.shuffle(options)
                    question['options'] = options
                    
                    questions.append(question)
                
                return questions
            else:
                return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def get_fallback_questions():
        """Fallback questions if API fails"""
        return [
            {
                'question': 'What is the capital of France?',
                'correct_answer': 'Paris',
                'options': ['Berlin', 'Madrid', 'Paris', 'Rome'],
                'category': 'Geography',
                'difficulty': 'easy'
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'correct_answer': 'Mars',
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'category': 'Science',
                'difficulty': 'easy'
            },
            {
                'question': 'Who painted the Mona Lisa?',
                'correct_answer': 'Leonardo da Vinci',
                'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
                'category': 'Art',
                'difficulty': 'medium'
            },
            {
                'question': 'What is the largest mammal in the world?',
                'correct_answer': 'Blue Whale',
                'options': ['Elephant', 'Blue Whale', 'Giraffe', 'Hippopotamus'],
                'category': 'Science',
                'difficulty': 'easy'
            },
            {
                'question': 'Which year did World War II end?',
                'correct_answer': '1945',
                'options': ['1943', '1944', '1945', '1946'],
                'category': 'History',
                'difficulty': 'medium'
            }
        ]

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Handle quiz submission
        username = request.form.get('username')
        if not username:
            flash('Please enter your name to start the quiz!', 'error')
            return redirect(url_for('quiz'))
        
        # Store username in session and start quiz
        session['username'] = username
        session['current_question'] = 0
        session['score'] = 0
        
        # Get questions from API
        questions = QuizAPI.get_questions(amount=5)
        if not questions:
            questions = QuizAPI.get_fallback_questions()
        
        session['questions'] = questions
        return redirect(url_for('question'))
    
    # Check if quiz is in progress
    if 'questions' in session and session.get('current_question', 0) < len(session['questions']):
        return redirect(url_for('question'))
    
    return render_template('quiz.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'questions' not in session or 'username' not in session:
        return redirect(url_for('quiz'))
    
    questions = session['questions']
    current_q_index = session.get('current_question', 0)
    
    if current_q_index >= len(questions):
        return redirect(url_for('quiz_result'))
    
    if request.method == 'POST':
        # Handle answer submission
        selected_answer = request.form.get('answer')
        current_question = questions[current_q_index]
        
        # Check if answer is correct
        if selected_answer == current_question['correct_answer']:
            session['score'] += 1
        
        session['current_question'] = current_q_index + 1
        
        # Check if quiz is completed
        if session['current_question'] >= len(questions):
            return redirect(url_for('quiz_result'))
        else:
            return redirect(url_for('question'))
    
    # GET request - show current question
    current_question = questions[current_q_index]
    progress = ((current_q_index + 1) / len(questions)) * 100
    
    return render_template('question.html.jinja2', 
                         question=current_question, 
                         question_number=current_q_index + 1,
                         total_questions=len(questions),
                         progress=progress)

@app.route('/result')
def quiz_result():
    if 'score' not in session or 'username' not in session:
        return redirect(url_for('quiz'))
    
    score = session['score']
    total_questions = len(session.get('questions', []))
    username = session['username']
    
    # Save result to database
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    
    # Add quiz result
    user.add_quiz_result(score)
    
    # Create quiz session record
    quiz_session = QuizSession(user_id=user.id, score=score, total_questions=total_questions)
    db.session.add(quiz_session)
    db.session.commit()
    
    # Calculate percentage
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Clear session
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    session.pop('username', None)
    
    return render_template('result.html.jinja2', 
                         score=score, 
                         total=total_questions,
                         percentage=percentage,
                         username=username)

@app.route('/leaderboard')
def leaderboard():
    # Get top players ordered by score
    top_players = User.query.order_by(User.total_score.desc()).all()
    return render_template('leaderboard.html', leaderboard=top_players)

@app.route('/api/categories')
def get_categories():
    """API endpoint to get available quiz categories"""
    try:
        response = requests.get('https://opentdb.com/api_category.php', timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    
    # Fallback categories
    return {
        'trivia_categories': [
            {'id': 9, 'name': 'General Knowledge'},
            {'id': 17, 'name': 'Science & Nature'},
            {'id': 22, 'name': 'Geography'},
            {'id': 23, 'name': 'History'},
            {'id': 11, 'name': 'Entertainment: Film'},
        ]
    }

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database
# Remove the @app.before_first_request decorator and function
# Add this at the end of your file instead:

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    app.run(debug=False)
