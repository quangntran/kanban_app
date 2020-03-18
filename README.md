# Kanban Board Web App

## Features

* Add task with title, description, and custom state (Todo, Doing, or Done)
* Entering title is mandatory
* Once a task is created, one can change its status to any other status
* One can delete a task on board
* If a column has no task, then it will indicate so

## Run the app
```console
python3.6 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app.py
flask run
```
Then go to http://127.0.0.1:5000/. If it says `OSError: [Errno 48] Address already in use`, then run:
```console
kill $(lsof -t -i:5000)
```

## Run unit test
In Terminal directly at `kanban_project`, run:
```console
python3 -m unittest discover test
```
