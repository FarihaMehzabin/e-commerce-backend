import traceback
from flask import Flask
from views import Views




config = {
    "DEBUG": True,  # some Flask specific configs
}



app = Flask(__name__)


views = Views()

@app.route("/users/total_value_spent", methods=["GET"])
def total_val_spent():
    try:
        return views.total_value_spent()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top_purchased_product", methods=["GET"])
def top_purchased_product():
    try:
        return views.top_purchased_product()
     
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")

@app.route("/users/top_10_user", methods=["GET"])
def top_10_user():
    try:
        return views.top_10_user()
    
    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")


app.run(host='0.0.0.0', port=8080)