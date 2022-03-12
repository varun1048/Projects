from application.views.boss import employee
from ..model import db
from flask import Blueprint, redirect,render_template,request,session, url_for
from bson.objectid import ObjectId

informer_blueprint = Blueprint('informer_blueprint', __name__,static_folder='static',template_folder='templates')

@informer_blueprint.route("/",methods=['GET','POST'])
def employee_list():
    employee =[]
    
    if request.method == 'POST':        
        form = request.form
        if not form["search"] == "" :
            regex = {'$regex': f'^{form["search"]}', '$options' : 'i'}  
            employee =db["employee"].find({'name': regex} )
        
    return render_template("informer/index.html",employee_list= employee)



@informer_blueprint.route('/employee/<string:_id>')
def employee(_id):
    employee = db['employee'].find_one({'_id':ObjectId(_id)})
    return render_template('informer/employee.html',data=employee)  
