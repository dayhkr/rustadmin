#! /usr/bin/env python
# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from rustadmin import RustAdmin
import ast
from settings import *

# Initialize the Flask application
app = Flask(__name__)
# Define a route for the default URL, which loads the form
@app.route('/', methods=['GET','POST'])
def form():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    #mess = cs.sndcommand(msg='playerlist')
    #players = ast.literal_eval(mess['Message'])

    return render_template('form_submit.html', players=getplayer(), status=getstatus())

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/rustitem/', methods=['GET','POST'])
def rustitem():
    if request.method == "POST":
        cs = RustAdmin(url=srvurl, passwd=srvpasswd)
        resourceitem=request.form['rustitem']
        player=request.form['player']
        itemnum=request.form['itemnum']
        mess = cs.sndcommand(msg='inventory.giveto ' + player + ' ' + resourceitem + ' ' + itemnum)
        print mess['Message']
        return render_template('form_submit.html', ritem=resourceitem, mess=mess, players=getplayer(), status=getstatus())
    else:
        cs = RustAdmin(url=srvurl, passwd=srvpasswd)
        #mess = cs.sndcommand(msg='playerlist')
        #players = ast.literal_eval(mess['Message'])

        return render_template('form_submit.html', players=getplayer(), status=getstatus())
def getplayer():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    mess = cs.sndcommand(msg='playerlist')
    players = ast.literal_eval(mess['Message'])
    return players

def getstatus():
    cs = RustAdmin(url=srvurl, passwd=srvpasswd)
    return cs.sndcommand(msg='global.status')
# Run the app :)
# Need to add keyboard interrupt and close connections
if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
  )