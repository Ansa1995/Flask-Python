#Importing the Flask Module
from flask import Flask, jsonify, request
#Pymongo supports MongoDB in Python
from flask_pymongo import PyMongo
import urllib.parse


#creating a Flask Object
app = Flask(__name__)

#connecting to database and configuring
app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://richee:'+ urllib.parse.quote('richee@1') + '@ds139960.mlab.com:39960/mydb'

#Connecting Pymongo to MongoDB server
mongo = PyMongo(app)

#route() decoratorhelps in bind URL to a function which indicates path to different pages
#CRUD 
#Read
@app.route('/users', methods = ['GET'])
def get_all_users():
    users = mongo.db.users

    output = []

    for i in users.find():
        output.append({'id' : i['id'], 'name' : i['name'], 'mail' : i['mail'], 'dob' : i['dob'], 'password' : i['password']})
            
    return jsonify(output)

#Create
@app.route('/users', methods=['POST'])
def create_user():

    user = mongo.db.users
    
    data = request.get_json()

    s = user.find_one({'mail':data['mail']})
    if not s:

        new_user = user.insert({'id':data['id'],'name':data['name'],'mail':data['mail'],'dob':data['dob'],'password':data['password']})
        new = user.find_one({'_id' : new_user})
        output = {'id':new['id'],'name':new['name'],'mail':new['mail'],'dob':new['dob'],'password':new['password']}

        return jsonify( output)
    else:
        return jsonify({'msg' : "user already exist"})

#update
@app.route('/users', methods=['PATCH'])
def update_user():
    
    #mail = input('\nEnter email to update\n')
    data = request.get_json()
    s = mongo.db.users.find_one({'mail':data['mail']})
    if s:
        mongo.db.users.update({'mail':data['mail']}, {'$set': {'id':data['id'],'name':data['name'],'dob':data['dob'],'password':data['password']}})
        return jsonify({'ok': True, 'message': 'record updated'}), 200
    else:
        return jsonify({'msg' : "No record found"})

#Delete   
@app.route('/users', methods=['DELETE'])
def delete_usr():
    data = request.get_json()
    mongo.db.users.delete_one({'mail':data['mail']})
    return jsonify({'ok': True, 'message': 'deleted successfully'})
    
    
#For running the app
if __name__ == '__main__':
    app.run(debug=True)

