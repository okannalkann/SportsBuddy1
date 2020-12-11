from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
import mysql.connector
from flask_mysqldb import MySQL
from database import Database

app = Flask(__name__)
app.secret_key = "SportBuddy"
db = Database("127.0.0.1", 3306, "root", "qwerty123456", "mydb")
db.con.cursor()    

@app.route('/', methods=['GET','POST'])
def home_page():
    try:
        if 'user' in session:
            username = session['user']
            return render_template('home.html',username=username)
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("hata")
    

@app.route('/sports', methods=['GET','POST'])
def sports():
    try:
        if 'user' in session:
            username = session['user'] 
            if request.method =="GET": #return values for button      
                query = "SELECT * FROM mydb.sports"
                db.cursor.execute(query)
                myresult = db.cursor.fetchall()
                return render_template('sports.html',len=len(myresult),data=myresult,username=username)

        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Sport Sayfa hatası")

@app.route('/sports/<int:sport_id>', methods=['GET','POST'])
def index(sport_id):
    try:
        if 'user' in session:
            username = session['user']
            if request.method == "GET": #return values for button 
                query =""" 
                    SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_sports ON mydb.users.user_id = mydb.user_want_to_play_sports.Users_user_id
                    LEFT JOIN mydb.sports ON mydb.user_want_to_play_sports.Sports_sport_id  = sports.sport_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.sports.sport_id = """
                db.cursor.execute(query + str(sport_id))
                myresult = db.cursor.fetchall()
                query="SELECT mydb.sports.sport_name FROM mydb.sports WHERE mydb.sports.sport_id= " + str(sport_id)
                db.cursor.execute(query)
                sport_name = db.cursor.fetchone()
                if myresult==[]:
                    print("yok kankam",myresult)
                    yok="Oynamak İsteyen Kimse yok"
                    return render_template('index.html',yok=yok,username=username,sport_ids=sport_id)
                return render_template('index.html',len=len(myresult),data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name)
            else:
                return redirect(url_for("sports"))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("index hata")


@app.route('/sports/<int:sport_id>/<string:user_name>_<string:user_surname>', methods=['GET','POST'])
def contact(sport_id,user_name,user_surname):
    try:
        print("alkanoooooo")
        if 'user' in session:
            username = session['user']
            if request.method == "GET": #return values for button 
                query="SELECT mydb.sports.sport_name FROM mydb.sports WHERE mydb.sports.sport_id= " + str(sport_id)
                db.cursor.execute(query)
                sport_name = db.cursor.fetchone()
                print("alkanoooooo")
                query="""SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_sports ON mydb.users.user_id = mydb.user_want_to_play_sports.Users_user_id
                    LEFT JOIN mydb.sports ON mydb.user_want_to_play_sports.Sports_sport_id  = sports.sport_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.sports.sport_id = """ + str(sport_id)

                query += " and mydb.users.user_name = " +  '"' +str(user_name)+'"'
                query +=" and mydb.users.user_surname = " + '"' +str(user_surname)+'"'
                print(query)
                db.cursor.execute(query)
                myresult = db.cursor.fetchone()
                return render_template('contact.html',data=myresult,username=username,sport_name=sport_name)
            else:
                return redirect(url_for("contact"))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("contact hata")


@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == "POST": 
            session.permanent = True
            if request.form.get("login-button"):
                user_email = request.form["username"] #take username from website textbox
                user_password = request.form["password"] #take password from website textbox
                
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + user_email + "\""
                print(query)
                db.cursor.execute(query)
                Logincheck = db.cursor.fetchone()
            
                if Logincheck:
                    
                    if Logincheck[5] == user_password:
                        session["user"] = Logincheck[1]
                        # return render_template('home.html',len=1,data=[1,2],table_name="Sports",username= session["user"])
                        return redirect(url_for("home_page"))

                    else:
                        print("WRONG PASSWORD")

                else:
                    print("WRONG USERNAME")
                    
        else:
            if "user" in session: #if already logged, redirect
                user_email=session["user"]
                return redirect(url_for("home_page"))

        return render_template("login.html")
    except:
        print("Login Error")

@app.route("/logout")
def logout():
    session.pop("user", None) #logout
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
