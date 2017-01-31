# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from timeit import default_timer
from math import floor


# configuration
DATABASE = '/Users/subramanian/Desktop/DDOSproject/EMPLOYEEFINAL.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app= Flask(__name__)
app.config.from_object(__name__)



speedfinal=300
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schemaEmployees.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def hello_world(name=None):
	return render_template('hello.html', name=name)
@app.route('/admin')
def admin():
	return render_template('linkspeed.html')

@app.route('/admin2', methods =['POST'])
def admin_post():
	speed=int(request.form['linkspeed'])
	global speedfinal
	speedfinal=speed*300/36
	return "Your chosen speed is "+str(speed)
	
@app.route('/getEmployees/<userid>')
def all(userid):
	if userid == "gooduser" or userid == "baduser" or userid== "baduser1" or userid=="baduser2" or userid=="baduser3" or userid== "baduser4":
		# Allow the user to specify an offset via querystring
		offset = request.args.get('offset')


		# Allow user to specify limit but default to 50
		limit = request.args.get('limit',speedfinal)

		if offset is None:
			# Look in the session and default to 0 if not defined
			offset = session.get('offset', 0)

		g.db = connect_db()
		cur = g.db.execute('select * from employees limit %d offset %d' % (limit, int(offset)))
		employees=[dict(emp_no=row[0],birth_date=row[1],first_name=row[2],last_name=row[3],gender=row[4],hire_date=row[5]) for row in cur.fetchall()]
		g.db.close()



		session['offset']= offset + limit;
		#session['offset']=0
		#return render_template('index.html', employees=employees)
		return str(employees)
		#return 'Working'
		

	else:
		return "You are not allowed to access"

	

@app.route('/getEmployees/<userid>/<emp_no>')
def byempno(userid,emp_no):
	if userid == "gooduser" or userid == "baduser" or userid== "baduser1" or userid=="baduser2" or userid=="baduser3" or userid =="baduser4":
		g.db = connect_db()
		cur=g.db.execute('select * from employees where emp_no = '+ emp_no)
		employees=[ dict(emp_no=row[0],birth_date=row[1],first_name=row[2],last_name=row[3],gender=row[4],hire_date=row[5]) for row in cur.fetchall()]
		g.db.close()

		x = str(employees)
		#return render_template('index.html', employees=employees)
		return (x)


	else:
		return "you are not allowed to access"

@app.route('/getEmployeesWildcard/<userid>/<wildcard>')
def wildcard(userid,wildcard):
	if userid == "gooduser" or userid == "baduser" or userid== "baduser1" or userid== "baduser2" or userid=="baduser3" or userid=="baduser4":
		g.db =connect_db()
		cur=g.db.execute('select * from employees where first_name Like'+"'%" + wildcard + "%'")
		employees=[ dict(emp_no=row[0],birth_date=row[1],first_name=row[2],last_name=row[3],gender=row[4],hire_date=row[5]) for row in cur.fetchall()]
		g.db.close()
		#return render_template('index.html', employees=employees)
		return str(employees)

@app.route('/getEmployeesAge/<userid>/<age>')
def agesort(userid,age):
	if userid == "gooduser" or userid == "baduser" or userid == "baduser1" or userid=="baduser2" or userid=="baduser3" or userid== "baduser4":
		
		# Allow the user to specify an offset via querystring
		offset = request.args.get('offset')

		# Allow user to specify limit but default to 50
		limit = request.args.get('limit', 400)

		if offset is None:
			# Look in the session and default to 0 if not defined
			offset = session.get('offset', 0)


		g.db = connect_db()
		cur=g.db.execute("select * from employees where date('now') - birth_date > "+ age)
		employees=[dict(emp_no=row[0],birth_date=row[1],first_name=row[2],last_name=row[3],gender=row[4],hire_date=row[5]) for row in cur.fetchall()]
		g.db.close()

		session['offset']= offset + limit;

		#return 'Working'
		return render_template('index.html', employees=employees)
		#return str(employees)
	else:
		return "You are not allowed to access"

@app.route('/getEmployeesOrderBy/<userid>/<column>')
def orderby(userid,column):
	if userid == "gooduser" or userid == "baduser" or userid == "baduser1" or userid=="baduser2" or userid=="baduser3" or userid=="baduser4":
		g.db = connect_db()
		cur=g.db.execute("select * from employees ORDER BY "+column)
		employees=[dict(emp_no=row[0],birth_date=row[1],first_name=row[2],last_name=row[3],gender=row[4],hire_date=row[5]) for row in cur.fetchall()]
		g.db.close()
		#return 'Working'
		#return render_template('index.html', employees=employees)
		return str(employees)

	else:
		return "You are not allowed to access"

if __name__=='__main__':
	app.run(host ='0.0.0.0')
	



        