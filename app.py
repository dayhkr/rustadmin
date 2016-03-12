#! /usr/bin/env python
# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from rustadmin import RustAdmin
import ast
# Initialize the Flask application
app = Flask(__name__)
# Define a route for the default URL, which loads the form
@app.route('/', methods=['GET','POST'])
def form():
    #cs = RustAdmin(url='192.168.1.137:5678', passwd='swUrUBr2kA')
    #mess = cs.sndcommand(msg='playerlist')
    #players = ast.literal_eval(mess['Message'])

    return render_template('form_submit.html', players=getplayer())

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/rustitem/', methods=['POST'])
def rustitem():
    cs = RustAdmin(url='192.168.1.137:5678', passwd='swUrUBr2kA')
    resourceitem=request.form['rustitem']
    player=request.form['player']
    itemnum=request.form['itemnum']
    mess = cs.sndcommand(msg='inventory.giveto ' + player + ' ' + resourceitem + ' ' + itemnum)
    return render_template('form_submit.html', ritem=resourceitem, mess=mess, players=getplayer())

def getplayer():
    cs = RustAdmin(url='192.168.1.137:5678', passwd='swUrUBr2kA')
    mess = cs.sndcommand(msg='playerlist')
    players = ast.literal_eval(mess['Message'])
    return players
# Run the app :)
if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
  )