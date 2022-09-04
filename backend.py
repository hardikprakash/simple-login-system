from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

con = sqlite3.connect("main.db")
cursor=con.cursor()

@app.route('/')
def login():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name=request.form.get('name')
    age=request.form.get('age-group')
    flat=request.form.get('flat')
    email=request.form.get('email')
    username=request.form.get('username')
    psw=request.form.get('psw')

    cursor.execute("""INSERT INTO `users` (`Name`,`AgeGroup`,`FlatNumber`,`Email`,`Username`,`Password`) VALUES ('{}','{}',{},'{}','{}','{}');""".format(name,age,flat,email,username,psw))
    con.commit()

    return redirect('/')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    uid=request.form.get('login-uid')
    password=request.form.get('psw-login')

    cursor.execute("""SELECT * FROM `users` WHERE `Username` LIKE '{}' AND `Password` LIKE '{}';""".format(uid,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('profile.html', name=(users[0])[0], uname=(users[0])[4], email=(users[0])[3], flatno=(users[0])[2])
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)