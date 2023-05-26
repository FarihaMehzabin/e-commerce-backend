import traceback
from flask import request, jsonify
from ecom_api.services.company.categories import CategoryService
from ecom_api.logger import Logger

category_service = CategoryService()
logger = Logger()

def categories_routes(app): 
    
    @app.route("/company/categories", methods=['POST'])
    def add_category():
        try:
            data = request.get_json()

            category_name = data.get('category_name')
            
            if not category_name:
                return jsonify(error="Category name is missing."), 400

            category_id = category_service.add_category(category_name)

            return jsonify(message="new category added"), 201

        except Exception as err:
            logger.error(f"An unexpected error occurred in add-categories route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500


    @app.route("/company/categories/<string:category_name>", methods=['PUT'])
    def edit_category(category_name):
        """
        Edit an existing category's name.

        Request JSON:
        {
            "new_category_name": "<new_category_name>"
        }

        Response JSON:
        {
            "message": "<success_message>"
        }
        """
        try:
            data = request.get_json()

            new_category = data.get('new_category')
            if not new_category:
                return jsonify(error="New category name is missing."), 400

            message = category_service.edit_category(category_name, new_category)

            return jsonify(message=message), 201

        except Exception as err:
            logger.error(f"An unexpected error occurred in editing-categories route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500


    @app.route("/company/categories/<string:category_name>", methods=['DELETE'])
    def delete_category(category_name):
        """
        Delete an existing category.

        Response JSON:
        {
            "message": "category deleted successfully"
        }
        """
        try:
            category_id = category_service.delete_category(category_name)

            return jsonify(message="category deleted successfully"), 201

        except Exception as err:
            logger.error(f"An unexpected error occurred in deleting-categories route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500


    @app.route('/company/categories', methods=['GET'])
    def get_all_categories():
        """
        Get a list of all categories.

        Response JSON:
        {
            "category_list": [
                {
                    "id": <category_id>,
                    "name": "<category_name>"
                },
                ...
            ]
        }
        """
        try:
            category_list = category_service.category_list()

            return jsonify(category_list=category_list), 201
        
        except Exception as err:
            logger.error(f"An unexpected error occurred in get-all-categories route | Error: {err} | Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An unexpected error occurred. Please contact the support team."}), 500
