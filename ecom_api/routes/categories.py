import traceback
from flask import request, jsonify
from categories import Category


category = Category()


def categories_routes(app): 
    
    @app.route("/company/add-category/<category_name>", methods=['GET'])
    def add_category(category_name):
        try:
            category_id = category.add_category(category_name)
            
            return jsonify(message = "new category added")
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    # edit existing category in the category table
    # returns edited category name 
    @app.route("/company/edit-category/", methods=['POST'])
    def edit_category():
        try:
            
            data = request.get_json()
            
            category_name = data['category_name']
            
            new_category_name = data['new_category_name']
            
            message = category.edit_category(category_name, new_category_name)
            
            return jsonify(message = message)
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            

    # delete existing category
    @app.route("/company/delete-category/", methods=['POST'])
    def delete_category():
        try:
            
            data = request.get_json()
            
            category_name = data['category_name']
            
            category_id = category.delete_category(category_name)
            
            return jsonify(message = "category deleted successfully")
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            

    @app.route('/get-all-category', methods=['GET'])
    def get_all_category():
        
        category_list = category.category_list()
        
        return jsonify(category_list = category_list)
