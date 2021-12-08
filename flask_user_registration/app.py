import re
from flask.templating import render_template
from models import *
from models import Userlog
from datetime import datetime, timedelta
import hashlib, jwt, werkzeug
import logging
from flask.cli import DispatchingApp
from flask.json import jsonify
from flask import app, request, make_response,Response
from functools import wraps


from datetime import datetime, timedelta
import hashlib, jwt, werkzeug
import logging

from flask.cli import DispatchingApp

from flask.json import jsonify
from flask import app, request, make_response,Response
from flask.templating import render_template
from models import *
from functools import wraps



# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# app.config['SECRET_KEY'] = 'group4'


# decorator for verifying the JWT
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('jwt') 
#         # return 401 if token is not passed
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401
  
#         try:
#             # decoding the payload to fetch the stored details
#             print(token)
#             data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
#             print(data)
#             current_user = data['user']

#         except:
#             return jsonify({
#                 'message' : 'Token is invalid !!'
#             }), 401
#         # returns the current logged in users contex to the routes
#         return  f(current_user, *args, **kwargs)
  
#     return decorated








get_id = Userlog()
print("hello this is id",get_id.id)

@app.route("/test")
def home():
    return "Hello world"


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/adminlogin')
def adminloginPage():
    return render_template('aloginsuccess.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/adminregister')
def adminregisterPage():
    return render_template('aregistersuccess.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')
    

@app.route('/registersuccess', methods = ["POST"])
def registersuccess():
    
    if request.method == "POST":
        # global Ug_id
        # Ug_id += 1
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        #hashing the password before storing
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        print(name)
        entry = Userlog( name = name, email = email,password = hashedPassword)        #how to insert id?????
        db.session.add(entry)
        db.session.commit()

        return render_template('login.html')



@app.route('/adminsuccess', methods = ["POST"])
def Asuccess():
    
    if request.method == "POST":
        # global Ag_id
        # Ag_id += 1
        name = request.form.get('name')
        email = request.form.get('email')

        password = request.form.get('password')
        #hashing the password before storing
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest() 
        print(name)
        entry = Adminlog( name = name, email = email,password = hashedPassword)        #how to insert id?????
        db.session.add(entry)
        db.session.commit()

        return render_template('admininput.html')



@app.route('/loginsuccess',methods = ["POST"])
def loginsuccess():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        # result = db.session.query(Userdata).filter(Userdata.uname==uname, Userdata.password==hashedPassword)
        # result = db.session.query(Userlog).filter(Userlog.email == email, Userlog.password == hashedPassword)
        

        dict={}
        result = db.session.query(Itemlog)
        print(result)
        for data in result:
            dict[data.id]=[data.title,data.categories,data.link,data.type,data.featured,data.levels]
            
        print(dict)  
        return render_template('output.html',data=dict)  

        
        # for row in result:
        #     if len(row.email)!= 0:          # we got that email and password matching in our db
        #         print("welcome",row.name)
        #         return render_template('output.html')
        data = "wrong credentials"
        return render_template('login.html', data=data)



@app.route('/aloginsuccess',methods = ["POST"])
def Aloginsuccess():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        # result = db.session.query(Userdata).filter(Userdata.uname==uname, Userdata.password==hashedPassword)
        result = db.session.query(Adminlog).filter(Adminlog.email == email, Adminlog.password == hashedPassword)


        for row in result:
            if len(row.email)!= 0:          # we got that email and password matching in our db
                print("welcome",row.name)
                return render_template('admininput.html',data=row.name)
        data = "wrong credentials"
        return render_template('login.html', data=data)




@app.route('/itemsuccess', methods = ["POST"])
# @token_required
def Itemsuccess():
    
    if request.method == "POST":
        # global Ig_id
        # Ig_id += 1
        title = request.form.get('title')
        categories = request.form.get('categories')
        link = request.form.get('link')
        type = request.form.get('type')
        featured = request.form.get('featured')
        level = request.form.get('level')
        entry = Itemlog(title = title, categories = categories,link = link,type=type,featured=featured,levels=level)        #how to insert id?????
        result = db.session.query(Itemlog)
        db.session.add(entry)
        db.session.commit()
        dict={}


        result = db.session.query(Itemlog)
        print(result)
        for data in result:
            dict[data.id]=[data.title,data.categories,data.link,data.type,data.featured,data.levels]
            
        print(dict)  
        return render_template('output.html',data=dict)  



if __name__ == "__main__":
    app.run(debug=True, port=3001)