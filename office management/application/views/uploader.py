from flask import Blueprint, redirect,render_template,request,flash, url_for
from ..model import db
from bson.objectid import ObjectId

def console(inner):
    print("\n"*3)
    print(inner)
    print("\n"*3)

uploader_blueprint = Blueprint('uploader_blueprint', __name__,static_folder='static',template_folder='template')

@uploader_blueprint.route('/',methods=['POST','GET'])
def uploader():
    if request.method == 'POST':
        form = request.form
        data = dict(form) 
        
        try:
            
            data["area"]
            data["area"] = False
        except:
            data["area"] = True

            
        print(data['area'])
        

        data.update({
        "salary":False,
        "manager_id":"",
        "manager_name":"",
        "attendance":False,
        "area":False 
        })
        
        emp = db['employee'].insert_one(data)
       
        
        db['uploader'].update_one(
            {"_id": ObjectId(   form['uploader_id'] ) },
            
            {'$push':   
                {'uploader_ids':ObjectId(emp.inserted_id)}  
                }
            )
        
        flash(f"{form['name']} \tadded ..")
        return render_template('uploader/index.html')
    
    return render_template('uploader/index.html')




# {
#     "_id": {
#         "$oid": "621fca7930fa3a22b8984329"
#     },
#     "name": "viki",
#     "salary": null,
#     "manager_id": null,
#     "manager_name": null
# }

# @uploader_blueprint.route('/employee_list',methods=['GET','POST'])
# def employee_list():
#     find_query = {}
#     if request.method == 'POST':
#         form = request.form
#         find_query = {'name': {'$regex':  form['name']  }} 
#     return render_template('uploader/employee_list.html',data=[ x for x in  db['employee'].find(find_query)])  

@uploader_blueprint.route('/employee/<_id>')
def employee(_id):
    return render_template('uploader/employee.html',data=db['employee'].find_one({'_id':ObjectId(_id)}))


@uploader_blueprint.route('/my_list/<string:uploader_id>')
def my_list(uploader_id):
    uploader   = db['uploader'].find_one({'_id':ObjectId(uploader_id)})
    find_query = {'_id': {'$in':  uploader['uploader_ids']  }} 

    return render_template('uploader/employee_list.html',data=[ x for x in  db['employee'].find(find_query)])  





@uploader_blueprint.route('/bar_room',methods=['GET','POST'])
def bar_room():
    find_query = {"attendance":False}
    if request.method == 'POST':
        form = request.form
        find_query = {'name': {'$regex':  f'^{form["name"]}', '$options' : 'i'} , "attendance":False} 
        # data = db['employee'].find(find_query)
        
    return render_template("uploader/bar_room.html",data = [ emp for emp in db['employee'].find(find_query) ])



@uploader_blueprint.route('/attendance/<string:_id>')
def attendance(_id):
    print(ObjectId(_id))
    db['employee'].find_one_and_update(
        {"_id":ObjectId(_id)},
        {"$set":{"attendance":True}}
        )
    return redirect(url_for("uploader_blueprint.bar_room"))














