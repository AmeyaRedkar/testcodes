from flask import Flask
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager,jwt_required
from userdb import Signup,Login
from shopdb import Shop

app=Flask(__name__)

api=Api(app)

app.secret_key="shhhhhsh"

jwt=JWTManager(app)


api.add_resource(Signup,"/signup")
api.add_resource(Login,"/login")
api.add_resource(Shop,"/shop")

app.run(debug=True,port=5000)