from behave import *


@step("de zaken-api is beschikbaar")
def step_impl(context):
    response = context.client.zaken.check_available()
    assert response.status_code == 200
    return


@step("zaken wordt gezocht met de volgende parameters")
def step_impl(context):
    query_param = ""
    for row in context.table:
        query_param = f"?{row['naam']}={row['waarde']}"

    response = context.client.zaken.search_zaak(params=query_param)
    context.response = response
    return


@step("heeft de response {number_of_zaken:d} zaak met de volgende gegevens")
def step_impl(context, number_of_zaken):
    response = context.response
    assert response.status_code == 200
    result = response.json()["results"]
    assert len(result) == number_of_zaken
    for row in context.table:
        assert result[0].get(row["naam"]) == row["waarde"]
    return


@step("er wordt een valide zaak aangemaakt met {archief_status}")
def step_impl(context, archief_status):
    """
    :type context: behave.runner.Context
    :type archief_status: str
    """
    context.flow.zaken(archief_status)


@step("is er een zaak aangemaakt met statuscode {status_code:d} terug")
def step_impl(context, status_code):
    """
    :type context: behave.runner.Context
    """
    response = context.flow.zaak
    assert response.status_code == status_code


@step("is de zaak terug te vinden")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200
    assert resp.json()["uuid"] == uuid
