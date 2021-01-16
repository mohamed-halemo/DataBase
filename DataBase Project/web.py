from flask import Flask,render_template,url_for,flash,redirect,request
from forms import RegistrationForm,LoginForm,ContactForm,UpdateAccountForm,PostForm
from flask_sqlalchemy import SQLAlchemy ##trying another DS
from datetime import datetime,timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,UserMixin,login_user   ,current_user ,logout_user ,login_required           
import secrets               
import os   ###
from PIL import Image
from dateutil import parser
from cal_setup import get_calendar_service
import random

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


login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


db.create_all()



@app.route('/')
@app.route('/home')
def home():
     posts = Post.query.all()
     return render_template('home.html', posts=posts)



@app.route('/about')
def about():
   return render_template('About.html')

@app.route('/register', methods=['GET','POST'])
def register():


   if current_user.is_authenticated:
      return redirect(url_for('home'))


   form=RegistrationForm()

  

   if form.validate_on_submit():
      if request.form.getlist('Doctor') and request.form.getlist('Patient'):
          
         return render_template('register.html',title='Register',form=form)

      if request.form.getlist('Doctor') :  ##knowing who entered a patient or a doctorpip install mysql
         
         if request.method =="POST":   #if data is correct go back to home not same page
           user=User(username=form.username.data,email=form.email.data,password=form.password.data)
           db.session.add(user)
           db.session.commit()
           username = request.form["username"]
           email = request.form["email"]
           password = request.form["password"]
           sql= "SELECT email FROM Doctors WHERE email= %s "
           val=(email,)
           cursor = mydb.cursor(buffered=True)

           mycursor.execute(sql, val)
           myresult=mycursor.fetchone()
           if myresult!=None:
               flash(f'Email is used before') 
               return redirect(url_for('register'))
           else :
               flash(f'Account Created for Doctor {form.username.data}! now you can login','success')
               sql = "INSERT INTO Doctors (username,email,password) VALUES (%s, %s, %s)"
               val = (username,email,password)
               cursor = mydb.cursor(buffered=True)

               mycursor.execute(sql, val)
               mydb.commit()
               print(username,email,password)   
         return redirect(url_for('login'))
      elif request.form.getlist('Patient'):

         user=User(username=form.username.data,email=form.email.data,password=form.password.data)
         db.session.add(user)
         db.session.commit()
           #if data is correct go back to home not same page
         if request.method =="POST":   #if data is correct go back to home not same page
          username = request.form["username"]
          email = request.form["email"]
          password = request.form["password"]
          sql= "SELECT email FROM Patients WHERE email= %s "
          val=(email,)
          cursor = mydb.cursor(buffered=True)

          mycursor.execute(sql, val)
          myresult=mycursor.fetchone()
          if myresult!=None:
            flash(f'Email is used before') 
            return redirect(url_for('register'))
          else :
           flash(f'Account Created for MR/MS {form.username.data}! now you can login','success')
           sql = "INSERT INTO patients (username,email,password) VALUES (%s, %s, %s)"
           val = (username,email,password)
           mycursor.execute(sql, val)
           mydb.commit()
           print(username,email,password)   
         return redirect(url_for('login'))
     


       
   return render_template('register.html',title='Register',form=form)



@app.route('/login', methods=['GET','POST'] )
def login():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
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
                        
         user=User.query.filter_by(email=form.email.data).first()
         if user is None:
            flash(f'Incorrect email/password!','success')                           ###########################
            return render_template('login.html',title='login',form=form)  

         login_user(user)  

              

         return redirect(url_for('doctor'))

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
         user=User.query.filter_by(email=form.email.data).first()
         if user is None:
            flash(f'Incorrect email/password!','success')                           ###########################
            return render_template('login.html',title='login',form=form)  
         login_user(user)  
 
              

         return redirect(url_for('patient'))

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
         
         user=User.query.filter_by(email=form.email.data).first()

         if user is None:
            flash(f'Incorrect email/password!','success')                           ###########################
            return render_template('login.html',title='login',form=form)  
         login_user(user)  
      

         return redirect(url_for('admin'))

         
 
 
 
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

