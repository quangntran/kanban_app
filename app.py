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
    todo = Task.query.filter_by(state='todo').all()
    doing = Task.query.filter_by(state='doing').all()
    done = Task.query.filter_by(state='done').all()
    # incomplete = Todo.query.filter_by(complete=False).all()
    # complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', todo=todo, doing=doing, done=done)

@app.route('/add', methods=['POST'])
def add():
    todo = Task(title=request.form['title'], description=request.form['description'], state=request.form['state'])
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_state/<id>/<state>', methods=['POST'])
def update_state(id,state):
    task = Task.query.filter_by(id=int(id)).first()
    task.state = str(state)
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/todo/<id>', methods=['POST'])
# def todo(id):
#     task = Task.query.filter_by(id=int(id)).first()
#     task.state = 'todo'
#     db.session.commit()
#
#     return redirect(url_for('index'))
#
# @app.route('/doing/<id>', methods=['POST'])
# def doing(id):
#     task = Task.query.filter_by(id=int(id)).first()
#     task.state = 'doing'
#     db.session.commit()
#     return redirect(url_for('index'))
#
# @app.route('/done/<id>', methods=['POST'])
# def done(id):
#     task = Task.query.filter_by(id=int(id)).first()
#     task.state = 'done'
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index'))

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
