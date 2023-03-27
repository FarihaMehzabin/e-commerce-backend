import traceback
from flask import request, jsonify
import requests

def category_routes(app):
    
    @app.route('/manage-categories')
    def manage_categories():
        
        category_list_response = requests.get(
                f"http://127.0.0.1:8080/get-all-category"
            )
        
        category_list = category_list_response.json()
        
        return render_template("manage_categories.html", categories = category_list["category_list"])





    # todo Product category manage (create/edit/delete)

    # View product list to edit
    # Choose a product to change the category
    # View product with the current category and list of categories available
    # can create a new category
    # can edit a category
    # can delete a category

    # creating categories 
    @app.route("/product/manage-category/create", methods=["GET", "POST"])
    def create_category():

        # Get the JSON data from the request
        data = request.get_json()

        # Extract the category name from the JSON data from frontend
        category_name = data['category_name']
        
        # add to category table
        response = requests.get(
                f"http://127.0.0.1:8080/company/add-category/{category_name}"
            )
        
        # get category id from the response
        res = response.json()
        
        # Return a response indicating success
        return jsonify({'message': res['message']}), 201
        

    # Editing existing category
    @app.route("/product/manage-category/edit", methods=["GET", "POST"])
    def edit_category():

        # Get the JSON data from the request
        data = request.get_json()

        category_name = data['category_name']
        new_category_name = data['new_category_name']

        
        response = requests.post(
            "http://127.0.0.1:8080/company/edit-category/",
            json={"category_name": category_name, "new_category_name": new_category_name},
        )
        
        res = response.json()
        
        # Return a response indicating success
        return jsonify({'message': res['message']}), 201

    # Deleting existing category
    @app.route("/product/manage-category/delete", methods=["GET", "POST"])
    def delete_category():

        # Get the JSON data from the request
        data = request.get_json()

        category_name = data['category_name']

        # Change the URL to match your API
        response = requests.post(
            "http://127.0.0.1:8080/company/delete-category/",
            json={"category_name": category_name},
        )
        # get category id from the response
        res = response.json()
        
        # Return a response indicating success
        return jsonify({'message': res['message']}), 201