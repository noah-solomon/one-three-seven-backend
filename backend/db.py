from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=None)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.done = kwargs.get('done', False)
        self.create_date = datetime.now()

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'create_date': str(self.create_date) if self.create_date else None
        }
