from flask import Flask , render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Required
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from random import randint


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
app.config['SECRET_KEY']='dsgjlsdfnlbdnlkmbkldfmkdkeopkwfefsbfhnghhbdb556'

bootstrap= Bootstrap(app)


class Question(db.Model):
    __tablename__='questions'
    idq = db.Column(db.Integer, primary_key= True, nullable =False)
    string = db.Column(db.Text, nullable =False)
    db.relationship('comment',backref ='questions')

class Comment(db.Model):
    __tablename__='comment'
    idq = db.Column(db.Integer, primary_key= True, nullable = False)
    string =db.Column(db.Text, nullable =False)
    comment_id= db.Column(db.Integer,db.ForeignKey('questions.idq'))

class  User(db.Model):
    __tablename__='user'
    name =db.Column(db.String(128), primary_key =True, nullable= False)
    password =db.Column(db.String(128), nullable =False)

####################################################################    
class User_meetup(db.Model):
    __tablename__='usermeetup'
    name =db.Column(db.String(128), primary_key =True, nullable= False)
    password =db.Column(db.String(128), nullable =False)
    email=db.Column(db.String(128), nullable =False)
    


class Meetup(db.Model):
    __tablename__='meetup'
    name=db.Column(db.String(128), nullable= False)
    location= db.Column(db.String(128), nullable =False)
    subject= db.Column(db.Text, nullable= False)
    id_m= db.Column(db.Integer, primary_key= True ,nullable =False)

    

db.create_all()


class question_form(FlaskForm):
    title= StringField('Question ID', validators=[Required()])
    post= TextAreaField('Post your question', validators=[Required()])
    submit= SubmitField('Post')


class comment_form(FlaskForm):
    answer= TextAreaField('Post your answer', validators=[Required()])
    submit= SubmitField('Post')

class signup_form(FlaskForm):
    name= StringField('User name', validators=[Required()])

    password= PasswordField('Password' , validators =[Required()])
    submit= SubmitField('Submit')

###########################################################################

    #Meetup project
class meetup_form(FlaskForm):
    name= StringField('name', validators=[Required()])
    location= StringField('location', validators=[Required()])
    subject= TextAreaField('subject', validators=[Required()])
    submit= SubmitField('Submit')

class login_meetup(FlaskForm):
    firstname= StringField('firstname', validators=[Required()])

    password= PasswordField('password' , validators =[Required()])
    submit= SubmitField('Submit')

class signup_meetup(FlaskForm):
    firstname= StringField('firstname', validators=[Required()])
    email= StringField('email', validators=[Required()])
    password= PasswordField('password' , validators =[Required()])
    submit= SubmitField('Sign up')

    

@app.route('/', methods=['POST','GET'])

def index():
    querys=Question.query.limit(30)
    form = question_form()
    user=session.get('name')
    if request.method== 'POST':
        if form.validate_on_submit():
            question= Question()
            question.idq=(form.title.data)
            question.string=form.post.data
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))

    else:
        form.title.data=''
        form.post.data=''
    
        #question.idq=form.title.data
        #question.string=form.post.data
        #form.populate_obj(question)
        #db.session.add(question( idq = form.title.data, string = form.post.data))
        #db.session.add(question)
        #return redirect(url_for('.index'))
    return render_template('form.html', form=form , querys=querys, user=user)






	
@app.route('/contacts')
def contacts():
    return "<h3> Contacts </h3>"


@app.route('/post', methods = ['GET','POST'])
def post():
    if request.method== 'POST':
        if form.validate_on_submit():
            return form.title.data+"   "+form.post.data
    else:
        return "<h3> post your question </h3>"

    

@app.route('/question/<id>', methods = ['GET','POST'])

def question(id):
    form=comment_form()
    querys = Question.query.filter_by(idq = id).first()
    query_comment=Comment.query.filter_by(comment_id=id).all()
    if request.method=='POST':
        comment=Comment()
        comment.comment_id=querys.idq
        comment.string=form.answer.data
        comment.idq=randint(1, 100000000000)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('question', id=id))
    else:
        return render_template('question.html', querys=querys,form=form ,comments=query_comment,user=session.get('name'))



@app.route('/api/v1/<auth>/<int:qid>/',methods =['GET'])

