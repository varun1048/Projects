from ..model import db
from flask import Blueprint, redirect,render_template,request, url_for
from bson.objectid import ObjectId

boss_blueprint = Blueprint('boss_blueprint', __name__,static_folder='static',template_folder='template')


def console(inner):
    print("\n"*3)
    print(inner)
    print("\n"*3)


@boss_blueprint.route('/')
def boss():
    manager = db['manager'].count_documents({})
    uploader = db['uploader'].count_documents({})
    employee = db["employee"].count_documents({})
    return render_template('boss/index.html',manager =manager,employee=employee,uploader=uploader)


@boss_blueprint.route('/search_list',methods=['GET','POST'])
def search_list():
    if request.method == 'POST':
        form = request.form
        documents = []
        
        
        regex = {'$regex': f'^{form["search"]}', '$options' : 'i'}  
        
        for type_ in ['manager','employee','uploader']:
            
            for obj in db[type_].find({'name': regex} ):
                documents.append(
                {
                    "documents":obj,
                    "type":type_
                })
        
    return render_template('boss/search_list.html', documents = documents)

@boss_blueprint.route('/search_by_type/<string:by_type>')
def search_by_type(by_type:str):
    return render_template('boss/all_people.html', documents =db[by_type].find(),by_type=by_type,count= db[by_type].count_documents({}) )






# @boss_blueprint.route('/salary')
# def salary():
#     return render_template('boss/salary.html')

@boss_blueprint.route('/manager/<_id>')
def manager(_id):
    manager = db['manager'].find_one({'_id':ObjectId(_id)})
    salary_list = db['employee'].find({    '_id':  { "$in" :manager['salary_list']}      })
    return render_template('boss/manager.html',data=manager,salary_list=salary_list)


@boss_blueprint.route('/update_manager/',methods=["POST"])
def update_manager():
    if request.method == 'POST':
        form = request.form
        
        total_amount = int(form['total_amount']) + int(form['amount'])
        amount = int(form['amount']) + int(form['balance_amount'])
        
        
        db['manager'].find_one_and_update(
            {'_id':ObjectId(form['_id'])},
            {'$set':{'amount':amount , 'total_amount':total_amount } }
            )
    return redirect(url_for('boss_blueprint.manager',_id=form['_id']))
        
    # return render_template('boss/manager.html',data=manager)

@boss_blueprint.route('/employee/<_id>')
def employee(_id):
    return render_template('boss/employee.html',data=db['employee'].find_one({'_id':ObjectId(_id)}) ,by_type = "employee")


@boss_blueprint.route('/uploader/<_id>')
def uploader(_id):
    return render_template('boss/uploader.html',data=db['uploader'].find_one({'_id':ObjectId(_id)}),by_type = "uploader")












def manager_bar_room_list()->list:
    managers = []
    
    for manager in db["manager"].find():
        
        attendance_attend = db["employee"].count_documents( {
            "$and":[
                    {"_id":{"$in":manager['salary_list']}},{"attendance":True}    
                ]
            }),
    
        outsider = db["employee"].count_documents({
            "$and":[{"_id":{"$in":manager['salary_list']}},{"attendance":False},{"area":True}]
            })
    
    
    
        tem = {
            "attendance_attend":attendance_attend[0],        
            "attendance_not_attend": len(manager["salary_list"])-attendance_attend[0],
            "outsider":outsider
        }
        
        
        tem.update(manager)
        managers.append(tem)        
    return managers
    


def main_display()->dict:
    total_employee  = db['employee'].count_documents({})
    attend_total = db['employee'].count_documents({'attendance':True})
    attend_salary = db['employee'].count_documents( {"$and":[{'attendance':True} ,{"salary":True}]} )
    
    balance_total = db['employee'].count_documents({'attendance':False})
    balance_salary = db['employee'].count_documents( {"$and":[{'attendance':False} ,{"salary":True} ]} )
    outsider_salary = db['employee'].count_documents( {"$and":[{'attendance':False} , {"area":True} ,{"salary":True}]} )
    outsider_other = db['employee'].count_documents( {"$and":[{'attendance':False} , {"area":True} ]} )
    
    try:
        winner = attend_salary *100 / attend_total
    except:
        winner = 0
    return {
        "total_employee":total_employee,
        "winner" : round(winner) ,
        
        
        "attend":{
            "total":attend_total,
            "salary":attend_salary,
            "other":attend_total - attend_salary  ,
            },
        "balance":{
            "total":balance_total,
            "salary":balance_salary,
            "other":balance_total - balance_salary,
            "outsider_salary":outsider_salary,
            "outsider_other":outsider_other
            },    
    }
    
    
    
    
    
    

@boss_blueprint.route('/bar_room')
def bar_room():

    return render_template('boss/bar_room.html',     
            display=main_display(),
            manager_list = manager_bar_room_list()
        )