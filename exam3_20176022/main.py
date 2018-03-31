from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hii'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///exam3database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class User(db.Model):

	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	password = db.Column(db.String(255))
	email = db.Column(db.String(255))

	def __init__(self,email,password):
		self.password=password
		self.email=email

db.create_all()


def logindetails():
	if 'email' not in session:
		login = False
	else:
		login = True

	return login

@app.route("/", methods = ['POST','GET'])
def root():
	login = logindetails()
	return render_template("home.html",error='')

@app.route("/login", methods = ['POST','GET'])
def login():
	if request.method =='POST':
		email = request.form['email']
		password = request.form['password']
		stmt = "SELECT email, password FROM users"
		data = db.engine.execute(stmt).fetchall()
		for row in data:
			if row[0] == email and row[1] == password:
				session['email']=email
				error = session['email']
				return render_template('login.html',error=error)
			elif row[0] == email and row[1] != password:
				error = 'Invalid password'
				return render_template('home.html',error=error)
			else:
				error = 'No account found'
				return render_template('home.html',error=error)

@app.route("/register", methods=['POST','GET'])
def register():
	if request.method == 'POST':
		email = request.form['reg_email']
		psw = request.form['reg_psw']
		cpsw = request.form['reg_cpsw']
		stmt = "SELECT email, password FROM users"
		data = db.engine.execute(stmt).fetchall()
		# error = ''
		for row in data:
			if row[0] == email:
				print("for -- if")
				error = 'account already exits'
			elif psw == cpsw:
				try:
					user = User(email,psw)
					db.session.add(user)
					db.session.commit()
					error = 'Register Successful'
					print("for -- elif -- try")
				except:
					db.rollback()
					error = 'error occured'
					print("for -- elif -- except")
			else:
				error = 'password don\'t match'
				print("for -- else")
		db.session.close()
		return render_template("home.html",error=error)

if __name__ =='__main__':
	
	app.run(debug=True)
