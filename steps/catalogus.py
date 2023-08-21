from datetime import datetime

from _datetime import timedelta
from behave import *


@step("de catalogus-api is beschikbaar")
def step_impl(context):
    response = context.client.catalogus.check_available()
    assert response.status_code == 200
    return


@step("de catalogus wordt gezocht met parameters")
def step_impl(context):
    search_responses = []
    response = context.flow.catalogus.json()
    for row in context.table:
        query_param = {row["parameter"]: response[row["parameter"]]}
        resp = context.client.catalogus.search_catalogus(query_arguments=query_param)
        search_responses.append(resp)
    context.search_responses = search_responses


@step("er een nieuwe valide catalogus aangemaakt wordt")
def step_impl(context):
    context.flow.setup_catalogus()
    context.response = context.flow.catalogus
    return


@step("er een valide besluittype aangemaakt wordt")
def step_impl(context):
    context.flow.besluittype()
    return


@step("er een valide informatieobjecttype aangemaakt wordt")
def step_impl(context):
    context.flow.informatieobjecttype()
    return


@step("er een valide deelzaaktype aangemaakt wordt")
def step_impl(context):
    context.flow.deelzaaktype()
    return


@step("er een valide zaaktype aangemaakt wordt")
def step_impl(context):
    context.flow.zaaktype()
    return


@step("er een relatie wordt gelegd tussen het zaaktype en informatieobjecttype")
def step_impl(context):
    context.flow.zaaktype_informatie_relation()
    return


@step("er een valide eigenschap aangemaakt wordt")
def step_impl(context):
    context.flow.eigenschappen()
    return


@step("er een valide resultaattype aangemaakt wordt")
def step_impl(context):
    context.flow.resultaattypen()
    return


@step("er een valide statussen aangemaakt wordt")
def step_impl(context):
    context.flow.statustype_begin_end()
    return


@step("er een valide rol aangemaakt wordt")
def step_impl(context):
    context.flow.roltype()
    return


@step("de benodigde typen worden gepubliceerd")
def step_impl(context):
    context.flow.publish_types()
    return


@step("krijgt de gebruiker de catalogus terug met de juiste informatie")
def step_impl(context):
    responses = context.search_responses
    for response in responses:
        assert response.status_code == 200


@step(
    "er een informatieobjecttype aangemaakt wordt met omschrijving {iot_omschrijving}"
)
def step_impl(context, iot_omschrijving):
    context.flow.informatieobjecttype(iot_omschrijving)


@step("er een besluittype aangemaakt wordt met het informatieobjecttype")
def step_impl(context):
    context.flow.besluittype_with_informatieobjecttype()


@step("er een zaaktype aangemaakt wordt")
def step_impl(context):
    context.flow.zaaktype_list()

@step("er een zaaktype aangemaakt wordt met identificatie en besluittype")
def step_impl(context):
    context.flow.zaaktype_list(add_besluittype=True)


@step(
    "er een valide zaaktypeinformatieobjecttype met zaaktype_url en het informatieobjecttype"
)
def step_impl(context):
    context.flow.zaaktype_informatie_relation()


@step("er een zaaktype wordt aangemaakt met een gerelateerd zaaktype")
def step_impl(context):
    context.flow.zaaktype_list(gerelateerd_zaaktype=True)


@step("er een zaaktype wordt aangemaakt met een deelzaaktype")
def step_impl(context):
    context.flow.zaaktype_list(gerelateerd_zaaktype=False, add_deelzaaktype=True)


@step(
    "het zaaktype met gerelateerd zaaktype opgevraagd wordt verwijst het gerelateerde zaaktype naar het eerste zaaktype"
)
def step_impl(context):
    zaaktypen = context.flow.zaaktypen_list
    for zaaktype in zaaktypen:
        if zaaktype["gerelateerdeZaaktypen"] != []:
            zktype = context.client.catalogus.retrieve_zaaktype(zaaktype["url"])
            z = zktype.json()
            related_zaaktype = z["gerelateerdeZaaktypen"][0]["zaaktype"]
            assert related_zaaktype == zaaktypen[0]["url"]


@step(
    "er een nieuw concept versie zaaktype met zaaktypeidentificatie van het gerelateerde zaaktype wordt aangemaakt"
)
def step_impl(context):
    first_zaaktype_id = context.flow.zaaktypen_list[0]["identificatie"]
    resp = context.flow.zaaktype_with_return(identificatie=first_zaaktype_id)
    assert resp.status_code == 201
    context.updated_zaaktype = resp.json()


