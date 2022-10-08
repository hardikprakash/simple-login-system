from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

con = sqlite3.connect("D:/gitrepos/simple-login-system/main.db", check_same_thread=False)
cursor = con.cursor()


@app.route('/')
def login():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    name = str(request.form.get('name'))
    email = str(request.form.get('email'))
    username = str(request.form.get('username'))
    psw = str(request.form.get('psw'))

    try:
        cursor.execute("""INSERT INTO users (Name, Email, Username, Password) VALUES('{}', '{}', '{}', '{}');""".format(name, email, username, psw))
    except:
        print("An Error Occurred, Fields mayn't be unique/correct; Try different values.")
    return redirect('/')


@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    uid = request.form.get('login-uid')
    password = request.form.get('psw-login')

    cursor.execute(
        """SELECT * FROM users WHERE Username LIKE '{}' AND Password LIKE '{}';""".format(uid, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = (users[0])[2]
        return render_template('profile.html', name=(users[0])[0], uname=(users[0])[2], email=(users[0])[1])

    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
