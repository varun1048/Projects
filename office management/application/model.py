from . import app
from flask_pymongo import PyMongo

app.config['MONGO_URI'] = "mongodb+srv://varun:i49ejjA159JquAUH@cluster.eji5z.mongodb.net/Boss"
cloud = PyMongo(app)
db = cloud.db
print(" * Data Base connected")

# employee_schema={
        
#         "name": form['name'],
#         "voter_id":None,
#         "father_name":None,
#         "dfb":None,   
#         "address":None,
        
        
#         "number":None,
#         "polling_booth":None,
        
        
        
        
        
        
#         "salary":False,
#         "manager_id":"",
#         "manager_name":"",
#         "attendance":False,
#         "area":False
        
#         }
        

        
# manager_schema = {
#     "_id": {
#         "$oid": "6223c58f9a8449d0884ba820"
#     },
#     "name": "v",
#     "password": "v",
#     "amount": {
#         "$numberInt": "210"
#     },
#     "total_amount": {
#         "$numberInt": "4220"
#     },
#     "salary_list": [{
#         "$oid": "6223c087aa408875df0a84f9"
#     }]
# }


#  uploader =  {
#     "_id": {
#         "$oid": "6223c5da9a8449d0884ba821"
#     },
#     "name": "q",
#     "password": "q",
#     " uploader_ids": [""],
#     "uploader_ids": [{
#         "$oid": "6223bd02488b2cc889509665"
#     }, {
#         "$oid": "6223bda3db749f74f85becf6"
#     }, {
#         "$oid": "6223bdcadb749f74f85becf7"
#     }, {
#         "$oid": "6223bdd7db749f74f85becf8"
#     }, {
#         "$oid": "6223be56db749f74f85becf9"
#     }, {
#         "$oid": "6223bfc2aa408875df0a84f8"
#     }, {
#         "$oid": "6223c087aa408875df0a84f9"
#     }, {
#         "$oid": "6223c4707d5f041ed8f22810"
#     }, {
#         "$oid": "6223c4a47d5f041ed8f22811"
#     }]
# }