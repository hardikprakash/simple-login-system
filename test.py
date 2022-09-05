import sqlite3
con = sqlite3.connect("simple-login-system/main.db")
cursor=con.cursor()
con.commit()