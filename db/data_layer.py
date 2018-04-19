from sqlalchemy import or_, and_
from db.base import DbManager
from db.entities import User, Quote

db = DbManager()

def get_all_quotes():
    return db.open().query(Quote).order_by(Quote.created_at.desc()).filter().all()

def get_all_quotes_for(user_id):
    pass

def search_by_user_or_email(query):
    return db.open().query(User).filter(or_(User.username.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    quote = Quote()
    quote.user_id = user_id
    quote.content = content
    return db.save(quote)

def delete_quote(quote_id):
    quote = db.open().query(Quote).filter(Quote.id == quote_id).one()
    return db.delete(quote)

def get_user_by_id(user_id):
    pass

def get_user_by_name(username):
    return db.open().query(User).filter(User.id == user_id).one()


def get_user_by_email(user_email):
    return db.open().query(User).filter(User.email == user_email).one()


def create_user(email, username, password):
    user = User()
    user.username = username
    user.email = email
    user.password = password
    return db.save(user)

