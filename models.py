from manage import db, app

class Shooting(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(64), index=True, unique=True)
    count = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime, index=True)
    lasttweet = db.Column(db.BigInteger, index = True, unique = True)
    initialtweet = db.Column(db.BigInteger, index=True, unique = True)
    backwards = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Event %r>' % (self.place)
