from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ideas.db'
db = SQLAlchemy(app)

# Define the Idea model
class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    request_type = db.Column(db.String(50), nullable=False)  # New field
    votes = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    ideas = Idea.query.all()
    return render_template('index.html', ideas=ideas)

@app.route('/submit', methods=['POST'])
def submit_idea():
    name = request.form.get('idea_name')
    text = request.form.get('idea_text')
    request_type = request.form.get('request_type')
    if name and text and request_type:
        idea = Idea(name=name, text=text, request_type=request_type)
        db.session.add(idea)
        db.session.commit()
    return redirect(url_for('thank_you'))

@app.route('/upvote/<int:idea_id>')
def upvote_idea(idea_id):
    idea = Idea.query.get(idea_id)
    if idea:
        idea.votes += 1
        db.session.commit()
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
