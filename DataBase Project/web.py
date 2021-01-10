from flask import Flask,render_template,url_for,flash,redirect,request
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

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
      if request.form.getlist('Doctor') :  ##knowing who entered a patient or a doctor
         flash(f'Account Created for Doctor {form.username.data}!','success')  #if data is correct go back to home not same page
         return redirect(url_for('home'))
      elif request.form.getlist('Patient'):
         flash(f'Account Created for MR/MS {form.username.data}!','success')  #if data is correct go back to home not same page
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
