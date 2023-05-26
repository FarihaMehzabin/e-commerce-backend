import requests, traceback
from flask import render_template, redirect, url_for, request, jsonify
from manager_site.services.application import Application


cache = Application.instance()


def products_routes(app): 
    
    @app.route("/manage-products/<id>", methods=["GET"])
    def show_company_products(id):
        """
        Show the list of products for a given company.
        """
        try:
            data = requests.get(f"http://127.0.0.1:8080/company/{id}/products")
            
            response = data.json()
            
            # print(response)

            if "error" in response:
                return render_template("manage_products.html", error=response["error"], company_id=id)
            else:
                rendered_template = render_template("manage_products.html", products=response["products"]["products"], company_id=id)
                return rendered_template

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


    
    @app.route("/company/products/<product_id>/edit", methods=["GET"])
    def show_edit_product_form(product_id):
        """
        Display the edit product form for a specific product.
        """
        try:
            
            response = requests.get(f"http://127.0.0.1:8080/company/products/{product_id}")

            data = response.json()

            product_data = data["product"]["product"][0]
            
            print(product_data)
            
            category_data = cache.category_repository.get_categories()

            return render_template("edit_product.html", product=product_data, all_categories = category_data)

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")



    @app.route("/company/products/<company_id>/<product_id>/edit", methods=["POST"])
    def edit_product(company_id, product_id):
        """
        Update the product data for a specific product.
        """
        try:
            # Extract the data from the form
            form_data = request.form
            product_data = {
                "name": form_data["name"],
                "brand": form_data["brand"],
                "price": form_data["price"],
                "unit": form_data["unit"],
                "item_weight": form_data["item_weight"],
                "product_description": form_data["product_description"],
                "selected_category_ids": request.form.getlist('categories')
            }
            
            print(product_data)

            # Send the updated product data to the backend
            response = requests.put(f"http://127.0.0.1:8080/company/products/{product_id}/edit", json=product_data)

            if response.status_code == 200:
                return redirect(url_for('show_company_products', id=company_id))
            else:
                error_message = response.json().get("error")
                return render_template("edit_product.html", product_id=product_id, error=error_message)
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")


            
    @app.route("/company/<company_id>/products/add", methods=["GET"])
    def show_add_product_form(company_id):
        """
        Display the add product form for a specific company.
        """
        try:
            category_data = cache.category_repository.get_categories()
            return render_template("add_product.html", company_id=company_id, all_categories = category_data)
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            
    
    @app.route("/company/<company_id>/products/add", methods=["POST"])
    def add_product(company_id):
        """
        Add a new product for a specific company.
        """
        try:
            # Extract the data from the form
            form_data = request.form
            product_data = {
                "name": form_data["name"],
                "brand": form_data["brand"],
                "price": form_data["price"],
                "unit": form_data["unit"],
                "item_weight": form_data["item_weight"],
                "product_description": form_data["product_description"],
                "selected_category_ids": request.form.getlist('categories')
                # Add any other required fields
            }
            
            print(product_data)

            # Send the new product data to the backend
            response = requests.post(f"http://127.0.0.1:8080/company/{company_id}/products/add", json=product_data)

            if response.status_code == 200:
                return redirect(url_for("show_company_products", id=company_id))
            else:
                error_message = response.json().get("error")
                return render_template("add_product.html", error=error_message)
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")

    @app.route("/delete-product/<product_id>", methods=["POST"])
    def delete_product(product_id):
        """
        Delete a specific product.
        """
        try:
            response = requests.delete(f"http://127.0.0.1:8080/company/products/{product_id}/delete")

            if response.status_code != 200:
                return jsonify(error="Failed to delete the product")

            response_data = response.json()
            
            if "error" in response_data:
                return jsonify(error=response_data["error"])

            return jsonify(message= response_data["message"])
        
        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
            return jsonify(error="An error occurred while deleting the product")

            
            




        

