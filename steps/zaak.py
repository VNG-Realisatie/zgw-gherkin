from behave import *
from requests import request


@given("de zaken-api is beschikbaar")
def step_impl(context):
    response = request("GET", context.ztc_address)
    assert response.status_code == 200
    return


@when("zaken wordt gezocht met de volgende parameters")
def step_impl(context):
    query_param = ""
    for row in context.table:
        query_param = f"?{row['naam']}={row['waarde']}"

    url = f"{context.ztc_address}/zaken{query_param}"
    payload = ""
    headers = {
        "Accept-Crs": "EPSG:4326",
        "Content-Crs": "EPSG:4326",
        "Authorization": f"Bearer {context.token}",
    }

    response = request("GET", url, headers=headers, data=payload)

    context.response = response
    return


@then("heeft de response {number_of_zaken:d} zaak met de volgende gegevens")
def step_impl(context, number_of_zaken):
    response = context.response
    assert response.status_code == 200
    result = response.json()["results"]
    assert len(result) == number_of_zaken
    for row in context.table:
        print(row["waarde"])
        print(result[0].get(row["naam"]))
        assert result[0].get(row["naam"]) == row["waarde"]
    return
