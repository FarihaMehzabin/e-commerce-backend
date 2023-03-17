import traceback
from flask import jsonify
from db import Db


db = Db()

def products_routes(app): 
    #  Pull registered products to the home page of public users
    @app.route("/company/pull-products", methods=['GET'])
    def pull_products_for_company():
        try:
            products = db.get_products()
            
            return jsonify(products = products)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
        