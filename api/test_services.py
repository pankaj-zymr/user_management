'''
Created on Nov 14, 2013

@author: manish.meshram
'''
from flask import Flask, jsonify, session, make_response
from flask import request, abort
from pdao import *
from os import urandom
from random import randint

app = Flask(__name__)



@app.route('/login', methods = ['POST'])
def login():
    """Login method"""
    if not request.json:
        abort(400)
    
    username = request.json['username']
    password = request.json['password']
    
    #temporary dictionary which we will send as response
    temp_dict = {}
    
    #getting user credentials object by username and password
    user_cred = get_user_byusername(username,password)
    
    #adding 'id' in temporary dictionary
    temp_dict["id"] = user_cred.id
    
    #adding 'username' in temporary dictionary
    temp_dict["username"] = user_cred.username
    
    #getting user preference object by id
    user_pref = get_user_pref(user_cred.id)
    
    #adding 'color' in temporary dictionary
    temp_dict["color"] = user_pref.color
    
    #getting user role object by id
    user_role = get_user_role(user_cred.id)
    
    #adding 'color' in temporary dictionary
    temp_dict["role"] = user_role.role
    
    return jsonify( { 'user': temp_dict } )


@app.route('/get_users', methods = ['GET'])
def get_users():
    """Method for getting all the users present"""
    user_creds_list = list_all_users()
    
    all_users_list = []
    
    for user_cred in user_creds_list:
        temp_dict = {}
        
        temp_dict['id'] = user_cred.id
        
        user_info = get_user_info(user_cred.id)
        temp_dict['firstname'] = user_info.firstname
        temp_dict['lastname'] = user_info.lastname
        
        user_role = get_user_role(user_cred.id)
        temp_dict['role'] = user_role.role
        
        all_users_list.append(temp_dict)
        
        
    return jsonify( { 'users': all_users_list} )



@app.route('/delete_user/<user_id>', methods = ['DELETE'])
def delet_user(user_id):
    """Method for delete user.Given the name as delet because our DAO layer method name is 
    delete_user"""
    status = delete_user(user_id)
    
    if status == True:
        return "user deleted"
    return "",406


@app.route('/get_user_info/<user_id>', methods = ['GET'])
def get_user_info_api(user_id):
    """Method for getting user_info object of given user_id"""
    user_info = get_user_info(user_id)
    
    #Dictionary for storing info data about required user
    #This list will get sent as a response after converting it into json 
    temp_dict={}
    
    if user_info == False:
        return "",406
    else:
        temp_dict['firstname'] = user_info.firstname
        temp_dict['lastname'] = user_info.lastname
        temp_dict['phone1'] = user_info.phone1
        temp_dict['phone2'] = user_info.phone2
        temp_dict['primary_email'] = user_info.primary_email
        temp_dict['email'] = user_info.email
        temp_dict['address_line1'] = user_info.address_line1
        temp_dict['address_line2'] = user_info.address_line2
        temp_dict['pin'] = user_info.pin
        temp_dict['country'] = user_info.country
        
        return jsonify( {'user_info': temp_dict} )
        

@app.route('/get_user_pref/<user_id>', methods = ['GET'])
def get_user_pref_api(user_id):
    """Method for getting user_pref object """
    user_pref = get_user_pref(user_id)
    
    temp_dict = {}
    
    if user_pref == False:
        return "",406
    else:
        temp_dict['color'] = user_pref.color
        temp_dict['decimal'] = user_pref.decimal
        temp_dict['currency'] = user_pref.currency
        temp_dict['time_format'] = user_pref.time_format
        temp_dict['date_format'] = user_pref.date_format
        
        return jsonify( {'user_pref': temp_dict} )

@app.route('/update_user_info/<user_id>', methods = ['PUT'])
def update_user_info_api(user_id):
    """Method for updating user_info object """
    
    edit_user_info()
    return ""


@app.route('/temp_login', methods = ['POST'])
def temp_login():
    session['dummy']="ghghgh"
    temp_dict={}
    temp_dict["id"] = 7
    temp_dict["username"] = "manish"
    temp_dict["color"] = "Red"
    temp_dict["role"] = "User"
    temp_dict["authentication_id"] = 47575844
    
    return jsonify( { 'user':temp_dict} )

@app.route('/temp_get_users', methods = ['GET'])
def temp_get_users():
    temp_list = []
    
    temp_dict={}
    temp_dict["id"] = 7
    temp_dict["firstname"] = "manish"
    temp_dict["lastname"] = "Green"
    temp_dict["role"] = "User"
    temp_list.append(temp_dict)
    
    temp_dict1={}
    temp_dict1["id"] = 8
    temp_dict1["firstname"] = "admin"
    temp_dict1["lastname"] = "Red"
    temp_dict1["role"] = "Admin"
    temp_list.append(temp_dict1)
    
    return jsonify( { 'users':temp_list} )

@app.route('/clear', methods = ['GET'])
def clear():
    #session.pop('username', None)
    #session.pop('item1', None)
    
    #session['item1'] = 'itismycookie'
    '''
    resp = make_response()
    resp.set_cookie('cook',generatedRandomNo)
    
    return resp
    
    ll = request.cookies.get('sessionID');
    print ll'''
    return "done"

    


@app.route('/aa', methods = ['GET'])
def aa():
    return "workingg"



if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug = True, host="0.0.0.0")