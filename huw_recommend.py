import ast

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
from recom_functions.recom_personal import get_simmilar_profiles as recom_personal
from recom_functions.recom_simpele_populair import read_meest_verkocht as recom_simple
from recom_functions.recom_behaviour import collect_contentfilter as recom_behaviour
from recom_functions.recom_aanbeidng import read_aanbiedingen as recom_aanbieing
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
        #print(session_shoppingcart)
        con, cur = connection('opdracht2_final', 'kip12345')
        if session_shoppingcart != '[]':
            session_shoppingcart = session_shoppingcart.replace('[','').replace(']','')
            session_shoppingcart = list(ast.literal_eval(session_shoppingcart))
            print(session_shoppingcart)
        #else:
        #     #prodids = simple_recom(con, cur)
        #     print(session_shoppingcart)

        if recom_code == 2:
            prodids = recom_personal(profileid,con, cur)
            print('personal',prodids)
            if prodids == None:
                prodids = recom_behaviour(profileid,cur)
                print('behaviour', prodids)
        elif recom_code == 6:
            prodids = recom_aanbieing(con, cur,session_shoppingcart) #toekomstig komt hier aanbieding
            print('aanbieding', prodids)

        elif recom_code == 8:
            prodids = recom_simple(con,cur)
            print('simpel', prodids)

        if prodids == None:# als 1 van de recommendations niks terug geeft dan komt de simpele in werking.
            prodids = recom_simple(con,cur)
            print('replace_simpel', prodids)

        cur.close()
        con.close()
        return prodids[:count], 200



# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<int:recom_code>/<string:session_shoppingcart>")