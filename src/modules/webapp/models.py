from src.modules.webapp import db
class Users(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=50),nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)