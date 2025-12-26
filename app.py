from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='Screens')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pathshala.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# --- ROUTE 1: JUST SHOW THE PAGE ---
@app.route('/')
def home():
    # Only FETCH data here. Do NOT use db.session.add or commit here.
    all_students = Student.query.all()
    return render_template('index.html', students=all_students)

# --- ROUTE 2: HANDLE THE FORM SUBMISSION ---
@app.route('/add_student', methods=['POST'])
def add_student():
    # This runs ONLY when you click the "Add Student" button
    name = request.form.get('u_name')
    email = request.form.get('u_email')

    if name and email: # Check to make sure they aren't empty
        new_student = Student(name=name, email=email)
        db.session.add(new_student)
        db.session.commit()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)