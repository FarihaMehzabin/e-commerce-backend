import traceback
from flask import jsonify, request
from ecom_api.db.product_db import ProductDB
from ecom_api.services.company.product import ProductService


product_service = ProductService()


def products_routes(app):
    @app.route("/company/pull-all-products", methods=["GET"])
    def pull_all_products():
        """
        Fetch all products and return them as JSON.
        """
        try:
            product_db = ProductDB()
            products = product_db.get_products()

            return jsonify(products=products)

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    @app.route("/company/<id>/products", methods=["GET"])
    def show_company_products(id):
        """
        Fetch and return the products for a specific company.
        """
        try:
            products = product_service.get_products_by_company(id)

            if products is None:
                return jsonify(error="No products found for company")

            return jsonify(products=products)

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    @app.route("/company/products/<product_id>", methods=["GET"])
    def get_product(product_id):
        """
        Fetch and return the product data for a specific product.
        """
        # Fetch the product data from the database
        product = product_service.get_product_by_id(product_id)

        # Return the product data as JSON
        return jsonify(product=product)

    @app.route("/company/<company_id>/products/add", methods=["POST"])
    def add_product(company_id):
        """
        Add a new product for a specific company and return the product ID.
        """
        try:
            new_product_data = request.get_json()

            product_id = product_service.add_product(new_product_data, company_id)

            if product_id is None:
                return jsonify(error="Failed to add the product")

            return jsonify(message="Product added successfully", product_id=product_id)
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    @app.route("/company/products/<product_id>/edit", methods=["PUT"])
    def edit_product(product_id):
        """
        Update the product data for a specific product and return a success message.
        """
        try:
            updated_product_data = request.get_json()

            success = product_service.update_product(product_id, updated_product_data)

            if not success:
                return jsonify(error="Failed to update the product")

            return jsonify(message="Product updated successfully")
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    @app.route("/company/products/<product_id>/delete", methods=["DELETE"])
    def delete_product(product_id):
        """
        Delete a specific product and return a success message.
        """
        try:
            success = product_service.delete_product(product_id)
            if not success:
                return jsonify(error="Failed to delete the product")

            return jsonify(message="Product deleted successfully")
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
