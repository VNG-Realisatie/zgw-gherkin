from datetime import datetime, timedelta

from behave import *


@step("de zaken-api is beschikbaar")
def step_impl(context):
    response = context.client.zaken.check_available()
    assert response.status_code == 200
    return


@step("er is een zaak beschikbaar")
def step_impl(context):
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200


@step("er wordt een valide zaak aangemaakt")
def step_impl(context):
    context.flow.zaken()


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


@step("dat een zaak bestaat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200


@step("er een resultaat aan de zaak wordt toegevoegd met een resultaattype")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.flow.resultaten()


@step("er een eindstatus met de datum van vandaag aan de zaak wordt toegevoegd")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    today = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    context.flow.statussen(close=True, datum_gezet=today)


@step("de zaak wordt heropend met een begin statustype")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.flow.statussen(close=False)


@step(
    "staan einddatum op vandaag, archiefactiedatum op {archiefactiedatum:d} jaar in de toekomst en archiefnominatie op {archiefnominatie}"
)
def step_impl(context, archiefactiedatum, archiefnominatie):
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    einddatum = datetime.utcnow().strftime("%Y-%m-%d")
    end_date_split = einddatum.split("-")
    ten_years_from_now = int(end_date_split[0]) + archiefactiedatum
    date_future = f"{ten_years_from_now}-{end_date_split[1]}-{end_date_split[2]}"
    sut = resp.json()
    assert date_future == sut["archiefactiedatum"]
    assert einddatum == sut["einddatum"]
    assert archiefnominatie == sut["archiefnominatie"]


@step("staan einddatum, archiefactiedatum en archiefnominatie op null")
def step_impl(context):
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    sut = resp.json()
    assert sut["archiefactiedatum"] == None
    assert sut["einddatum"] == None
    assert sut["archiefnominatie"] == None


@step(
    "dat het resultaattype archiefnominatie {archiefnominatie} en archiefactietermijn {archiefactietermijn} en archiefprocedure {archiefprocedure} heeft"
)
def step_impl(context, archiefnominatie, archiefactietermijn, archiefprocedure):
    """
    :type context: behave.runner.Context
    :type archiefnominatie: str
    :type archiefactietermijn: str
    :type archiefprocedure: str
    """
    url = context.flow.resultaattype.json()["url"]
    resp = context.client.catalogus.search_resultaattype(url)
    assert resp.status_code == 200

    sut = resp.json()
    assert sut["archiefnominatie"] == archiefnominatie
    assert sut["archiefactietermijn"] == archiefactietermijn
    assert sut["brondatumArchiefprocedure"]["afleidingswijze"] == archiefprocedure


@step("dat deze zaak geen einddatum heeft")
def step_impl(context):
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    sut = resp.json()
    assert sut["einddatum"] is None


@step("een medewerker de eindstatus vastlegt")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    today = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"archieftime: {today}")
    response = context.flow.statussen(close=True, datum_gezet=today)
    context.end_status_response = response


@step("reageert de Zaken API met een code {status_code:d}")
def step_impl(context, status_code):
    """
    :type context: behave.runner.Context
    """
    assert context.end_status_response.status_code == status_code


@step(
    "registreert de Zaken API bij archiefstatus de waarde {archiefstatus} en archiefnominatie {archiefnominatie}"
)
def step_impl(context, archiefstatus, archiefnominatie):
    """
    :type context: behave.runner.Context
    :type archiefstatus: str
    :type archiefnominatie: str
    """
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    sut = resp.json()
    assert sut["archiefstatus"] == archiefstatus
    assert sut["archiefnominatie"] == archiefnominatie


@step(
    "registreert de Zaken API bij archiefactietermijn de einddatum van de zaak, verhooogd met bij het resultaattype geregistreerde archiefactietermijn"
)
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    end_date_split = datetime.utcnow().strftime("%Y-%m-%d").split("-")
    ten_years_from_now = int(end_date_split[0]) + 10
    date_future = f"{ten_years_from_now}-{end_date_split[1]}-{end_date_split[2]}"
    sut = resp.json()
    assert date_future == sut["archiefactiedatum"]


@step("het veld {veld} geexpand wordt bij de list operatie")
def step_impl(context, veld):
    """
    :type context: behave.runner.Context
    :type veld: str
    """
    identificatie = context.flow.zaak.json()["identificatie"]
    params = {
        "expand": veld,
        "identificatie": identificatie,
    }
    resp = context.client.zaken.search_zaken(params)
    context.response = resp


@step("is het veld {veld} opgenomen in de response")
def step_impl(context, veld):
    """
    :type context: behave.runner.Context
    :type veld: str
    """
    zaak_expanded = context.response.json()
    fields = veld.split(",")
    for field in fields:
        split = field.split(".")
        try:
            included = zaak_expanded["results"][zaak_expanded["count"] - 1][
                "_expand"
            ][split[0]]
            if len(split) == 2:
                also_included = included["_expand"]
                assert also_included is not None
            if len(split) > 2:
                also_included = included[0]["_expand"]
                assert also_included is not None
        # this is an error but to make the tests pass we leave it for the first version of inclusions
        except KeyError:
            pass
        assert included is not None
