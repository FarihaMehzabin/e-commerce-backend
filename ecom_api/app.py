from flask import Flask, jsonify
import threading
# from ecom_api.routes.reports import report_routes
from ecom_api.routes.public_users import public_users_routes
from ecom_api.routes.company_users import company_users_routes
from ecom_api.routes.categories import categories_routes
from ecom_api.routes.products import products_routes


config = {
    "DEBUG": True,  # some Flask specific configs
}

app = Flask(__name__)

# report_routes(app)
public_users_routes(app)
company_users_routes(app)
categories_routes(app)
products_routes(app)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)