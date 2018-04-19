import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user, get_all_quotes, create_quote, delete_quote
import db.data_layer as db
'''
USAGE:        db.<function_name>
EXAMPLES:     db.search_by_user_or_email('Smith')
              db.search_by_user_or_email('gmail.com')
'''

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

@app.route('/')
def index():
    db_quotes = db.get_all_quotes()
    return render_template('index.html', quotes = db_quotes)

@app.route('/create_quote', methods=['POST'])
def create_quote():
    user_id = session['user_id']
    content = request.form['html_content']
    quote = db.create_quote(user_id, content)
    return redirect(url_for('index'))

@app.route('/delete/<quote_id>')
def delete_a_quote(quote_id):
    db.delete_quote(quote_id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    return redirect(url_for('search_users', query=request.args['html_query']))
    
@app.route('/results/<query>')
def search_users(query):
    pass

@app.route('/user/<user_id>')
def user_quotes(user_id):
    pass

def setup_web_session(user):
    pass

@app.route('/authenticate')
def authenticate():
    return render_template('authenticate.html')

@app.route('/login', methods = ['POST'])
def login():
    
    try:
        user = get_user_by_email(request.form['html_email'])
        if user.password == request.form['html_password']:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
    except:
        raise    

    flash('Invalid login')
    return redirect(url_for('authenticate'))

@app.route('/register', methods = ['POST'])
def register():
    email = request.form['html_email']
    username = request.form['html_username']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    is_valid = True

    if is_empty('email', request.form):
        is_valid = False
    
    if is_empty('username', request.form):
        is_valid = False
    
    if is_empty('password', request.form):
        is_valid = False

    if password != confirm:
        flash('passwords do not match')
        is_valid = False

    if is_valid == False:
        return redirect(url_for('authenticate'))

    user = create_user(email, username, password)
    session['user_id'] = user.id
    session['username'] = user.username

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def is_empty(field, form):
    key = 'html_{}'.format(field)
    value = form[key]
    empty = False
    if not len(value) > 0:
        empty = True
        flash('{} is empty'.format(field))
    return empty

app.run(debug=True)