def api_get_question(auth,qid):
    querys_ = Question.query.filter_by(idq = qid).first()

    if querys_ is None:

        return "No results Found "+auth +" "+str(qid)


    else:

        return querys_.string




@app.route('/api/v1/GET/<auth>/all/', methods =['GET','POST'])

def api_get_all_questions(auth):

    querys = Question.query.all()
    all_questions=''
    length= len(querys)
    for i in range(length):
        all_questions += querys[i].string+ "                           "+str(querys[i].idq)+"                                   "

    return all_questions



@app.route('/api/v1/POST/<question>/', methods =['GET','POST'])

def api_post_question(question):
    if question is not None:


        rand= randint(1000000,9000000000)
        post=Question()
        post.idq=rand
        post.string=question
        db.session.add(post)
        db.session.commit()

        return "Successfuly Posted"


    else:

        return " Wrong URI "
@app.route('/favicon.ico')
def favicon():

    return "<!html>{{url_for('static' filename='images/10279_001.jpg')}}</html>"


@app.route('/auth/signup', methods= ['GET','POST'])

def signup():

    form=signup_form()
    if form.validate_on_submit() and request.method =='POST':
        user=User()
        user.name=form.name.data
        user.password= form.password.data
        db.session.add(user)
        try:
            db.session.commit()
            session['name']=form.name.data
            return "succcessfuly created Account"
        except:

            return "Such a username already exist try a different  on"
    else:
        return render_template('signup.html', form=form)
        


@app.route('/auth/login', methods= ['GET', 'POST'])

def login():
    form=signup_form()
    if form.validate_on_submit() and request.method =='POST':
        user= User.query.filter_by(name=form.name.data).first()
        #return user.password
        if user.password == form.password.data:
            session['name']=form.name.data
            return redirect(url_for('index'))
        else:
            return render_template('logintry.html')
    else:
        return render_template('login.html', form=form)

#####################################################################################################################################
#####################################################################################################################################    

# Boot camp Questioner/ Meetup project




@app.route('/api/v1/meetups', methods=['GET'])

def meetupsapi():
    results= Meetup.query.all()
    length= len(results)
    all_meetups=""
    
    for i in range(length):
        all_meetups += results[i].name+ "      "+str(results[i].id_m)+ "    " +results[i].subject + "  "+ results[i].location
    

    return all_meetups



@app.route('/signup_meetups' ,methods =['GET','POST'])

def signnup_meetups():
    form =signup_meetup()
    user= User_meetup()
    if request.method== 'POST':
        if 1:
            user.name=form.firstname.data
            user.password=form.password.data
            user.email=form.email.data
            db.session.add(user)
            db.session.commit()
            return "Account Created"

        


        else:
            return "error creating account"
    else:
        return render_template('signup_meetups.html')



@app.route('/login_meetups_form', methods=['GET','POST'])

def login_meetups():
    form=login_meetup()
    user=User_meetup()
    
    if request.method=='POST':
        if 1:
            query=User_meetup.query.filter_by(name=form.firstname.data).first()
            if query is not None:
                if query.password == form.password.data:
                    session['name']=form.firstname.data
                    return "success"
                else:
                    return "wrong password or user name"

                
            else:
                return "wrong password or user name"

        else:
            return redirect(url_for('login_meetups_form'))
            
    else:
        return redirect(url_for('login_meetups_form'))


@app.route('/login_meetups', methods= ['GET'])

def login_meetups_form():

    return render_template('sign.html')



@app.route('/meetups/<id>', methods =['GET','POST'])
def meet_ups(id):
    query= Meetup.query.filter_by(id_m=id).first()
    return query.name





@app.route('/create_meetup', methods =['POST', 'GET'])

def create_meetup():
    form = meetup_form()
    var=1
    meetup= Meetup()
    user=session.get('name')

    if request.method=='POST':
        if var:
            meetup.name=form.name.data
            meetup.location= form.location.data
            meetup.subject = form.subject.data
            db.session.add(meetup)
            db.session.commit()
            return "<h1>Successfuly posted </h1>"+ user

        else:
            return "<h1>error updating database </h1>"
        
        
    else:
        return request.method        

    


	
if __name__=='__main__':
    app.run( debug= True )