@app.route('/viewContact')
def viewC():
   if current_user.is_authenticated:

      mycursor.execute("SELECT * FROM contact_us")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('viewContact.html',viewC=myresult)    
   else :
      form=LoginForm()
      return render_template('login.html',title='login',form=form)      

@app.route('/addDoctor', methods=['GET', 'POST'])
def add():
   
      if request.method=="POST":
         username = request.form["doctorName"]
         email = request.form["doctorEmail"]
         password= request.form["doctorPass"]
         user=User(username=username,email=email,password=password)

         db.session.add(user)
         db.session.commit()
         ID = request.form["doctorID"]
         sql = "INSERT INTO Doctors (username,email,password,ID) VALUES (%s, %s,%s, %s)"
         val = (username,email,password,ID)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'Doctor is succesfully added !')    
         return redirect(url_for('viewD')) 
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
         user=User(username=username,email=email,password=password)

         db.session.add(user)
         db.session.commit()
         ID = request.form["patientID"]
         sql = "INSERT INTO patients (username,email,password,ID) VALUES (%s, %s, %s, %s)"
         val = (username,email,password,ID)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'Patient is succesfully added !')    
         return redirect(url_for('viewP'))
    
      else:
         return render_template('addPatient.html') 
               
   
 
@app.route('/typeP', methods=['GET', 'POST'])
def typeP():

      if request.method=="POST":
         ID = request.form["patientID"]
         typeP = request.form["typeP"]
         #user=User(typeP=typeP)
         #db.session.add(user)
         #db.session.commit()  #ana sayeb el database bta3et add patient 3adlha bs bl t3delat el gdedaa 
         sql = "UPDATE patients SET type = %s  WHERE id = %s "
         val = (typeP,ID)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'Your Info is succesfully updated !')    
         return render_template('patient.html')
    
      else:
         return render_template('typeP.html') 
  
@app.route('/viewPatients')
def viewP():

      mycursor.execute("SELECT * FROM patients")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('viewPatients.html',viewP=myresult)
 
@app.route('/patientH')
def patientH():

      mycursor.execute("SELECT * FROM patients")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('patientH.html',patientH=myresult)   
   
@app.route('/removeDoctor', methods=['GET', 'POST'])
def deleteD():

      if request.method=="POST":
         id = request.form["doctorID"]
         mycursor = mydb.cursor()
         sql = "DELETE FROM Doctors WHERE id = %s"
         val = (id,)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'Doctor is succesfully removed !')    
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
         flash(f'Patient is succesfully removed !')    
         return redirect(url_for('viewP'))
      else:
         return render_template('removePatient.html')
    

@app.route('/relate', methods=['GET', 'POST'])
def relate():
  

      if request.method=="POST":
         p_code = request.form["patientID"]
         d_code = request.form["doctorID"]
         appointment=request.form["appointmenttime"]
         hour=request.form["hour"]
         sql = "INSERT INTO DOC_PAT (d_code,p_code,appointment,hour) VALUES (%s,%s,%s,%s)"
         val = (d_code,p_code,appointment,hour)
         cursor = mydb.cursor(buffered=True)

         mycursor.execute(sql,val)
         mydb.commit()
         print(p_code,d_code,appointment)
         flash(f'The Patient is assigned to a Doctor !')  
       #####################################################################   


# creates one hour event tomorrow 10 AM IST
         service = get_calendar_service()

         d = datetime.now().date() 
         tomorrow = datetime(d.year, d.month, d.day,int (hour))+timedelta(days=1) #CHANGE HERE
         start = tomorrow.isoformat()
         end = (tomorrow + timedelta(hours=1)).isoformat()

         event_result = service.events().insert(calendarId='primary',
         body={
              "summary": 'Automating calendar',
              "description": 'This is a tutorial example of automating google calendar with python',
              "start": {"dateTime": start, "timeZone": 'GMT-10'},
              "end": {"dateTime": end, "timeZone": 'GMT-10'},
            }
         ).execute()

         print("created event")
         print("id: ", event_result['id'])
         print("summary: ", event_result['summary'])
         print("starts at: ", event_result['start']['dateTime'])
         print("ends at: ", event_result['end']['dateTime'])


  
         return redirect(url_for('viewR')) 






###########################################################################
      else:
         return render_template('relate.html')

  





















