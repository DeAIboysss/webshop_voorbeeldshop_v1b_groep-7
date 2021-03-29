from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
# if os.getenv(envvals[0]) is not None:
#     envvals = list(map(lambda x: str(os.getenv(x)), envvals))
#     client = MongoClient(dbstring.format(*envvals))
# else:
client = MongoClient()
database = client.huwebshop 
from recom_functions.recom_personal import get_simmilar_profiles as recom_1
from recom_functions.recom_simpele_populair import read_meest_verkocht as simple_recom
from recom_functions.recom_behaviour import collect_contentfilter as recom_3
from recom_functions.connect import connection

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count,recom_code,session_shoppingcart):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        # randcursor = database.products.aggregate([{ '$sample': { 'size': count } }])
        # prodids = list(map(lambda x: x['_id'], list(randcursor)))
        #prodids = recom_2(con,cur)
        print(session_shoppingcart)
        con, cur = connection('opdracht2_final', 'kip12345')
        if recom_code == 2:
            prodids = recom_1(profileid, con, cur)
        elif recom_code == 4:
            prodids = recom_3(profileid,cur,con)
        elif recom_code == 6:
            prodids = simple_recom(con, cur) #toekomstig komt hier aanbieding

        if prodids == None:# als 1 van de recommendations niks terug geeft dan komt de simpele in werking.
            prodids = simple_recom(con, cur)

        cur.close()
        con.close()
        return prodids[:count], 200



# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<int:recom_code>/<list:session_shoppingcart>")