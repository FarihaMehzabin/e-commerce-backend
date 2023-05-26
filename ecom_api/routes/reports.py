import traceback
from views import Views

views = Views()

def report_routes(app):
    
    # returns report on total value spent by each user
    @app.route("/users/total-value-spent", methods=["GET"])
    def total_val_spent():
        try:
            return views.total_value_spent()
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    # returns top purchased products from the database
    @app.route("/users/top-purchased-product", methods=["GET"])
    def top_purchased_product():
        try:
            return views.top_purchased_product()
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


    # returns top 10 users who purchased the highest amount of products
    @app.route("/users/top-10-user", methods=["GET"])
    def top_10_user():
        try:
            return views.top_10_user()
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
    
    
     