@app.route('/viewRelation')
def viewR():

      mycursor.execute("SELECT doctors.username,doctors.id , patients.username,patients.id , doc_pat.appointment FROM DOC_PAT  JOIN Doctors on DOC_PAT.d_code = doctors.id JOIN patients on DOC_PAT.p_code = patients.id;")
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('viewRelation.html',viewR=myresult)    
  

@app.route('/recoveredPatient', methods=['GET', 'POST'])
def rec():


      if request.method=="POST":
         p_code = request.form["patientID"]
         recoveredTime=request.form["recoveredTime"]
         sql = "INSERT INTO REC_PATIENT (p_id,date_rec) VALUES (%s,%s)"
         val = (p_code,recoveredTime)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'Informations succesfully updated !')
         return redirect(url_for('vRec')) 
      else:
         return render_template('recoveredPatient.html')
      
      

@app.route('/viewRecovered')
def vRec():

      mycursor.execute("SELECT patients.username,patients.id ,date_rec FROM REC_PATIENT JOIN PATIENTS on REC_PATIENT.p_id = patients.id")
    
      myresult = mycursor.fetchall()

      for x in myresult:
         print(x)
      return render_template('viewRecovered.html',vRec=myresult)
   

@app.route('/terminate', methods=['GET', 'POST'])
def terminate():

      if request.method=="POST":
         p_code = request.form["patientID"]
         sql="DELETE FROM DOC_PAT WHERE p_code=%s"
         val=(p_code,)
         mycursor.execute(sql, val)
         mydb.commit()
         flash(f'The Patient is terminated successfully !')    
         return redirect(url_for('viewR')) 
    
      else:
         return render_template('terminate.html') 
 

@app.route('/yourPatient', methods=['GET', 'POST'])
def yourPatient():

      if request.method=="POST":
         d_code = request.form["doctorID"]
         sql="SELECT Patients.username, Patients.id, doc_pat.appointment FROM DOC_PAT  JOIN Doctors on DOC_PAT.d_code = Doctors.id JOIN Patients on DOC_PAT.p_code = Patients.id WHERE d_code= %s "
         val=(d_code,)
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         for x in myresult:
            print(x)
         return render_template('vyourPatient.html',yourPatient=myresult)        
    
      else:
         return render_template('yourPatient.html')  
         

@app.route('/yourDoctor', methods=['GET', 'POST'])
def yourDoctor():

      if request.method=="POST":
         p_code = request.form["patientID"]
         sql="SELECT Doctors.username,Doctors.id ,doc_pat.appointment FROM DOC_PAT  JOIN Patients on DOC_PAT.p_code = Patients.id JOIN Doctors on DOC_PAT.d_code = Doctors.id WHERE p_code= %s "
         val=(p_code,)
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         for x in myresult:
            print(x)
         return render_template('vyourDoctor.html',yourDoctor=myresult)        
    
      else:
         return render_template('yourDoctor.html')
 
@app.route('/available')
def available():

      mycursor.execute("SELECT * FROM Doctors")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('available.html',available=myresult)   
   

@app.route('/stats')
def stats():
   if current_user.is_authenticated:
      mycursor.execute("SELECT 'Doctors' AS table_name, COUNT(id) FROM doctors UNION SELECT 'All Patients' AS table_name, COUNT(id) FROM patients UNION SELECT 'Recovered' AS table_name, COUNT(p_id) FROM rec_patient")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for x in myresult:
         print(x)
      return render_template('stats.html',stats=myresult)      
   else :
      form=LoginForm()
      return render_template('login.html',title='login',form=form)     

@app.route('/admin')
def admin():
    if current_user.is_authenticated:  
       return render_template('admin.html')
    else:
       form=LoginForm()
       return render_template('login.html',title='login',form=form)  



@app.route('/doctor')
def doctor():
   if current_user.is_authenticated:
      return render_template('doctor.html')
   else :
      form=LoginForm()

      return render_template('login.html',title='login',form=form)  


@app.route('/patient')
def patient():

   if current_user.is_authenticated:
      return render_template('patient.html')
   else :
      form=LoginForm()
      return render_template('login.html',title='login',form=form)  





@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) 

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)








@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))




   








if __name__ == '__main__':
   app.run(debug=True)


 