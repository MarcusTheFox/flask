from flask import Flask, render_template, request, redirect, url_for, session
# from models import (add_user, check_user, get_user_tasks, change_user_task,
#                     remove_user_task, create_user_task, change_access)
from models import *
from mail_send import reset_password

from sqlalchemy.exc import IntegrityError
from models import AccountExists, AccountNotFound

app = Flask(__name__)
app.secret_key = 'themostsecuredpasswordinthewholeworld'



@app.errorhandler(404)
def error_page(error):
    if 'account' in session:
        name = session['account']
        return render_template('404.html', username=name)
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        if password != password_check:
            return render_template('index.html', error='passwords_dont_match')
        try:
            add_user(name, email, password)
        except AccountExists:
            return render_template('index.html', error='account_already_exists')
        session['account'] = name
        return redirect('/users/' + name)
    return render_template('index.html')

@app.route('/users/<name>')
def user_page(name):
    user_tasks = get_user_tasks(name)
    access_id = None
    if get_user_info(name) != None:
        access_id = get_user_info(name)["access_id"]
    return render_template('user.html', name=name, tasks=user_tasks, access_id=access_id)

@app.route('/admin/', methods=['GET', 'POST'])
def admin_panel():
    if 'account' in session:
        user_info = get_user_info(session['account'])
        if user_info["access_id"] >= 3:
            users_list = get_users_list()
            users_list = [(
                        users_list[i].username, 
                        users_list[i].access,
                        users_list[i].access_id
                        ) for i in range(len(users_list))]
            # print(users_list)
            if request.method == "POST":
                name = request.form.getlist('name')
                new_access = request.form.getlist('access')
                for i in range(len(name)):
                    access = change_access(name[i], new_access[i])
                    print("\n"+access+"\n")
                return redirect('/admin/')
            return render_template('admin_panel.html', users_list=users_list, 
                                                    username=session['account'], 
                                                    user_access=user_info["access_id"])
        else:
            return render_template('404.html', username=user_info["name"])
    return render_template('404.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            name = check_user(email, password)
        except AccountNotFound:
            return render_template('login.html', error=True)
        session['account'] = name
        return redirect('/users/' + name)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for('index'))

@app.route('/reset_password', methods=['GET', 'POST'])
def update_pw_form():
    if request.method == 'POST':
        if 'email' in request.form:
            session['email'] = request.form['email']
            session['secret_code'] = str(reset_password(session['email']))
            return render_template('reset_password.html', error=False, code='no_code')
        if 'code' in request.form:
            code = request.form['code']
            if session['secret_code'] == code:
                return render_template('reset_password.html', error=False, code='no_error')
            else:
                return render_template('reset_password.html', error=False, code='error')
        if 'password' in request.form:
            password = request.form['password']
            password_confirm = request.form['password_confirm']
            if password == password_confirm:
                update_password(session['email'], password)
                name = check_user(session['email'], password)
                session['email'], session['secret_code'] = None, None
                session['account'] = name
                return redirect('/users/' + name)
            else:
                return render_template('reset_password.html', error=False, code='no_error', confirm_password_error=True)
    return render_template('reset_password.html', error=True)

@app.route('/create_task/<task>')
def create_task(task):
    if 'account' in session:
        create_user_task(session['account'], task)
        return redirect(url_for('user_page', name=session['account']))
    return render_template('404.html')

@app.route('/status_task/<int:id>')
def change_status(id):
    if 'account' in session:
        change_user_task(session['account'], id)
        return redirect(url_for('user_page', name=session['account']))
    return render_template('404.html')

@app.route('/remove_task/<int:id>')
def remove_task(id):
    if 'account' in session:
        remove_user_task(session['account'], id)
        return {"message": "Task was deleted"}, 200
    return render_template('404.html')

@app.route('/remove_user/<name>')
def delete_user(name):
    if 'account' in session:
        user_info = get_user_info(session['account'])
        if user_info["access_id"] == 4:
            remove_user(name)
            return {"message": "User was deleted"}, 200
        else:
            return render_template('404.html', username=user_info["name"])
    return render_template('404.html')

@app.route('/edit_user/<name>')
def edit_settings_user(name):
    if 'account' in session:
        user_info = get_user_info(session['account'])
        if user_info["access_id"] == 4:
            user_edit = get_user_info(name)
            tasks = get_user_tasks(name)
            return render_template('edit_user.html', user_edit=user_edit, tasks=tasks)
        else:
            return render_template('404.html', username=user_info["name"])
    return render_template('404.html')
    

if __name__ == '__main__':
    app.run(debug=True)
