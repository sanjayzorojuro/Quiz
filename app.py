from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


if __name__ == '__main__':
    app.run(debug=True)
