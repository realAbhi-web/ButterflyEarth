from flask import Flask, render_template, redirect, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
# from questions import add_words
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SECRET_KEY'] = 'y4rou3rjsalf1234_f9e'  # Change this to a random secret key
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

points=0
loop=0
level=1

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    username= db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

# Initialize app with extension
# db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

def add_words():
    # from models import Word  # Import here to avoid circular import
    words = [
    {'word': 'What is the largest planet in our solar system?', 'answer': 'Jupiter'},
    {'word': 'What is the closest planet to the Sun?', 'answer': 'Mercury'},
    {'word': 'Which planet is known as the Red Planet?', 'answer': 'Mars'},
    {'word': 'What is the name of the galaxy we live in?', 'answer': 'Milky Way'},
    {'word': 'What is the name of the first human to travel into space?', 'answer': 'Yuri Gagarin'},
    {'word': 'What is the name of Earth’s natural satellite?', 'answer': 'Moon'},
    {'word': 'Which planet has the most rings?', 'answer': 'Saturn'},
    {'word': 'What is the hottest planet in our solar system?', 'answer': 'Venus'},
    {'word': 'Which planet is known for its Great Red Spot?', 'answer': 'Jupiter'},
    {'word': 'What do we call a star explosion?', 'answer': 'Supernova'},
    # Add more space-related questions as needed
]


    for item in words:
        new_word = Word(word=item['word'], answer=item['answer'])
        db.session.add(new_word)
    db.session.commit()

# Only call this once
with app.app_context():
    add_words()

@app.route('/')
def home():
    points=0
    try:
        return render_template('home.html')
    except Exception as e:
        return f"Error rendering template: {e}"

@app.route('/game', methods=['GET', 'POST'])
# @app.route('/game methods=['GET', 'POST'])
def game():
    global points
    global loop
    if request.method == 'POST':
        # Handle the user's answer and game logic
        try:
            new_word = random.choice(Word.query.all())
            user_answer = request.form['answer']
            radio_answer=request.form.get('answer')
            # print(request.form['answer'])
            # print(request.form.get('answer2'))
            word_id = request.form['word_id']
            word = Word.query.get(word_id)
            # print(word)
            

            if not word:
                feedback = "Error: Word not found."
                return render_template('game.html', points=points, feedback=feedback)
            else:
                multiple_choices = [new_word.answer]
                # print(word.answer)
                while len(multiple_choices) < 4:
                    choice = random.choice(Word.query.all()).answer
                    # print(choice)
                    # print(new_word.answer)
                    # choice = new_word.answer
                    if choice not in multiple_choices:
                        multiple_choices.append(choice)

            # print(multiple_choices)
            # print(new_word.answer)
            loop=loop+1
            # print(loop)
            if loop == 10:
                return redirect('/level-complete')

            if user_answer.lower() == word.answer.lower() or radio_answer.lower()==word.answer.lower():
                feedback = "Correct!"
                points += 10
            else:
                feedback = f"Wrong! The correct answer is '{word.answer}'."
                points -= 5
            
            
            random.shuffle(multiple_choices)
            # print(user_answer)

            # for i in new_word:
                # print(i)
            # print(new_word.answer)
            return render_template('game.html', points=points, feedback=feedback, word=new_word, multiple_choices=multiple_choices)

        except Exception as e:
            feedback = f"An error occurred: {e}"
            return render_template('game.html', points=points, feedback=feedback,multiple_choices=[])

    # Get a random word to quiz the user
    
    word = random.choice(Word.query.all())
    return render_template('game.html', points=0, feedback="", word=word,multiple_choices=[])

# @app.route("/level-complete")
# def complete():
#     session['level'] = session.get('level', 1) + 1
#     return "<h1>Level Complete!<h1>"

@app.route("/register", methods=['GET','POST'])
def sign_in():

    data=request.get_json()
    username=data.get('email')
    password=data.get('password')

    user=User.query.filter_by(username=username).first()
    if user is None:
        database=User(username=username, password=password)
        db.session.add(database)
        db.session.commit()
        return "Your account has been created"

    if user.username==username:
        login_user(user)
        return f"You are signed in as {username}"
    
    if not username or not password:
        return "Both email and pasword are required"


if __name__ == '__main__':
    # print(word.answer)
    # print()
    app.run(debug=True)
