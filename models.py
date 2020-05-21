"""Models for r13 resource"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to Database """

    db.app = app
    db.init_app(app)


class Lecture(db.Model):
    """ Lecture """

    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)


class Exercise(db.Model):
    """ Exercise """

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)


class GitUser(db.Model):
    """ GitHub Users """

    __tablename__ = 'gitusers'

    repos = db.relationship('GitRepo')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.Text, nullable=False)
    owner_url = db.Column(db.Text, nullable=False)
    owner_avatar = db.Column(db.Text, nullable=False)


class GitRepo(db.Model):
    """ GitHub Repos """

    __tablename__ = 'gitrepos'

    user = db.relationship('GitUser')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.Text, nullable=False)
    repo_url = db.Column(db.Text, nullable=False)
    repo_push = db.Column(db.Text, nullable=False)
    repo_commit = db.Column(db.Text, nullable=False)
    repo_owner = db.Column(db.Integer, db.ForeignKey('gitusers.id'))


class Resource(db.Model):
    """ Additional Resources """

    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)


class Timestamp(db.Model):
    """ Additional Resources """

    __tablename__ = 'timestamp'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Text, nullable=False)


class LocalUser(db.Model):
    """ Local user database """

    __table_name__ = 'local_user2'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    localuser = db.Column(db.Text, nullable=False)
