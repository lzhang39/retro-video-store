from app import db
from flask import current_app
from sqlalchemy import DateTime
from app.models.customer import Customer
from app.models.video import Video
from datetime import date, datetime, timedelta
# from sqlalchemy.orm import relationship, backref


class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.customer_id"), nullable=True)
    video_id = db.Column(
        db.Integer, db.ForeignKey("videos.video_id"), nullable=True)
    due_date = db.Column(
        db.DateTime, default=datetime.now() + timedelta(days=7))

    # video = db.relationship('Video', back_populates='customers')
    # customer = db.relationship('Customer', back_populates='videos')
