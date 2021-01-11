from flask import Flask,render_template,url_for,flash,redirect,request
from forms import RegistrationForm,LoginForm,ContactForm
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
      if request.form.getlist('Doctor') and request.form.getlist('Patient'):
         flash(f'Choose only one Doctor, patient ','success') 
         return render_template('register.html',title='Register',form=form)

      if request.form.getlist('Doctor') :  ##knowing who entered a patient or a doctorpip install mysql
         flash(f'Account Created for Doctor {form.username.data}! now you can login','success') 
         if request.method =="POST":   #if data is correct go back to home not same page
          username = request.form["username"]
          email = request.form["email"]
          password = request.form["password"]
          sql = "INSERT INTO Doctors (username,email,password) VALUES (%s, %s, %s)"
          val = (username,email,password)
          mycursor.execute(sql, val)
          mydb.commit()
          print(username,email,password)   
         return redirect(url_for('login'))
      elif request.form.getlist('Patient'):
         flash(f'Account Created for MR/MS {form.username.data}! now you can login','success')  #if data is correct go back to home not same page
         if request.method =="POST":   #if data is correct go back to home not same page
          username = request.form["username"]
          email = request.form["email"]
          password = request.form["password"]
          sql = "INSERT INTO patients (username,email,password) VALUES (%s, %s, %s)"
          val = (username,email,password)
          mycursor.execute(sql, val)
          mydb.commit()
          print(username,email,password)   
         return redirect(url_for('login'))
     


       
   return render_template('register.html',title='Register',form=form)



@app.route('/login', methods=['GET','POST'] )
def login():
   
   form=LoginForm()
   if form.validate_on_submit():
      if request.form.getlist('Doctor') and request.form.getlist('Patient'):
         flash(f'Choose only one Doctor, patient ','success') 
         return render_template('login.html',title='login',form=form)

      if request.form.getlist('Doctor') :
         if request.method =="POST":  
           email = request.form["email"]
           password = request.form["password"]
           sql= "SELECT email , password FROM Doctors WHERE email= %s and password = %s "
           val=(email,password)
           mycursor.execute(sql, val)
           myresult=mycursor.fetchone()
           print(myresult)
           
           if myresult==None:
             flash(f'Incorrect email/password!','success') 
             return render_template('login.html',title='login',form=form)  

              

           return redirect(url_for('home'))

      elif request.form.getlist('Patient') :
       
         if request.method =="POST":  
           email = request.form["email"]
           password = request.form["password"]
           sql= "SELECT email , password FROM Patients WHERE email= %s and password = %s "
           val=(email,password)
           mycursor.execute(sql, val)
           myresult=mycursor.fetchone()
           print(myresult)
           
           if myresult==None:
             flash(f'Incorrect email/password!','success') 
             return render_template('login.html',title='login',form=form)  

              

           return redirect(url_for('home'))

      elif request.form.getlist('Admin') :

         if request.method =="POST":  
           email = request.form["email"]
           password = request.form["password"]
           sql= "SELECT email , password FROM admin WHERE email= %s and password = %s "
           val=(email,password)
           mycursor.execute(sql, val)
           myresult=mycursor.fetchone()
           print(myresult)

           if myresult==None:
             flash(f'Incorrect email/password!','success') 
             return render_template('login.html',title='login',form=form)  

              

           return render_template('admin.html',title='Register',form=form)

         
 
 
 
   return render_template('login.html',title='Register',form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    
    username = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    sql = "INSERT INTO contact_us (username,email,subject,message) VALUES (%s, %s, %s,%s)"
    val = (username,email,subject,message)
    mycursor.execute(sql, val)
    mydb.commit()
    print(username,email,subject,message)   
    flash(f'Form posted ! , We are happy to hear from you !')    
    return redirect(url_for('contact'))
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/addDoctor', methods=['GET', 'POST'])
def add():
   if request.method=="POST":
      username = request.form["doctorName"]
      email = request.form["doctorEmail"]
      password= request.form["doctorPass"]
      ID = request.form["doctorID"]
      sql = "INSERT INTO Doctors (username,email,password,ID) VALUES (%s, %s,%s, %s)"
      val = (username,email,password,ID)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('Home.html') 
   else:
      return render_template('addDoctor.html') 

@app.route('/viewDoctors')
def viewD():
   mycursor.execute("SELECT * FROM Doctors")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   for x in myresult:
      print(x)
   return render_template('viewDoctors.html',viewD=myresult)

@app.route('/addPatient', methods=['GET', 'POST'])
def addP():
   if request.method=="POST":
      username = request.form["patientName"]
      email = request.form["patientEmail"]
      password= request.form["patientPass"]
      ID = request.form["patientID"]
      sql = "INSERT INTO patients (username,email,password,ID) VALUES (%s, %s, %s, %s)"
      val = (username,email,password,ID)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('Home.html') 
   else:
      return render_template('addPatient.html') 

@app.route('/viewPatients')
def viewP():
   mycursor.execute("SELECT * FROM patients")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   for x in myresult:
      print(x)
   return render_template('viewPatients.html',viewP=myresult)  

@app.route('/removeDoctor', methods=['GET', 'POST'])
def deleteD():
   if request.method=="POST":
      id = request.form["doctorID"]
      mycursor = mydb.cursor()
      sql = "DELETE FROM Doctors WHERE id = %s"
      val = (id,)
      mycursor.execute(sql, val)
      mydb.commit()
      flash(f'Doctor succesfully removed !')    
      return redirect(url_for('viewD'))
   else:
      return render_template('removeDoctor.html')

@app.route('/removePatient', methods=['GET', 'POST'])
def deleteP():
   if request.method=="POST":
      id = request.form["patientID"]
      mycursor = mydb.cursor()
      sql = "DELETE FROM patients WHERE id = %s"
      val = (id,)
      mycursor.execute(sql, val)
      mydb.commit()
      flash(f'Patient succesfully removed !')    
      return redirect(url_for('viewP'))
   else:
      return render_template('removePatient.html')
if __name__ == '__main__':
   app.run(debug=True)

 