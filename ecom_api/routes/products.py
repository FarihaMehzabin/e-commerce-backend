import traceback
from flask import jsonify



def products_routes(app): 
    #  Pull registered products to the home page of public users
    @app.route("/company/pull-products", methods=['GET'])
    def pull_products_for_company():
        try:
            products = 0
            
            return jsonify(products = products)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
        