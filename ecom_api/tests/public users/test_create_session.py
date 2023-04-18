from ecom_api.models.data_table_models.company.create_company_session_result import CreateCompanySessionResultDataModel


def test_create_company_session_success(client, mocker):
    comp_id = "1"
    mocked_guid = "12345678-1234-5678-1234-567812345678"
    mocked_create_session_result = CreateCompanySessionResultDataModel(mocked_guid)

    mocker.patch(
        "ecom_api.services.company.company_session.CompanySessionService.create_session",
        return_value=mocked_create_session_result,
    )

    response = client.post(f"/company/create-session/{comp_id}")

    assert response.status_code == 200
    assert response.json == {"guid": mocked_guid}


def test_create_company_session_failure(client, mocker):
    comp_id = "1"

    mocker.patch(
        "ecom_api.services.company.company_session.CompanySessionService.create_session",
        return_value=False,
    )

    response = client.post(f"/company/create-session/{comp_id}")

    assert response.status_code == 500
