from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Initialize the Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)
# Create the database model
class TodoModel(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    ## This is the string representation of the class
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
# Create the database
with app.app_context():
    db.create_all() 

# *********************** End of Database Configuration ***********************#

## Home page Endpoint
@app.route('/',  methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['excerpt']
        todo = TodoModel(title=title, excerpt=desc)
        db.session.add(todo) # Add the todo to the database
        db.session.commit() # Commit the changes
    return render_template('index.html')

## Show DB Values
@app.route('/tasks', methods = ['GET', 'POST'])
def show():
    if request.method == "GET":
        allTodo = TodoModel.query.all()
    return render_template('details.html', allTodo = allTodo)


@app.route('/edit/<int:sno>', methods = ['GET','POST'])
def edit(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['excerpt']
        allTodo = TodoModel.query.filter_by(sno = sno).first()
        allTodo.title = title
        allTodo.excerpt = desc
        db.session.add(allTodo) # Add the todo to the database
        db.session.commit() # Commit the changes
        return redirect('/tasks')
    allTodo = TodoModel.query.filter_by(sno=sno).first()
    return render_template('edit.html', allTodo = allTodo)


@app.route('/delete/<int:sno>', methods = ['GET', 'POST'])
def delete(sno):
    allTodo = TodoModel.query.filter_by(sno = sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/show')




if __name__ == '__main__':
    app.run(debug=True, port="5000")
