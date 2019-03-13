from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from FrData_Setup import Base, FrCompanyName, FurnitureName, FurnitureUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

# Google client_id
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Furnitures"

engine = create_engine('sqlite:///furniture.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)

# creating session
dbSession = sessionmaker(bind=engine)
session = dbSession()
app = Flask(__name__)

# Create anti-forgery state token
vhs = session.query(FrCompanyName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    vhs = session.query(FrCompanyName).all()
    sk = session.query(FurnitureName).all()
    return render_template('login.html',
                           STATE=state, vhs=vhs, sk=sk)
    # return render_template('myhome.html', STATE=state
    # vhs=vhs,sk=sk)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    mainuser1 = FurnitureUser(
        name=login_session['username'], email=login_session['email'])
    session.add(mainuser1)
    session.commit()
    user = session.query(FurnitureUser).filter_by(
        email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(FurnitureUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(FurnitureUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


# Home


@app.route('/')
@app.route('/home')
def home():
    vhs = session.query(FrCompanyName).all()
    return render_template('myhome.html', vhs=vhs)


# Furnitures for admins


@app.route('/FurnitureStore')
def FurnitureStore():
    try:
        if login_session['username']:
            name = login_session['username']
            vhs = session.query(FrCompanyName).all()
            vhbp = session.query(FrCompanyName).all()
            sk = session.query(FurnitureName).all()
            return render_template('myhome.html', vhs=vhs,
                                   vhbp=vhbp, sk=sk, uname=name)
    except:
        return redirect(url_for('showLogin'))


# Showing furnitures based on furniture category


@app.route('/FurnitureStore/<int:gptid>/AllFurnitures')
def showFurnitures(gptid):
    vhs = session.query(FrCompanyName).all()
    vhbp = session.query(FrCompanyName).filter_by(id=gptid).one()
    sk = session.query(FurnitureName).filter_by(
        furniturecompanynameid=gptid).all()
    try:
        if login_session['username']:
            return render_template('showFurnitures.html', vhs=vhs,
                                   vhbp=vhbp, sk=sk,
                                   uname=login_session['username'])
    except:
        return render_template('showFurnitures.html',
                               vhs=vhs, vhbp=vhbp, sk=sk)


# Add New Furniture


@app.route('/FurnitureStore/addFurnitureCogptidmpany', methods=['POST', 'GET'])
def addFurnitureCompany():
    if request.method == 'POST':
        furcompany = FrCompanyName(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(furcompany)
        session.commit()
        return redirect(url_for('FurnitureStore'))
    else:
        return render_template('addFurnitureCompany.html', vhs=vhs)


# Edit Furniture Category


@app.route('/FurnitureStore/<int:gptid>/edit', methods=['POST', 'GET'])
def editFurnitureCategory(gptid):
    editFurniture = session.query(FrCompanyName).filter_by(
        id=gptid).one()
    furcreator = getUserInfo(editFurniture.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if furcreator.id != login_session['user_id']:
        flash("You cannot edit this Furniture Category."
              "This is belongs to %s" % furcreator.name)
        return redirect(url_for('FurnitureStore'))
    if request.method == "POST":
        if request.form['name']:
            editFurniture.name = request.form['name']
        session.add(editFurniture)
        session.commit()
        flash("Furniture Category Edited Successfully")
        return redirect(url_for('FurnitureStore'))
    else:
        # vhs is global variable we can them in entire application
        return render_template('editFurnitureCategory.html',
                               nh=editFurniture, vhs=vhs)


# Delete Furniture Category


@app.route('/FurnitureStore/<int:gptid>/delete', methods=['POST', 'GET'])
def deleteFurnitureCategory(gptid):
    nh = session.query(FrCompanyName).filter_by(id=gptid).one()
    furcreator = getUserInfo(nh.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if furcreator.id != login_session['user_id']:
        flash("You cannot Delete this Furniture Category."
              "This is belongs to %s" % furcreator.name)
        return redirect(url_for('FurnitureStore'))
    if request.method == "POST":
        session.delete(nh)
        session.commit()
        flash("Furniture Category Deleted Successfully")
        return redirect(url_for('FurnitureStore'))
    else:
        return render_template('deleteFurnitureCategory.html', nh=nh, vhs=vhs)


# Add New Furniture Name Details


@app.route('/FurnitureStore/addCompany/addFrDetails/<string:tbname>/add',
           methods=['GET', 'POST'])
def addFrDetails(tbname):
    vhbp = session.query(FrCompanyName).filter_by(name=tbname).one()
    # See if the logged in user is not the owner of furniture
    furcreator = getUserInfo(vhbp.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if furcreator.id != login_session['user_id']:
        flash("You can't add new furniture"
              "This is belongs to %s" % furcreator.name)
        return redirect(url_for('showFurnitures', gptid=vhbp.id))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        model = request.form['model']
        price = request.form['price']
        color = request.form['color']
        furnituredetails = FurnitureName(name=name, description=description,
                                         color=color,
                                         price=price,
                                         model=model,
                                         date=datetime.datetime.now(),
                                         furniturecompanynameid=vhbp.id,
                                         user_id=login_session['user_id'])
        session.add(furnituredetails)
        session.commit()
        return redirect(url_for('showFurnitures', gptid=vhbp.id))
    else:
        return render_template('addFrDetails.html',
                               tbname=vhbp.name, vhs=vhs)


# Edit Furniture details


@app.route('/FurnitureStore/<int:gptid>/<string:gptename>/edit',
           methods=['GET', 'POST'])
def editFurniture(gptid, gptename):
    nh = session.query(FrCompanyName).filter_by(id=gptid).one()
    furnituredetail = session.query(FurnitureName).filter_by(
        name=gptename).one()
    # See if the logged in user is not the owner of furniture
    furcreator = getUserInfo(nh.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if furcreator.id != login_session['user_id']:
        flash("You can't edit this furniture"
              "This is belongs to %s" % furcreator.name)
        return redirect(url_for('showFurnitures', gptid=nh.id))
    # POST methods
    if request.method == 'POST':
        furnituredetail.name = request.form['name']
        furnituredetail.description = request.form['description']
        furnituredetail.color = request.form['color']
        furnituredetail.price = request.form['price']
        furnituredetail.model = request.form['model']
        furnituredetail.date = datetime.datetime.now()
        session.add(furnituredetail)
        session.commit()
        flash("Furniture Edited Successfully")
        return redirect(url_for('showFurnitures', gptid=gptid))
    else:
        return render_template('editFurnitur.html',
                               gptid=gptid, furnituredetail=furnituredetail,
                               vhs=vhs)


# Delte Furniture Edit


@app.route('/FurnitureStore/<int:gptid>/<string:gptename>/delete',
           methods=['GET', 'POST'])
def deleteFurniture(gptid, gptename):
    nh = session.query(FrCompanyName).filter_by(id=gptid).one()
    furnituredetails = session.query(FurnitureName).filter_by(
        name=gptename).one()
    # See if the logged in user is not the owner of furniture
    furcreator = getUserInfo(nh.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if furcreator.id != login_session['user_id']:
        flash("You can't delete this Furniture"
              "This is belongs to %s" % furcreator.name)
        return redirect(url_for('showFurnitures', gptid=nh.id))
    if request.method == "POST":
        session.delete(furnituredetails)
        session.commit()
        flash("Deleted Furniture Successfully")
        return redirect(url_for('showFurnitures', gptid=gptid))
    else:
        return render_template('deleteFurniture.html',
                               gptid=gptid, furnituredetails=furnituredetails,
                               vhs=vhs)


# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Displays Furniture company names and details about their funitures
# Json


@app.route('/FurnitureStore/JSON')
def allFurnituresJSON():
    furniturecategories = session.query(FrCompanyName).all()
    category_dict = [c.regular for c in furniturecategories]
    for c in range(len(category_dict)):
        furnitures = [i.regular for i in session.query(
                 FurnitureName).filter_by(
                     furniturecompanynameid=category_dict[c]["id"]).all()]
        if furnitures:
            category_dict[c]["furnitures"] = furnitures
    return jsonify(FrCompanyName=category_dict)

# Displays Furniture categories with their id and name


@app.route('/FurnitureStore/furnitureCategories/JSON')
def categoriesJSON():
    furnitures = session.query(FrCompanyName).all()
    return jsonify(furnitureCategories=[c.regular for c in furnitures])

# Displays full details of furnitures


@app.route('/FurnitureStore/furnitures/JSON')
def itemsJSON():
    items = session.query(FurnitureName).all()
    return jsonify(furnitures=[i.regular for i in items])

# Displays details of particular furniture category


@app.route('/FurnitureStore/<path:furniture_name>/furnitures/JSON')
def categoryItemsJSON(furniture_name):
    furnitureCategory = session.query(FrCompanyName).filter_by(
        name=furniture_name).one()
    furnitures = session.query(FurnitureName).filter_by(
        furniturecompanyname=furnitureCategory).all()
    return jsonify(furnitureEdtion=[i.regular for i in furnitures])

# Displays details of particular furniture in particular furniture category


@app.route('/FurnitureStore/<path:furniture_name>/<path:edition_name>/JSON')
def ItemJSON(furniture_name, edition_name):
    furnitureCategory = session.query(FrCompanyName).filter_by(
        name=furniture_name).one()
    furnitureEdition = session.query(FurnitureName).filter_by(
           name=edition_name, furniturecompanyname=furnitureCategory).one()
    return jsonify(furnitureEdition=[furnitureEdition.regular])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
