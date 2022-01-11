import json
import os
from db import db
from db import Task
from flask import Flask
from flask import request
from flask_migrate import Migrate

app = Flask(__name__)
db_name = "one-three-seven"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

ENV = os.environ.get("ENV", "prod")
if ENV == 'dev':
    app.debug = True
    db_filepath = f"postgresql://postgres:@localhost/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_filepath
else:
    app.debug = False
    db_filepath = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_filepath


db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# generalized response formats


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.before_request
def before_request():
    try:
        json.loads(request.data)
    except json.JSONDecodeError:
        return failure_response("Invalid JSON")


# -- TASK ROUTES ---------------------------------------------------
@app.route("/")
def hello_world():
    return success_response('Hello World')

# Get all tasks
@app.route("/api/tasks/")
def get_tasks():
    return success_response([t.serialize() for t in Task.query.all()])


# Add new task
@app.route("/api/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    title = body.get('title')
    column_name = body.get('column_name')
    if column_name not in ['one', 'three', 'seven']:
        return failure_response('Invalid field column_name', 400)
    if title is None:
        return failure_response("Title is required", 400)
    new_task = Task(title=title, column_name=column_name)
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)

# Update task
@app.route("/api/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found", 404)
    body = json.loads(request.data)
    title = body.get('title')
    column_name = body.get('column_name')
    done = body.get('done')
    if column_name is not None:
        if column_name not in ['one', 'three', 'seven']:
            return failure_response("Invalid field column_name, must be 'one', 'three', or 'seven'", 400)
        else:
            task.column_name = column_name
    if done is not None:
        if not isinstance(done, bool):
            return failure_response('Invalid field done, must be boolean', 400)
        else:
            task.done = done
    if title is not None:
        task.title = title
    db.session.commit()
    return success_response(task.serialize())

# Get task
@app.route("/api/tasks/<int:task_id>/")
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found', 404)
    return success_response(task.serialize())


# Delete task
@app.route("/api/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found!')
    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
