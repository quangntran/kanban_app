from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    state = db.Column(db.String(200))

@app.route('/')
def index():
    todo = Task.query.filter_by(state='todo').all() # get all the todo tasks
    doing = Task.query.filter_by(state='doing').all()# get all the doing tasks
    done = Task.query.filter_by(state='done').all() # get all the done tasks
    # incomplete = Todo.query.filter_by(complete=False).all()
    # complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', todo=todo, doing=doing, done=done)

@app.route('/add', methods=['POST'])
def add():
    # create the task based on data
    task_to_add = Task(title=request.form['title'], description=request.form['description'], state=request.form['state'])
    # add task to db
    db.session.add(task_to_add)
    # commit the add
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_state/<id>/<state>', methods=['POST'])
def update_state(id,state):
    # get the task by id
    task = Task.query.filter_by(id=int(id)).first()
    # update the state
    task.state = str(state)
    # commit the update
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    # delete the task with the id
    Task.query.filter_by(id=int(id)).delete()
    # commit the change
    db.session.commit()
    return redirect(url_for('index'))

# create the db 
db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
