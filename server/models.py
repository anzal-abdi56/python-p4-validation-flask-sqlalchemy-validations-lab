from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    phone_number = db.Column(db.String(10), CheckConstraint('length(phone_number) = 10'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required for an author')
        return name

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String,CheckConstraint("length(summary)<=250"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (
        CheckConstraint("category IN ('Fiction', 'Non-Fiction')"),
        CheckConstraint("length(content) >= 250"),
        CheckConstraint("length(summary) <= 250")
    )

    @validates('title')
    def validate_title(self, key, title):
        forbidden_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if any(word not in title for word in forbidden_words):
            raise ValueError('Invalid title does not contain clickbait words')
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'