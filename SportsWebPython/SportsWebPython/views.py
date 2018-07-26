"""
Routes and views for the flask application.
"""
import os
import secrets
import uuid
import json
from flask.json import JSONEncoder
from datetime import datetime
import dateutil.parser
from flask import render_template,flash,redirect,url_for,request,jsonify
from SportsWebPython import app,db,bcrypt
from SportsWebPython.models.models import User,Clubs,Persons,Events,Teams,Members
from SportsWebPython.forms.forms import RegistrationForm, LoginForm, CreateClubForm,PersonForm,EventForm,TeamForm
from wtforms.ext.appengine.db import model_form
from sqlalchemy.ext.declarative import DeclarativeMeta


def new_alchemy_encoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                #for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:                  
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and not x.startswith('query')]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields
            jsonify(obj)
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'layout2.html'
    )

#@app.route('/')
#@app.route('/home')
#def home():
#    """Renders the home page."""
#    return render_template(
#        'index.html',
#        title='Home Page',
#        year=datetime.now().year,
#    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/register', methods=['GET','POST'])
def register():
    """Renders the register page."""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!, You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        title='Register', form = form
    )

@app.route('/login', methods=['GET','POST'])
def login():
    """Renders the register page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if form.email.data == user.email:
        #if form.email.data == 'admin@blog.com' and form.password.data == 'password':
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template(
        'login.html',
        title='Register', form = form
    )

@app.route('/local/club<int:id>/logo')
def club_logo(id):
    club = Clubs.query.get_or_404(id)
    return app.response_class(club.Logo, mimetype='application/octet-stream')

@app.route('/local/club', methods=['GET','POST'])
def createclub():
    """Renders the create club page."""
    form = CreateClubForm()
    if form.validate_on_submit():
        file = request.files.get('Logo')
        #file = request.files['Logo']
        if file:
            logo = file.read()
        else:
            logo = None
        club = Clubs(UID=uuid.uuid4(),Name=form.Name.data,Since=form.Since.data,Date_Of=form.Date_Of.data,Logo=logo)
        db.session.add(club)
        db.session.commit()
        return redirect(url_for('home'))
        flash('Club succesfully created', 'success')
    return render_template(
        'createClub.html',
        title='Create Club', form = form
    )

@app.route('/local/clubs', methods=['GET','POST'])
def clubs():
    """Renders the clubs page."""
    clubs = Clubs.query.all()
    #club = Club.query.filter_by(name='HC Ocelari').first()
    #if clubs:
    #    flash('Club loaded', 'success')
    club = Clubs.query.first()  

    return render_template(
        'clubs.html',
        title='Create Club', clubs = clubs
    )

@app.route('/local/team<int:clubId>', methods=['GET','POST'])
def createteam(clubId):
    """Renders the create club page."""
    form = TeamForm()
    if form.validate_on_submit():
        team = Teams(UID=uuid.uuid4(),Id_Club=clubId, Name=form.Name.data,Date_Of=form.Date_Of.data)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('clubs'))
        flash('Team succesfully created', 'success')
    return render_template(
        'team.html',
        title='Create Team', form = form
    )

@app.route('/local/team<int:teamId>/members', methods=['GET','POST'])
def editteam(teamId):
    """Renders the create club page."""

    team = Teams.query.get(teamId)
    #if form.validate_on_submit():
    #    member = Members(UID=uuid.uuid4(),Id_Club=clubId, Name=form.Name.data,Date_Of=form.Date_Of.data)
    #    db.session.add(member)
    #    db.session.commit()
        #return redirect(url_for('clubs'))
        #flash('Team succesfully created', 'success')
    return render_template(
        'editTeam.html',
        title='Edit Team', team=team
    )

@app.route('/events', methods=['GET','POST'])
def events():
    """Renders the calendar page."""
    #event = Events(Id_Team=1,Subject='Prvni trenink',Date_Start=datetime.utcnow())
    events = Events.query.all()
    dict3 = []
    for event in events:
        dict = event.to_dict()
        dict.update({'title': dict['Subject'],'start':dict['Date_Start'], 'id': dict['Id_Event'],'end':dict['Date_End']})
        dict3.append(dict)

    return json.dumps(dict3)

@app.route('/local/event/<string:uid>', methods=['GET','POST'])
def editevent(uid):
    """Renders the event modal page."""
    event = Events.query.filter_by(Id_Event=uid).first()
    form = EventForm(obj=event)
    data_type='Update Event'

    if (request.method == 'POST'):
        if 'Subject' in request.form:
            event.Subject = request.form['Subject'];
        if 'Description' in request.form:
            event.Descrition = request.form['Description'];
        if 'Date_Start' in request.form:
            event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
        if 'Date_End' in request.form:
            event.Date_End = dateutil.parser.parse(request.form['Date_End']);
        db.session.add(event);
        db.session.commit();

        return json.dumps(event.to_dict())
    return render_template(
        'event.html',
        title='Update event', form = form,event=event,data_type=data_type
    )

@app.route('/local/event/', methods=['GET','POST'])
def addevent():
    """Renders the event modal page."""
    #event = Events.query.filter_by(Id_Event=uid).first()
    form = EventForm()
    data_type='Add Event'

    if (request.method == 'POST'):
        event = Events(UID = uuid.uuid4(), Id_Team = 1, Subject = request.form['Subject'],Description = request.form['Description'], Date_Start = dateutil.parser.parse(request.form['Date_Start']))
        db.session.add(event);
        db.session.commit();

        return json.dumps(event.to_dict())
    return render_template(
        'event.html',
        title='Add event', form=form,data_type=data_type
    )
   

@app.route('/calendar', methods=['GET','POST'])
def calendar():
    """Renders the calendar page."""
    #event = Events(Id_Team=1,Subject='Prvni trenink',Date_Start=datetime.utcnow)


    return render_template(
        'calendar.html',
        title='Calendar'
    )

@app.route('/local/person', methods=['GET','POST'])
def createperson():
    """Renders the create person page."""
    form = PersonForm()
    data_type = 'Create Person'
    if form.validate_on_submit():
        file = request.files['Photo']
        person = Persons(First_name=form.First_name.data,
                        Second_name=form.Second_name.data,
                        Surname=form.Surname.data,
                        Photo=file.read(),
                        Email=form.Email.data,
                        Height=form.Height.data,
                        Weight=form.Weight.data,
                        UID=uuid.uuid4()
                        )
        db.session.add(person)
        db.session.commit()
        flash('Person succesfully created', 'success')
        return redirect(url_for('persons'))
    return render_template(
        'createPerson.html',
        title='Create Person', form = form,data_type=data_type
    )

@app.route('/local/persons', methods=['GET'])
def persons():
    """Renders the persons page."""
    persons = Persons.query.all() 
    return render_template(
        'persons.html',
        title='Persons', persons = persons
    )

@app.route('/local/person<int:id>/logo')
def person_photo(id):
    person = Persons.query.get_or_404(id)
    return app.response_class(person.Photo, mimetype='application/octet-stream')

@app.route('/local/person<string:uid>', methods=['GET','POST'])
def editperson(uid):
    """Renders the create person page."""
    person = Persons.query.filter_by(UID=uid).first()
    form = PersonForm(obj=person)
    data_type='Update Person'
    if form.validate_on_submit():
        file = request.files['Photo']
        form.populate_obj(person)
        person.Photo=file.read()
        db.session.add(person)
        db.session.commit()
        #person.put()
        flash('Person succesfully updated', 'success')
    #form.first_name.data = person.First_name
    return render_template(
        'createPerson.html',
        title='Update Person', form = form,person=person,data_type=data_type
    )

@app.route('/local/personsModal/<int:idteam>', methods=['GET','POST'])
def addmember(idteam):
    """Renders the event modal page."""
    persons = Persons.query.all();
    team = Teams.query.filter_by(Id_Team=idteam).first();
    #form = EventForm(obj=event)
    #data_type='Update Event'

    #if (request.method == 'POST'):
    #    if 'Subject' in request.form:
    #        event.Subject = request.form['Subject'];
    #    if 'Description' in request.form:
    #        event.Descrition = request.form['Description'];
    #    if 'Date_Start' in request.form:
    #        event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
    #    if 'Date_End' in request.form:
    #        event.Date_End = dateutil.parser.parse(request.form['Date_End']);
    #    db.session.add(event);
    #    db.session.commit();

    #    return json.dumps(event.to_dict())
    return render_template(
        'personsModal.html',
        title='Add members',persons=persons,team=team
    )

@app.route('/local/team<int:idteam>/members/add', methods=['GET','POST'])
def addteammembers(idteam):
    """Renders the event modal page."""
    team = Teams.query.filter_by(Id_Team=idteam).first();

    if request.method == 'POST':
        for id in request.get_json()["ids"]:
            member = Members(UID=uuid.uuid4(),Id_Person=id,Id_Team=idteam,Id_Club=team.Id_Club,Id_Position=1);
            db.session.add(member);
        db.session.commit();

        return redirect(url_for('editteam',teamId=idteam))
    #form = EventForm(obj=event)
    #data_type='Update Event'

    #if (request.method == 'POST'):
    #    if 'Subject' in request.form:
    #        event.Subject = request.form['Subject'];
    #    if 'Description' in request.form:
    #        event.Descrition = request.form['Description'];
    #    if 'Date_Start' in request.form:
    #        event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
    #    if 'Date_End' in request.form:
    #        event.Date_End = dateutil.parser.parse(request.form['Date_End']);
    #    db.session.add(event);
    #    db.session.commit();

    #    return json.dumps(event.to_dict())
    return json.dumps([])