from datetime import date
from sqlalchemy import (Column, Integer, String, Boolean, Text, Date, 
                        ForeignKey, create_engine)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from hashlib import sha256

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)

accesses = ["User", "VIP", "Moderator", "Admin", "Super-admin"]
accesses_id = {}
for i in range(len(accesses)):
    accesses_id[accesses[i]] = i

class AccountExists(Exception):
    '''
    Authentification pair already in db
    '''

class AccountNotFound(Exception):
    '''
    Authentification pair not found in db
    '''

class Abstract:
    id = Column(Integer, primary_key=True)
    created_on = Column(Date, default=date.today())


class User(Abstract, Base):
    __tablename__ = 'users'
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    hash_password = Column(String(64))
    access = Column(String(60), default='User')
    access_id = Column(Integer, default=accesses_id['User'])

    tasks = relationship("Task", cascade="all, delete-orphan")

    def __str__(self):
        return ' | '.join([self.id, self.username, self.email, self.password, self.hash_password])


class Task(Abstract, Base):
    __tablename__ = 'tasks'
    title = Column(String(20), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    details = Column(Text)
    deadline = Column(Date)
    status = Column(Boolean, default=0)
    author = relationship(User)

    def __str__(self):
        return ' | '.join([self.id, self.title, self.status])

# Base.metadata.create_all()

def add_user(name, email, password, access=None):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)

    hash_password=sha256(password.encode('utf-8')).hexdigest()

    if access:
        user = User(username=name, email=email, password=password, hash_password=hash_password, access=access, access_id=accesses_id[access])
    else:
        user = User(username=name, email=email, password=password, hash_password=hash_password)
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        raise AccountExists
    finally:
        session.close()

def remove_user(name):
    # def remove_user_task(username, id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    session.delete(user)
    session.commit()
    session.close()

def check_user(email, password):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    hash_password=sha256(password.encode('utf-8')).hexdigest()
    user = session.query(User).filter_by(email=email, 
                                         hash_password=hash_password).first()
    
    session.close()

    if not user:
        raise AccountNotFound

    return user.username

def get_user_info(name):

    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    if user != None:
        user_info = {
                    "id": user.id, 
                    "name": user.username, 
                    "email": user.email, 
                    "password": user.password, 
                    "access": user.access,
                    "access_id": user.access_id
                    }
        session.close()

        return user_info
    session.close()
    return None

def change_access(name, new_access):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    session.query(User).filter_by(username=name).update({'access': new_access, 'access_id': accesses_id[new_access]})
    user = session.query(User).filter_by(username=name).first()
    name = user.username
    access = user.access
    session.commit()
    session.close()

    return f'User {name} now has {access} access level'

def get_users_list():

    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user_list = session.query(User).all()
    session.close()
    
    return user_list

def get_user_tasks(name):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    if user:
        user_tasks = user.tasks
        session.close()

        return user_tasks
    session.close()
    return None


def create_user_task(author_id, title, details='', deadline=None):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).get(author_id)
    user_tasks = user.tasks
    new_task = Task(title=title, details=details, deadline=deadline)
    user_tasks.append(new_task)
    session.commit()
    session.close()


def change_user_task(username, id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=username).first()
    user_tasks = user.tasks
    task_to_change = user_tasks[id-1]
    task_to_change.status = not(task_to_change.status)
    session.commit()
    session.close()

def remove_user_task(username, id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=username).first()
    task_to_remove = user.tasks[id-1]
    session.delete(task_to_remove)
    session.commit()
    session.close()

def update_password(email, new_password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    hash_password = sha256(new_password.encode('utf-8')).hexdigest()
    session.query(User).filter_by(email=email).update({'password': new_password, 'hash_password': hash_password})
    session.commit()
    session.close()