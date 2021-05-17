from project import db


class User(db.Model):

    __tablename__ = 'humans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)

    def __init__(self, name, birthday):
        self.name = name.lower()
        self.birthday = birthday

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday.isoformat()
        }
