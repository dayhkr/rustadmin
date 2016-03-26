#! /usr/bin/env python

from flask import Flask, render_template, request, url_for, redirect
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin
from rustadmin import RustAdmin
import ast
from settings import srvurl, srvpasswd, contentcode, mode
from datetime import timedelta
import hashlib
from itsdangerous import URLSafeTimedSerializer

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "password"

login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager = LoginManager()


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

        :param userid: Get User info
        :return:
        """
        for user in USERS:

            if user[0] == userid:
                return User(user[0], user[1])
        return None


def hash_pass(password):
    """

    :param password: Unhashed password
    :return: hashed password string
    """
    m = hashlib.md5()
    salted_password = password + app.secret_key
    m.update(salted_password)
    return m.hexdigest()


@login_manager.user_loader
def load_user(userid):
    """

    :param userid: Id for the usernae
    :return: Username
    """
    return User.get(userid)


@login_manager.token_loader
def load_token(token):

    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)

    # Find the User
    user = User.get(data[0])

    # Check Password and return user or None
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


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.get(request.form['username'])

        if user and hash_pass(request.form['password']) == user.password:
            print "Sweet"
            login_user(user, remember=True)
            return redirect("/rustitem")
        else:
            error = "Invalid Username or Password"
            # Figure out how to reset the page and then display the error
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route('/rustitem/', methods=['GET', 'POST'])
@login_required
def rustitem():
    error = ''
    mess = ''
    if request.method == "POST":
        cs = RustAdmin(url=srvurl, passwd=srvpasswd)
        atire = request.form['atire']
        food = request.form['food']
        tool = request.form['tool']
        misc = request.form['misc']
        construction = request.form['construction']
        iitems = request.form['items']
        medical = request.form['medical']
        weapons = request.form['weapons']
        trap = request.form['trap']
        ammo = request.form['ammunition']
        resource = request.form['resources']
        player = request.form['player']
        itemnum = request.form['itemnum']
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

        return render_template('form_submit.html',
                               itmlist=contentcode(),
                               players=getplayer(),
                               status=getstatus(),
                               console=getconsole())


def getplayer():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    mess = cs.sndcommand(msg='playerlist')
    if mode != 'test':
        players = ast.literal_eval(mess['Message'])
        return players
    else:
        return '{dayhkr:{"ping": "5"}}'


def getconsole():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    mess = cs.sndcommand(msg='console.tail')
    if mode != 'test':
        console = ast.literal_eval(mess['Message'])
        return console
    else:
        return '{message1:{"stuff": "stuff"}}'


def getstatus():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    return cs.sndcommand(msg='global.status')


if __name__ == '__main__':
    # Need a real user pass system
    USERS = (("test", hash_pass("password")), ("test1", hash_pass("pass1")))
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
    # Tell the login manager where to redirect users to display the login page
    login_manager.login_view = "/"
    # Setup the login manager.
    login_manager.setup_app(app)

    # Run the flask Development Server

    app.run(host="0.0.0.0", port=int("8000"), debug=True)
