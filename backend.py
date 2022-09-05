from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
import os
import datetime

app=Flask(__name__)
app.secret_key=os.urandom(24)

con = sqlite3.connect("simple-login-system/main.db")
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

    try:
        cursor.execute("""INSERT INTO `users` (`Name`,`AgeGroup`,`FlatNumber`,`Email`,`Username`,`Password`) VALUES('{}','{}','{}','{}','{}','{}');""".format(name,age,flat,email,username,psw))
        con.commit()
    except:
        print("An Error Ocurred, Fields mayn't be unique/correct; Try different values.")
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
        session['user_id']=(users[0])[0]
        UserFlat = int((users[0])[2])
        isSafe = "Yes"
        NearestFlat = "NULL"
        uplim = int(UserFlat) + 5
        downlim = int(UserFlat) - 5
        CurDate = (datetime.datetime.now()).strftime("%d%m%Y")
        CurDate = (CurDate[0])[0]
        CurDate = CurDate.date()
        cursor.execute("SELECT covid_details.FlatNumber, covid_details.Date FROM users,covid_details WHERE (covid_details.FlatNumber BETWEEN '{}' AND '{}') AND users.FlatNumber=covid_details.FlatNumber AND (IsPositive = 1);".format(downlim, uplim))
        PosFlats = cursor.fetchall()
        DangerFlats = []

        for i in PosFlats:
            if (datetime.datetime.strptime(i[1], "%d%m%Y") - datetime.datetime.strptime(CurDate, "%d%m%Y").days < 15) or (i[1] - CurDate).days > -15:
                DangerFlats.append(i[0])
        FlatStr = ""
        if len(DangerFlats) == 0:
            FlatStr = "None In Potential Range"
        if len(DangerFlats) == 1:
            FlatStr = str(DangerFlats[0])
        if len(DangerFlats) > 1:
            tempLen = (len(DangerFlats)) - 1
            i = 0
            while i < tempLen:
                FlatStr.append(str(DangerFlats[i]))
                FlatStr.append(", ")
                i = i + 1
            FlatStr.pop(-2)
            FlatStr.append("and", str(DangerFlats[-1]))
        if len(DangerFlats) > 0:
            isSafe = "No"
        
        return render_template('profile.html', name=(users[0])[0], uname=(users[0])[4], email=(users[0])[3], flatno=(users[0])[2], IsSafe=isSafe, FlatsStr=FlatStr)

    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)