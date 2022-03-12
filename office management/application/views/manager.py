from ..model import db
from flask import Blueprint, redirect,render_template,request,session, url_for
from bson.objectid import ObjectId

manager_blueprint = Blueprint('manager_blueprint', __name__,static_folder='static',template_folder='templates')


def console(inner):
    print("\n"*3)
    print(inner)
    print("\n"*3)
    
def return_manager(inner):
    return db['manager'].find_one( {"_id" :ObjectId(inner)} )
    
    
@manager_blueprint.route('/<string:_id>')
def manager(_id):
    return render_template('manager/index.html',manager=return_manager(_id))



    
@manager_blueprint.route('/employee/<string:_id>/<string:manager_id>')
def employee(_id,manager_id):
    
    employee = db['employee'].find_one({'_id':ObjectId(_id)})
    return render_template('manager/employee.html',data=employee,manager = return_manager(manager_id))  


@manager_blueprint.route('/update_manager/',methods=["POST"])
def update_employee():
    if request.method == 'POST':
        form = request.form
        
        manager =  db['manager'].find_one( {"_id" :ObjectId(form['manager_id'])} )
        amount = int(manager["amount"]) - 10
        arr  =  manager['salary_list']
        arr.append(ObjectId(form['employee_id']))
        db['manager'].find_one_and_update(
            {'_id':ObjectId(form['manager_id'])},
            {'$set':{'amount':amount,"salary_list":arr } })

        db['employee'].find_one_and_update(
            {'_id':ObjectId(form['employee_id'])},
            {'$set':{'salary':True ,"manager_name":manager['name'],"manager_id":manager['_id']} })
        
        
    return redirect(url_for('manager_blueprint.employee',_id=ObjectId(form['employee_id']),manager_id=manager["_id"]))




@manager_blueprint.route('/search_list',methods=['GET','POST'])
def search_list():
        if request.method == 'POST':
            form = request.form

        regex = {'$regex':  f'^{form["search"]}', '$options' : 'i'}
        documents = []
        
        for doc in db['employee'].find( {'name': regex} ):
            documents.append(doc)
        
        console(documents)
        
        return render_template('manager/search_list.html',data = {
            "search_list" : documents,
            "search_count" : len(documents)
        },manager=return_manager(form['manager_id']))


@manager_blueprint.route('/salary_list/<string:manager_id>')
def salary_list(manager_id):
    manager  = return_manager(manager_id)
    data = db['employee'].find({    '_id':  { "$in" :manager['salary_list']}      })
    return render_template("manager/salary_list.html",data=data,manager = manager)














@manager_blueprint.route('/bar_room/<string:manager_id>')
def bar_room(manager_id):
    manager  = return_manager(manager_id)

    data = db['employee'].find(
        {"manager_id":ObjectId(manager_id) , "attendance":False}
        )
        
    return render_template("manager/bar_room.html",data = data,manager=manager)

