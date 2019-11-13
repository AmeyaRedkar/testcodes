from pymongo import MongoClient
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required

class Shop(Resource):

	client=MongoClient("localhost",27017)

	shopdb=client['shop']

	products=shopdb['products']

	itemparser=reqparse.RequestParser()
	itemparser.add_argument("itemname",required=True,help="itemname as key")

	priceparser=reqparse.RequestParser()
	priceparser.add_argument("price",type=float,required=True,help="price as key")

	@classmethod
	def get(cls):
		search=cls.products.find()
		match=[x for x in search]
		return str(match)

	@classmethod
	def post(cls):
		item=cls.itemparser.parse_args()
		search=cls.products.find(item)
		match=[x for x in search]
		return str(match)

	@classmethod
	@jwt_required
	def post(cls):
		item=cls.itemparser.parse_args()
		pricetag=cls.priceparser.parse_args()
		cls.products.insert_one({"itemname":item["itemname"],"price":pricetag["price"]})
		return "new product is inserted..!!"

	@classmethod
	@jwt_required	
	def put(cls):
		item=cls.itemparser.parse_args()
		pricetag=cls.priceparser.parse_args()
		cls.products.update_one(
			{"itemname":item["itemname"]},
			{"$set":{"price":pricetag["price"]}})
		return "product price is updated"

	@classmethod 
	@jwt_required	
	def delete(cls):
		item=cls.itemparser.parse_args()
		cls.products.delete_one({"itemname":item["itemname"]})
		return "product is deleted"