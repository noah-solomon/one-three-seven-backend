from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', '')
        self.title = kwargs.get('title', '')
        self.done = kwargs.get('done', False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }
