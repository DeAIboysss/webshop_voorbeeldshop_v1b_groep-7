from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
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
client = MongoClient()
database = client.huwebshop

from ..recom_functions.recom_personal import get_simmilar_profiles as recom_personal
from ..recom_functions.recom_simple_popular import read_meest_verkocht as recom_simple
from ..recom_functions.recom_behaviour import collect_contentfilter as recom_behaviour
from ..recom_functions.recom_aanbiedingen_4_1 import read_aanbiedingen as recom_aanbieding
from ..recom_functions.recom_aanbeidingen_4_2 import get_promo_products as recom_aanbieding2
from ..recom_functions.connect import connection
from ..recom_functions.recom_price_range import collect_pricerangefilter as recom_similars
import ast #for sepperation of shopping cart tuple

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count,recom_code,session_shoppingcart,curentPID):
        """
        This function represents the handler for GET requests coming in
        through the API.
        :param profileid: The current profile id
        :param count: The number of recommended products
        :param recom_code: The code for witch recommendation is asked by the website
        :param session_shoppingcart: The current content of the shopping cart
        :return: the recommended products
        """
        con, cur = connection('opdracht2_final', 'kip12345')
        if session_shoppingcart != '[]':
            session_shoppingcart = session_shoppingcart.replace('[','').replace(']','')
            session_shoppingcart = list(ast.literal_eval(session_shoppingcart))
            print(session_shoppingcart)
            #print(type(session_shoppingcart),type(session_shoppingcart[0]),type(session_shoppingcart[1]))

        if recom_code == 2:
            prodids = recom_personal(profileid,con, cur)
            print('personal',prodids)
            if prodids == None:
                prodids = recom_behaviour(profileid,cur)
                print('behaviour', prodids)
        elif recom_code == 4:
           prodids = recom_similars(curentPID,con,cur)
        elif recom_code == 6:
            if session_shoppingcart != '[]':
                prodids = recom_aanbieding2(session_shoppingcart,con,cur)
                if prodids == None:
                    prodids = recom_aanbieding(con, cur,session_shoppingcart)
                    print('aanbieding', prodids)
                else:
                    print('aanbieding 2 succes', prodids)


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
api.add_resource(Recom, "/<string:profileid>/<int:count>/<int:recom_code>/<string:session_shoppingcart>/<string:curentPID>")