from app import db
from flask import current_app
from sqlalchemy import DateTime


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    # # 'Task' looks at class in python and loads multiple of those (this is like a pseudo column)
    # tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory}