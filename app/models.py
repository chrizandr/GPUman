"""Models for Hydra Classes."""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from passlib.hash import bcrypt
import datetime
from sqlalchemy.orm import sessionmaker
from settings import DB_URL
import pdb

engine = create_engine(DB_URL)

Base = declarative_base()


class User(Base):
    """Model for Users.

    Each user has a username and password that matches with their ubuntu login IDs.
    """

    __tablename__ = "users"

    id_ = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))
    name = Column(String(20))
    email = Column(String(20), unique=True)
    faculty = Column(String(20))

    def __init__(self, username, password, name, email, faculty):
        """Create new instance."""
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.name = name
        self.email = email
        self.faculty = faculty

    def validate_password(self, password):
        """Check encrypted password."""
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', username='%s'>" % (self.id_, self.username)


class Admin(Base):
    """Model for Admins.

    Normal users can be given admin access to modify exisitng users and manage the server.
    """

    __tablename__ = "admins"

    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id_"), unique=True)

    def __repr__(self):
        """Verbose object name."""
        return "<userid='%s'>" % (self.user_id)


class UsageRequest(Base):
    """Model for GPU usage requests.

    Each user needs to request usage time for the server.
    """

    __tablename__ = "requests"

    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id_"))
    usage_time = Column(Integer)
    timestamp = Column(DateTime)
    status = Column(String(20))

    def __init__(self, user_id, usage_time):
        """Create new instance."""
        self.user_id = user_id
        self.usage_time = usage_time
        self.timestamp = datetime.datetime.now()
        self.status = "new"

    def __repr__(self):
        """Verbose object name."""
        return "<userid='%s', username='%s', timestamp='%s'>" % (self.user_id, self.usage_time, str(self.timestamp))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    test_user = User("test", "test", "test", "test@gmail.com", "test")
    session.add(test_user)
    session.commit()
    pdb.set_trace()
