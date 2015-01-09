from flask import render_template, request, flash
from app import app
import json, Database, psycopg2, sqlite3


from itertools import combinations
from Database import session, Show, Login



@app.route('/')
def index():
    options = {'events':session.query(Show).order_by(Show.id),
    	'hourconvert':hourconvert,
    	'checkspot':checkspot}

    idat = session.query(Show).order_by(Show.id)
    k = 0
    j = 1
    m = []
    for i in idat:
    	k += 1
    if k % 10 == 0:
    	k = k / 10
    else:
    	k = (k / 10) + 1

	while j <= k:
		m.append(j)
		j += 1 

	options['num']=m
	return render_template('index.html', **options)


@app.route('/submitpicks', methods=["POST", "GET"])
def subpicks():
	options = {
		'events': list(session.query(Show).order_by(Show.id)),
		'hourconvert': hourconvert,
		'checkspot': checkspot}
	
	shows = options['events']
	data = request.form.getlist('spoopy',type=int)

	schedules = []

	for i in data:

		working = []
		working.append(shows[i])

		for j in data:

			if times_work(shows[i], shows[j]):
				
				if shows[j] not in working:
					
					working.append(shows[j])

		for j in working:

			for l in working:

				if (j.name != l.name) and not times_work(j,l):

					working.remove(l)


		working = sorted(working, key=lambda show: show.start)

		if working not in schedules:
			
			schedules.append(working)


	schedules = sorted(schedules, key=len)
	schedules.reverse()

	options['schedules'] = schedules

	return render_template('submitpicks.html', **options)



@app.route('/log')
def log():
	return render_template('login.html')



@app.route('/change', methods=["POST","GET"])
def login():
	options = {'events':session.query(Show).order_by(Show.id),
		'checkspot':checkspot
		}
	data = session.query(Login)
	name = request.form.get('username')
	password = request.form.get('password')

	idat = session.query(Show).order_by(Show.id)
	k = 0
	j = 1
	m = []
	for i in idat:
		k += 1
	if k % 10 == 0:
		k = k / 10
	else:
		k = (k / 10) + 1

	while j <= k:
		m.append(j)
		j += 1 

	options['num']=m

	if name == data[0].username:

		if password == data[0].password:


			return render_template('change.html', **options)

	error = str('Invalid Username or Password, Please Try Again')
	options['error'] = error
	return render_template('error.html', **options)


	

@app.route('/fixtable', methods=["POST","GET"])
def fix():
	options = {'events':session.query(Show).order_by(Show.id),
		'checkspot':checkspot
		}
	shows = options['events']
	person1 = request.form.getlist('first')
	person2 = request.form.getlist('second')

	
	idat = session.query(Show).order_by(Show.id)
	k = 0
	j = 1
	m = []
	for i in idat:
		k += 1
	if k % 10 == 0:
		k = k / 10
	else:
		k = (k / 10) + 1

	while j <= k:
		m.append(j)
		j += 1 

	options['num']=m

	j = 0
	for i in person1:
		if shows[j].person1 != i:
			shows[j].person1 = i
		j += 1
	
	j = 0
	for i in person2:
		if shows[j].person2 != i:
			shows[j].person2 = i
		j += 1

	j=0
	for i in shows:
		if i.person1 == ' ' or '':
			i.person1 = 'none'
		if i.person2 == ' ' or '':
			i.person2 = 'none'

	j=0
	for i in shows:
		if i.person1 == 'none' and i.person2 != 'none':
			i.person1 = i.person2
			i.person2 = 'none'
		if i.person1 == '' and i.person2 != 'none':
			i.person1 = i.person2
			i.person2 = 'none'
		if i.person1 == ' ' and i.person2 != 'none':
			i.person1 = i.person2
			i.person2 = 'none'

	session.commit()

	return render_template('change.html', **options)

@app.route('/cleartable', methods=["POST","GET"])
def clear():
	options = {'events':session.query(Show).order_by(Show.id),
    	'hourconvert':hourconvert,
    	'checkspot':checkspot}
	shows = session.query(Show).order_by(Show.id)

	for i in shows:
		i.person1 = 'none'
		i.person2 = 'none'

	session.commit()

	idat = session.query(Show).order_by(Show.id)
	k = 0
	j = 1
	m = []
	for i in idat:
		k += 1
	if k % 10 == 0:
		k = k / 10
	else:
		k = (k / 10) + 1

	while j <= k:
		m.append(j)
		j += 1 

	options['num']=m

	return render_template('change.html', **options)

@app.route('/submitchoices', methods=["POST","GET"])
def subchoice():
	options = {'events':session.query(Show).order_by(Show.id),
    	'hourconvert':hourconvert,
    	'checkspot':checkspot}
 	
	error = ''
	shows = options['events']
	data = request.form.getlist('picks',type=int)
	username = request.form.get('name',type=str)
	
	if username == '':
		error = 'Please Use a Proper Name'
		options['error'] = error
		return render_template('error.html', **options)


	for i in data:

		if shows[i].person2 != 'none':
			
			error = str(shows[i].name + ' is Full, Please Adjust your Choices')
			options['error'] = error
			return render_template('error.html', **options)

	for i in data:

		if shows[i].person2 == shows[i].person1 and shows[i].person1 != 'none':
			error = str('You Cannot Sign Up Twice for the Same Shift, Please Adjust Your Choices')
			options['error'] = error
			return render_template('error.html', **options)

	for i in data:

		for j in data:

			if not times_work(shows[i], shows[j]):
				
				error = str(shows[i].name + ' Does Not Work with ' + shows[j].name + ', Please Adjust Your Choices')
				options['error'] = error
				return render_template('error.html', **options)
	

	for i in data:
		if shows[i].person1 == 'none':
			shows[i].person1 = username

		else:
			shows[i].person2 = username

		session.add(shows[i])

	session.commit()

	htmlpage = []

	for i in data:
		htmlpage.append(shows[i])


	htmlpage = sorted(htmlpage, key=lambda show: show.start)

	options['data'] = htmlpage

	return render_template('thankyou.html', **options)

   

def hourconvert(time):
	
	half = 'AM'
	hour = int(time) / 60
	if int(hour) > 12:
		hour -= 12
		half = 'PM'
	if int(hour) > 12:
		hour -= 12
		half = 'AM'
	minutes = int(time) % 60
	display = "{:2d}:{:02d} {}".format(hour, minutes, half)
	return display




def checkspot(person):
	if person == 'none':
		return ''
	return person


def shows_work(one, two):
	if one.name == two.name:
		return False

	if one.start <= two.start <= one.finish:
		return False
	
	if one.start <= two.finish <= one.finish:
		return False

	if two.start <= one.start <= two.finish:
		return False

	if two.start <= one.finish <= two.finish:
		return False

	return True

def times_work(one, two):
	if one.name == two.name:
		return True

	if one.start <= two.start <= one.finish:
		return False
	
	if one.start <= two.finish <= one.finish:
		return False

	if two.start <= one.start <= two.finish:
		return False

	if two.start <= one.finish <= two.finish:
		return False

	return True


def formpage():
	return 'kyle'

def checktime(time1start, time1end, time2start, time2end):

	if time1start > time2start > time1end:
		return False
	if time1start > time2end > time1end:
		return False
	return True









































