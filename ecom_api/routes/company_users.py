import traceback


from models.data_table_models.company_signup_request import (
    CompanySignupRequestDataModel,
)
from models.data_table_models.company_login_request import CompanyLoginRequestDataModel

from services.company_signup import CompanySignupService
from services.company_login import CompanyLoginService
from services.company_session import CompanySessionService

from models.response_models.company_signup import CompanySignupResponseModel
from models.response_models.company_login import CompanyLoginResponseModel
from models.response_models.create_company_session import (
    CreateCompanySessionResponseModel,
)
from models.response_models.check_company_session import (
    CheckCompanySessionResponseModel,
)


signup_service = CompanySignupService()
login_service = CompanyLoginService()


def company_users_routes(app):
    # company users signup
    @app.route("/company/user/signup/<cname>/<username>/<password>", methods=["GET"])
    def comp_sign_up(cname, username, password):

        # creating a signup data model with the data received from the frontend
        company_data = CompanySignupRequestDataModel(cname, username, password)

        # pass the object to the service
        # using the company signup service model to do db operations and hashing
        # returns a signup response data model
        signup_response = signup_service.comp_signup(company_data)

        # using the response to send reponse model back to the client
        if signup_response.user_created:

            return CompanySignupResponseModel(
                f"New user signed up! Welcome, {username} :)",
                False,
                signup_response.company_id,
            )

        return CompanySignupResponseModel("Username taken. Please try again.", True, 0)

    
    @app.route("/company/user/login/<username>/<password>", methods=["GET"])
    def comp_login(username, password):

        company_data = CompanyLoginRequestDataModel(username, password)

        login_response = login_service.comp_login(company_data)

        if login_response.user_logged:
            return CompanyLoginResponseModel(
                f"Logged in! Welcome, {username} :)", False, login_response.company_id
            )

        return CompanyLoginResponseModel(
            "Invalid Credentials. Please try again.", True, 0
        )

    
    @app.route("/company/create-session/<comp_id>", methods=["GET"])
    def create_session_comp(comp_id):

        response = CompanySessionService.create_session(comp_id)

        return CreateCompanySessionResponseModel(response.guid)

    
    
    @app.route("/company/check-cookie-validity/<guid>", methods=["GET", "POST"])
    def check_cookie_validity_comp(guid):
        try:
            response = CompanySessionService.check_session_comp(guid)

            return CheckCompanySessionResponseModel(
                response.session_valid, response.company_name
            )

        except Exception as err:
            print(traceback.format_exc())
            print(f"{err}")
