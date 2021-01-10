from flask import Flask,render_template,url_for,flash,redirect,request
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="project"
)
mycursor = mydb.cursor()


app.config['SECRET_KEY']='b0a26ce6fb663a3d7f006e020de17a9e'  #secret key for protection

@app.route('/')
@app.route('/home')
def home():
   return render_template('Home.html')

@app.route('/about')
def about():
   return render_template('About.html')

@app.route('/register', methods=['GET','POST'])
def register():
   form=RegistrationForm()

   

   if form.validate_on_submit():
      if request.form.getlist('Doctor') :  ##knowing who entered a patient or a doctorpip install mysql
         flash(f'Account Created for Doctor {form.username.data}!','success') 
         if request.method =="POST":   #if data is correct go back to home not same page
          username = request.form["username"]
          email = request.form["email"]
          password = request.form["password"]
          sql = "INSERT INTO Doctors (username,email,password) VALUES (%s, %s, %s)"
          val = (username,email,password)
          mycursor.execute(sql, val)
          mydb.commit()
          print(username,email,password)   
         return redirect(url_for('home'))
      elif request.form.getlist('Patient'):
         flash(f'Account Created for MR/MS {form.username.data}!','success')  #if data is correct go back to home not same page
         if request.method =="POST":   #if data is correct go back to home not same page
          username = request.form["username"]
          email = request.form["email"]
          password = request.form["password"]
          sql = "INSERT INTO patients (username,email,password) VALUES (%s, %s, %s)"
          val = (username,email,password)
          mycursor.execute(sql, val)
          mydb.commit()
          print(username,email,password)   
         return redirect(url_for('home'))

       
   return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET','POST'] )
def login():
   
   form=LoginForm()
   ##if form.validate_on_submit():
      #### wait for data base 
   return render_template('login.html',title='Login',form=form)


if __name__ == '__main__':
   app.run(debug=True)