@step("deze zaaktypen worden gepubliceerd")
def step_impl(context):
    zaaktypen = context.flow.zaaktypen_list
    for zaaktype in zaaktypen:
        context.client.catalogus.publish_type(reference_url=zaaktype["url"])


@step("het gerelateerde zaaktype een datum van vandaag krijgt")
def step_impl(context):
    old_zaaktype_url = context.flow.zaaktypen_list[1]["url"]
    old_zaaktype_id = old_zaaktype_url.split("/")[-1]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    context.flow.update_zaaktype_with_geldigheid(
        uuid=old_zaaktype_id, geldigheid=timestamp
    )


@step("het nieuwe concept wordt gepubliceerd")
def step_impl(context):
    zaaktype = context.updated_zaaktype
    context.client.catalogus.publish_type(reference_url=zaaktype["url"])


@step("het zaaktype opgevraagd word")
def step_impl(context):
    zaaktypen = context.flow.zaaktypen_list
    url = zaaktypen[0]["url"]
    td = timedelta(days=5)
    d = datetime.utcnow() + td
    datum_geldigheid = d.strftime("%Y-%m-%d")
    qp = {"datumGeldigheid": datum_geldigheid}
    zaaktype_nieuw = context.client.catalogus.retrieve_zaaktype(url, query_arguments=qp)
    delta = datetime.utcnow() - td
    geldigheid = delta.strftime("%Y-%m-%d")
    query_param = {"datumGeldigheid": geldigheid}
    zaaktype_oud = context.client.catalogus.retrieve_zaaktype(
        url, query_arguments=query_param
    )

    context.zaaktype_oud = zaaktype_oud
    context.zaaktype_nieuw = zaaktype_nieuw


@step("moeten de besluittypen naar de juiste versie wijzen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    zaaktype_oud = context.zaaktype_oud
    zaaktype_nieuw = context.zaaktype_nieuw
    assert zaaktype_nieuw.status_code == 200
    assert zaaktype_oud.status_code == 200

    bto = context.client.catalogus.retrieve_catalogus_object(zaaktype_oud.json()['besluittypen'][0])
    btn = context.client.catalogus.retrieve_catalogus_object(zaaktype_nieuw.json()['besluittypen'][0])

    assert bto.status_code == 200
    assert not bto.json()['concept']
    assert bto.json()["eindeGeldigheid"] != ""
    assert btn.status_code == 200
    assert btn.json()['concept']
    assert btn.json()["eindeGeldigheid"] is None


@step("moeten de gerelateerdeZaaktype naar de juiste versie wijzen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    zaaktype_oud = context.zaaktype_oud
    zaaktype_nieuw = context.zaaktype_nieuw
    assert zaaktype_nieuw.status_code == 200
    assert zaaktype_oud.status_code == 200
    assert zaaktype_nieuw.json()['gerelateerdeZaaktypen'] != []
    assert zaaktype_oud.json()['gerelateerdeZaaktypen'] != []

@step("er een nieuwe besluittype wordt aangemaakt door de reactietermijn omhoog te zetten")
def step_impl(context):
    bt = context.client.catalogus.retrieve_catalogus_object(context.flow.besluittype_url)
    body = bt.json()
    td = timedelta(days=1)
    d = datetime.utcnow() + td
    datum_geldigheid = d.strftime("%Y-%m-%d")
    new_reactietermijn = "P1Y1M10D"
    body["reactietermijn"] = new_reactietermijn
    body["beginGeldigheid"] = datum_geldigheid
    del body["eindeGeldigheid"]
    del body["concept"]
    resp = context.flow.besluittype_with_return(body)
    print(resp.json())


@step("het besluittype gepubliceerd wordt")
def step_impl(context):
    bt = context.client.catalogus.retrieve_catalogus_object(context.flow.besluittype_url)
    context.client.catalogus.publish_type(bt.json()['url'])


@step("het besluittype een datum van vandaag krijgt")
def step_impl(context):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    uuid = context.flow.besluittype_url.split("/")[-1]
    context.flow.update_besluittype_with_geldigheid(
        uuid=uuid, geldigheid=timestamp
    )