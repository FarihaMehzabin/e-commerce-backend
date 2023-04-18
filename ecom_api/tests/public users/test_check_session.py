import pytest
from flask_api import status
import json
from ecom_api.models.data_table_models.company.check_company_session_result import CheckCompanySessionResultDataModel

def test_check_cookie_validity_valid_session(client, mocker):
    guid = "sample-guid"

    mocker.patch(
        "ecom_api.services.company.company_session.CompanySessionService.check_session_comp",
        return_value=CheckCompanySessionResultDataModel(True, "Test Company"),
    )

    response = client.post(f"/company/check-cookie-validity/{guid}")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["session_validity"] == True
    assert json_data["company_name"] == "Test Company"


def test_check_cookie_validity_invalid_session(client, mocker):
    guid = "sample-guid"

    mocker.patch(
        "ecom_api.services.company.company_session.CompanySessionService.check_session_comp",
        return_value=CheckCompanySessionResultDataModel(False, "No company present"),
    )

    response = client.post(f"/company/check-cookie-validity/{guid}")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["session_validity"] == False
    assert json_data["company_name"] == "No company present"
