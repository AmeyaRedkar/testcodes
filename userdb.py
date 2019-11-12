from pymongo import MongoClient
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token

client=MongoClient('localhost',27017)

database=client['userdb']

collection= database['login_signup']


class Signup(Resource):
	userparse=reqparse.RequestParser()
	userparse.add_argument('username',required=True,help="This field require key as username")
	passwordparse=reqparse.RequestParser()
	passwordparse.add_argument("password",required=True,help="This field require key as password")

	@classmethod 
	def post(cls):
		user= cls.userparse.parse_args()
		password=cls.passwordparse.parse_args()
		
		search=collection.find({"$and":[{"username":user,"password":password}]})
		list1=[x for x in search]
	
		for match in list1:
			if match["username"]==user and match["password"]==password:
				return "username {} and password {} already exist".format(user['username'],password['password'])
		
		
		entry={"username":user,"password":password}

		collection.insert(entry)

		return "Username is  created"

	

class Login(Resource):

	userparse=reqparse.RequestParser()
	userparse.add_argument('username',required=True,help="This field require key as username")

	passwordparse=reqparse.RequestParser()
	passwordparse.add_argument("password",required=True,help="This field require key as password")
	
	@classmethod
	def post(cls):

		user= cls.userparse.parse_args()
		password=cls.passwordparse.parse_args()
		search=collection.find({"$and":[{"username":user,"password":password}]})
		list1=[x for x in search]
	
		for match in list1:
			if match["username"]==user and match["password"]==password:
				access_token=create_access_token(identity=match["username"])
				refresh_token=create_refresh_token(match["username"])


				return {

				"access":access_token,
				"refresh":refresh_token
				},200

		return "Signup, no username {} and password {} exist".format(user['username'],password['password'])