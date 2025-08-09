# JPOT - Interactive Quiz Platform 

A modern, responsive quiz application built with Flask that fetches questions from the Open Trivia Database API and features a beautiful glassmorphism design.

## 🔗 Live Demo

🚀 Deployed at: [[https://todo-render-2-yelb.onrender.com](https://todo-render-2-yelb.onrender.com)]

```
## Features

-  **Dynamic Questions**: Fetches questions from Open Trivia Database API
-  **Leaderboard System**: Track scores and compete with other players  
-  **Responsive Design**: Works perfectly on desktop, tablet, and mobile
-  **Modern UI**: Glassmorphism design with smooth animations
-  **Database Integration**: SQLite database for user scores and quiz history
-  **Fallback Questions**: Built-in questions if API is unavailable
-  **Real-time Progress**: Live progress tracking during quiz

## Project Structure

```
jpot-quiz/
├── app.py                 
├── requirements.txt       
├── Quiz.db               
├── templates/
│   ├── base.html         
│   ├── home.html        
│   ├── quiz.html        
│   ├── question.html     
│   ├── result.html       
│   └── leaderboard.html  
└── static/              
```

## Installation & Setup

### 1. Clone or Download the Project
```bash
# Create project directory
mkdir jpot-quiz
cd jpot-quiz
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv quiz_env

# Activate virtual environment
# On Windows:
quiz_env\Scripts\activate
# On macOS/Linux:
source quiz_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

## Database Schema

### User Table
- `id`: Primary key (Integer)
- `username`: User's display name (String, Unique)
- `total_score`: Cumulative score across all quizzes (Integer)
- `quizzes_taken`: Number of quizzes completed (Integer)
- `last_played`: Last quiz date (DateTime)

### QuizSession Table
- `id`: Primary key (Integer)
- `user_id`: Foreign key to User table (Integer)
- `score`: Score for this quiz session (Integer)
- `total_questions`: Number of questions in this session (Integer)
- `created_at`: Session timestamp (DateTime)

## API Integration

### Open Trivia Database
- **Base URL**: `https://opentdb.com/api.php`
- **Parameters**:
  - `amount`: Number of questions (default: 5)
  - `type`: Question type (multiple choice)
  - `encode`: URL encoding for special characters

### Fallback System
If the API is unavailable, the system uses built-in questions covering:
- Geography
- Science
- History
- Art
- General Knowledge


## Configuration

### Database Configuration
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```

### Quiz Settings
- **Default Questions**: 5 per quiz
- **Question Types**: Multiple choice only
- **Score Calculation**: 1 point per correct answer
- **Session Management**: Flask sessions for quiz state

## Customization

### Adding Custom Questions
Edit the `get_fallback_questions()` method in `app.py`:

```python
def get_fallback_questions():
    return [
        {
            'question': 'Your custom question?',
            'correct_answer': 'Correct Answer',
            'options': ['Option 1', 'Option 2', 'Correct Answer', 'Option 4'],
            'category': 'Custom Category',
            'difficulty': 'medium'
        },
        # Add more questions...
    ]
```

### Changing Quiz Settings
Modify these variables in the quiz routes:
- Number of questions: Change `amount=5` in `QuizAPI.get_questions()`
- Difficulty levels: Add `difficulty='easy'` parameter
- Categories: Add `category=9` parameter (see API docs for category IDs)

### Styling Customization
The CSS uses CSS custom properties for easy theming:
- Primary colors: `#60a5fa`, `#a78bfa`, `#34d399`
- Background: Gradient from `#0f172a` to `#334155`
- Glassmorphism: `backdrop-filter: blur(20px)`



### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=sqlite:///Quiz.db
FLASK_ENV=production
```


**API not working**:
- Check internet connection
- The app will automatically use fallback questions
- Verify API is accessible: `https://opentdb.com/api.php?amount=1&type=multiple`



## Features Overview

###  Home Page
- Modern landing page with animated elements
- Feature showcase and statistics
- Call-to-action buttons for quiz and leaderboard

###  Quiz System
- User name input with validation
- Dynamic question loading from API
- Progress tracking with visual indicators
- Real-time answer validation

###  Leaderboard
- Top 3 podium display with special styling
- Complete rankings table with user statistics
- Auto-refresh functionality
- Responsive design for mobile

### Results Page
- Detailed score breakdown
- Performance categorization (Excellent, Good, etc.)
- Celebration animations for high scores
- Quick action buttons for retaking quiz

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Credits

- **Questions**: [Open Trivia Database](https://opentdb.com/)
- **Design**: Modern glassmorphism with Inter font family
- **Icons**: Unicode emojis for universal compatibility
- **Framework**: Flask with SQLAlchemy and Jinja2

---

