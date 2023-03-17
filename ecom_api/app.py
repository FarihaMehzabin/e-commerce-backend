from flask import Flask
from routes.reports import report_routes
from routes.public_users import public_users_routes
from routes.company_users import company_users_routes
from routes.categories import categories_routes
from routes.products import products_routes

config = {
    "DEBUG": True,  # some Flask specific configs
}

app = Flask(__name__)

report_routes(app)
public_users_routes(app)
company_users_routes(app)
categories_routes(app)
products_routes(app)

            
app.run(host='0.0.0.0', port=8080)