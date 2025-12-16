from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import enum

db = SQLAlchemy()


class NewsCategory(enum.Enum):
    
    GENERAL = "general"
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    SCIENCE = "science"
    HEALTH = "health"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"
    
   
    PROTHOM_ALO = "prothom_alo" 
    DAILY_STAR = "daily_star"
    BBC_BENGALI = "bbc_bengali"

    @classmethod
    def list(cls):
        return [c.value for c in cls]

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True) 
    password = db.Column(db.String(80), nullable=False)
   
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    urlToImage = db.Column(db.String(255))
    source_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    published_at = db.Column(db.String(50))
    
    
    category = db.Column(db.String(50), default=NewsCategory.PROTHOM_ALO.value) 
    
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    article = db.relationship('Article')
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)