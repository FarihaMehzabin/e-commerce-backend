import traceback
from flask import request, jsonify


# Import request data models
from models.data_table_models.company.company_login_request import (
    CompanyLoginRequestDataModel,
)
from models.data_table_models.company.company_signup_request import (
    CompanySignupRequestDataModel,
)

# Import response data models
from models.response_models.company.check_company_session import (
    CheckCompanySessionResponseModel,
)
from models.response_models.company.company_login import CompanyLoginResponseModel
from models.response_models.company.company_signup import CompanySignupResponseModel
from models.response_models.company.create_company_session import (
    CreateCompanySessionResponseModel,
)

# Import services
from services.company.company_login import CompanyLoginService
from services.company.company_session import CompanySessionService
from services.company.company_signup import CompanySignupService


signup_service = CompanySignupService()
login_service = CompanyLoginService()


def company_users_routes(app):
    @app.route("/company/user/signup", methods=["POST"])
    def comp_sign_up():

        company_data = CompanySignupRequestDataModel(request.get_json())

        signup_response = signup_service.comp_signup(company_data)

        response_data = CompanySignupResponseModel(signup_response)

        return jsonify(response_data.to_dict())

    @app.route("/company/user/login", methods=["POST"])
    def comp_login():

        company_data = CompanyLoginRequestDataModel(request.get_json())

        login_response = login_service.comp_login(company_data)

        response_data = CompanyLoginResponseModel(login_response)

        return jsonify(response_data.to_dict())

    @app.route("/company/create-session/<comp_id>", methods=["POST"])
    def create_session_comp(comp_id):

        response = CompanySessionService.create_session(comp_id)

        response_data = CreateCompanySessionResponseModel(response.guid)

        return jsonify(response_data.to_dict())

    @app.route("/company/check-cookie-validity/<guid>", methods=["POST"])
    def check_cookie_validity_comp(guid):
        try:
            response = CompanySessionService.check_session_comp(guid)

            response_data = CheckCompanySessionResponseModel(
                response.session_valid, response.company_name
            )

            return jsonify(response_data.to_dict())

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
