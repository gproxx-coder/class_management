from config import *

user_course = db.Table('user_course',
                       db.Column('user_id', db.ForeignKey('user_info.id'), primary_key=True),
                       db.Column('course_id', db.ForeignKey('course.id'), primary_key=True)
                       )

user_batch = db.Table('user_batch',
                      db.Column('user_id', db.ForeignKey('user_info.id'), primary_key=True),
                      db.Column('batch_id', db.ForeignKey('batch.id'), primary_key=True)
                      )


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    courses_list = db.relationship('Course', secondary=user_course,
                                   backref=db.backref('users_list', lazy=False))
    batches_list = db.relationship('Batch', secondary=user_batch,
                                   backref=db.backref('users_list', lazy=False))

    @classmethod
    def get_dummy(cls):
        return cls(id="", fname="", lname="", email="", contact="", city="", gender="", image="")

    def __repr__(self):
        # return '<User %r>' % self.username
        return f"\n{self.id} | {self.fname} {self.lname} | {self.email}"


class LoginInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.ForeignKey('user_info.id'), unique=True)
    user_status = db.Column(db.ForeignKey('user_status.id'), unique=False)
    user_role = db.Column(db.ForeignKey('role.id'), unique=False)
    userref = db.relationship("UserInfo", lazy=False, backref=db.backref('loginref', uselist=False))
    statusref = db.relationship("UserStatus", uselist=False, lazy=False, backref="userref")
    roleref = db.relationship("Role", uselist=False, lazy=False, backref="userref")

    @classmethod
    def get_dummy(cls):
        return cls(id="", username="", password="", user_id="", user_status="", user_role="")


class UserStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), nullable=False, unique=True)

    @classmethod
    def get_dummy(cls):
        return cls(id="", status="")


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False, unique=True)

    @classmethod
    def get_dummy(cls):
        return cls(id="", role="")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    fees = db.Column(db.Float)
    duration = db.Column(db.Integer)
    # batches_list = db.relationship("Batch", backref="courseref", uselist=True, lazy=False,)
    # batches_list = db.relationship("Batch", backref = ('voteinfo', uselist=False), uselist=True, lazy=False,)
    batches_list = db.relationship('Batch', backref=db.backref('courseref', lazy=False, uselist=True))

    @classmethod
    def get_dummy(cls):
        return cls(id="", name="", fees="", duration="")


class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bcode = db.Column(db.String(80), unique=True, nullable=False)
    start_date = db.Column(db.DateTime)
    course_id = db.Column(db.ForeignKey('course.id'), unique=False)


    @classmethod
    def get_dummy(cls):
        return cls(id="", bcode="", start_date="", course_id="")


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
