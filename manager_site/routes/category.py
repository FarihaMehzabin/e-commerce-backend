import traceback
from flask import request, jsonify, render_template
import requests

def category_routes(app):
    
    @app.route('/manage-categories')
    def manage_categories():
        """
        Render the manage_categories.html template with the list of categories.
        """
        category_list_response = requests.get(
                f"http://127.0.0.1:8080/company/categories"
            )
        
        category_list = category_list_response.json()
        
        print(category_list)
        
        return render_template("manage_categories.html", categories = category_list["category_list"])

    @app.route("/product/manage-category/create", methods=["POST"])
    def add_category():
        """
        Create a new category.

        Request JSON:
        {
            "category_name": "<category_name>"
        }

        Response JSON:
        {
            "message": "<success_message>"
        }
        """
        data = request.get_json()
        category_name = data['category_name']
        
        response = requests.post(
            "http://127.0.0.1:8080/company/add-category",
            json={"category_name": category_name}
        )
        
        res = response.json()
        
        return jsonify({'message': res['message']}), 201

    @app.route("/product/manage-category/edit", methods=["PUT"])
    def edit_category():
        """
        Edit an existing category's name.

        Request JSON:
        {
            "category_name": "<category_name>",
            "new_category_name": "<new_category_name>"
        }

        Response JSON:
        {
            "message": "<success_message>"
        }
        
        """
        data = request.get_json()
        category_name = data['category_name']
        new_category = data['new_category']

        response = requests.put(
            f"http://127.0.0.1:8080/company/categories//{category_name}",
            json={"new_category": new_category},
        )
        
        res = response.json()
        
        return jsonify({'message': res['message']}), 201

    @app.route("/product/manage-category/delete", methods=["DELETE"])
    def delete_category():
        """
        Delete an existing category.

        Request JSON:
        {
            "category_name": "<category_name>"
        }

        Response JSON:
        {
            "message": "<success_message>"
        }
        """
        data = request.get_json()
        category_name = data['category_name']

        response = requests.delete(
            "http://127.0.0.1:8080/company/delete-category/",
            json={"category_name": category_name},
        )
        
        res = response.json()
        
        return jsonify({'message': res['message']}), 201
