from flask import Flask ,render_template, request,url_for,redirect,session,flash
app = Flask(__name__)

from flask_session import Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from .views.manager import manager_blueprint 
from .views.boss import boss_blueprint 
from .views.uploader import  uploader_blueprint
from .views.informer import  informer_blueprint

app.register_blueprint(manager_blueprint,url_prefix='/manager')
app.register_blueprint(boss_blueprint,url_prefix='/boss')
app.register_blueprint(uploader_blueprint,url_prefix='/uploader')   

app.register_blueprint(informer_blueprint,url_prefix='/informer')   




from .model import db
@app.route('/',methods=['POST','GET'])
def login():
    session.clear()
    
    if request.method == 'POST':
        
        form = request.form
        user = db[ form['type'] ].find_one({
            "name":form['name'],
            "password":form['password'],
            })
        
        if user:
            # session["name"] = user['name']  
            # session["_id"] = user['_id']  
            # session["amount"] = user['amount']  
            
            session["user"] = user  
            
            session['type'] =  form['type']               
            # print(session['name'])
            
            url =  form['type'] + "_blueprint." + form['type']  
            if form['type'] == "boss":
                return redirect(url_for(url))    
            return redirect(url_for(url,_id=user["_id"]))    

        flash('No data')
        return render_template("login.html")
        
    
    return render_template("login.html")