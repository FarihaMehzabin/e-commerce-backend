import traceback
from flask import jsonify
from ecom_api.db.product_db import ProductDB



def products_routes(app): 
    #  Pull registered products to the home page of public users
    @app.route("/company/pull-products", methods=['GET'])
    def pull_products_for_company():
        try:
            
            product_db = ProductDB()
            products = product_db.get_products()
            
            return jsonify(products = products)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
        