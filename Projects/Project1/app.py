from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

TodoTable = SQLAlchemy(app) 

class TodoDBModel(TodoTable.Model):
    sno = TodoTable.Column(TodoTable.Integer, primary_key = True)
    task = TodoTable.Column(TodoTable.String(200))
    excerpt = TodoTable.Column(TodoTable.String(500))
    date_created = TodoTable.Column(TodoTable.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.task}"

with app.app_context():
    TodoTable.create_all()

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_name = request.form['name']
        task_desc = request.form['excerpt']
        todo_task = TodoDBModel(task = task_name, excerpt = task_desc)
        TodoTable.session.add(todo_task)
        TodoTable.session.commit()
        print(task_name , task_desc)   
    return render_template('form.html')

@app.route('/show', methods = ['GET','POST'])
def display_task():
    if request.method == "GET":
        todo = TodoDBModel.query.all()
    return render_template('tasks.html', todo = todo)

# Delete Action

@app.route('/delete/<int:sno>', methods = ['GET','POST'])
def delete_task(sno):
    task = TodoDBModel.query.filter_by(sno = sno).first()
    TodoTable.session.delete(task)
    TodoTable.session.commit()
    return redirect('/show')

# Update Action
@app.route('/edit/<int:sno>', methods = ['GET', 'POST'])
def update_task(sno):
    if request.method == 'POST':
        task_name = request.form['name']
        task_desc = request.form['excerpt']
        todo = TodoDBModel.query.filter_by(sno=sno).first()
        todo.task = task_name
        todo.excerpt = task_desc
        TodoTable.session.add(todo)
        TodoTable.session.commit()
        return redirect('/show')
    todo = TodoDBModel.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)




if __name__ == '__main__':
    app.run(debug=True)