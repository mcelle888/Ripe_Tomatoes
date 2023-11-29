from main import db

class Actor(db.Model):
    __tablename__= "actors"
    id = db.Column(db.Integer,primary_key=True)  
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    gender = db.Column(db.String())
    country = db.Column(db.String())
