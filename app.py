#! /usr/bin/env python
# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, redirect
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin
from rustadmin import RustAdmin
import ast
from settings import srvurl,srvpasswd, contentcode
from datetime import timedelta
import hashlib
from itsdangerous import URLSafeTimedSerializer

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "password"
#Login_serializer used to encryt and decrypt the cookie token for the remember
#me option of flask-login
login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager=LoginManager()
#login_manager.init_app(app)

class User(UserMixin):
    """
    User Class for flask-Login
    """
    def __init__(self, userid, password):
        self.id = userid
        self.password = password

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(userid):
        """
        Static method to search the database and see if userid exists.  If it
        does exist then return a User Object.  If not then return None as
        required by Flask-Login.
        """
        #For this example the USERS database is a list consisting of
        #(user,hased_password) of users.
        for user in USERS:

            if user[0] == userid:
                return User(user[0], user[1])
        return None

def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    m = hashlib.md5()
    salted_password = password + app.secret_key
    m.update(salted_password)
    return m.hexdigest()

@login_manager.user_loader
def load_user(userid):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    return User.get(userid)

@login_manager.token_loader
def load_token(token):

    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    #Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)

    #Find the User
    user = User.get(data[0])

    #Check Password and return user or None
    if user and data[1] == user.password:
        return user
    return None

@app.route("/logout/", methods=['POST'])
def logout():
    """
    Web Page to Logout User, then Redirect them to Index Page.
    """
    logout_user()
    return redirect("/")

# Define a route for the default URL, which loads the form
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.get(request.form['username'])

        #If we found a user based on username then compare that the submitted
        #password matches the password in the database.  The password is stored
        #is a slated hash format, so you must hash the password before comparing
        #it.
        if user and hash_pass(request.form['password']) == user.password:
            print "Sweet"
            login_user(user, remember=True)
            return redirect("/rustitem")

    return render_template("login.html")
# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/rustitem/', methods=['GET','POST'])
@login_required
def rustitem():
    error = ''
    mess = ''
    if request.method == "POST":
        cs = RustAdmin(url=srvurl, passwd=srvpasswd)
        atire=request.form['atire']
        food=request.form['food']
        tool=request.form['tool']
        misc=request.form['misc']
        construction=request.form['construction']
        iitems=request.form['items']
        medical=request.form['medical']
        weapons=request.form['weapons']
        trap=request.form['trap']
        ammo=request.form['ammunition']
        resource=request.form['resources']
        #toolitem=request.form['titem']
        player=request.form['player']
        itemnum=request.form['itemnum']
        if player == 'None':
            error = 'Please Choose a Player'
        else:
            if resource != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + resource + ' ' + itemnum)
                error = mess['Message']
            elif tool != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + tool + ' ' + itemnum)
                error = mess['Message']
            elif atire != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + atire + ' ' + itemnum)
                error = mess['Message']
            elif food != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + food + ' ' + itemnum)
                error = mess['Message']
            elif misc != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + misc + ' ' + itemnum)
                error = mess['Message']
            elif construction != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + construction + ' ' + itemnum)
                error = mess['Message']
            elif iitems != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + iitems + ' ' + itemnum)
                error = mess['Message']
            elif medical != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + medical + ' ' + itemnum)
                error = mess['Message']
            elif weapons != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + weapons + ' ' + itemnum)
                error = mess['Message']
            elif trap != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + trap + ' ' + itemnum)
                error = mess['Message']
            elif ammo != 'None':
                mess = cs.sndcommand(msg='inventory.giveto "' + player + '" ' + ammo + ' ' + itemnum)
                error = mess['Message']
            else:
                error = "Please Choose an Item"

        return render_template('form_submit.html',
                               itmlist=contentcode(),
                               mess=mess,
                               players=getplayer(),
                               status=getstatus(),
                               console=getconsole(),
                               error=error)
    else:
        cs = RustAdmin(url=srvurl, passwd=srvpasswd)
        #mess = cs.sndcommand(msg='playerlist')
        #players = ast.literal_eval(mess['Message'])

        return render_template('form_submit.html',
                               itmlist=contentcode(),
                               players=getplayer(),
                               status=getstatus(),
                               console=getconsole())
def getplayer():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    mess = cs.sndcommand(msg='playerlist')
    players = ast.literal_eval(mess['Message'])
    return players

def getconsole():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    mess = cs.sndcommand(msg='console.tail')
    console = ast.literal_eval(mess['Message'])
    return console

def getstatus():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    return cs.sndcommand(msg='global.status')
# Run the app :)
# Need to add keyboard interrupt and close connections
if __name__ == '__main__':
    # Need a real user pass system
    USERS = (("test", hash_pass("password")),("test1", hash_pass("pass1")))

    #Change the duration of how long the Remember Cookie is valid on the users
    #computer.  This can not really be trusted as a user can edit it.
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
    #Tell the login manager where to redirect users to display the login page
    login_manager.login_view = "/"
    #Setup the login manager.
    login_manager.setup_app(app)

    #Run the flask Development Server

    app.run(host="0.0.0.0", port=int("80"), debug=True)