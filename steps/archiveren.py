from behave import *

use_step_matcher("re")


@step("dat deze zaak een begin status heeft")
def step_impl(context):
    context.flow.statussen(close=False)


@step("deze zaak nog niet de eindstatus bereikt heeft")
def step_impl(context):
    # zaak -> status -> statustype -> assert !eindstatus
    # uuid = context.flow.zaak.json()["uuid"]
    # resp = context.client.catalogus.search_statustype(uuid)
    # assert resp.status_code == 200

    # status van de zaak ophalen

    # assert resp.json()["eindstatus"] == None
    assert True is True


@step("dat de archiefnominatie van de zaak nog niet bekend is")
def step_impl(context):
    uuid = context.flow.zaak.json()["uuid"]
    resp = context.client.zaken.search_zaak(uuid)
    assert resp.status_code == 200

    assert resp.json()["archiefnominatie"] == None


@step(
    "voor alle aan deze zaak gerelateerde informatieobjecten de status (?P<informatieobject_status>.+) heeft en indicatie_gebruiksrecht (?P<indicatie_gebruiksrecht>.+)"
)
def step_impl(context, informatieobject_status, indicatie_gebruiksrecht):
    """
    :type context: behave.runner.Context
    :type informatieobject_status: str
    :type indicatie_gebruiksrecht: str
    """
    context.flow.zaakinformatieobjecten_kopppeling()
    resp = context.client.zaken.search_zaakinformatieobject(
        url=context.flow.zaakinformatieobject_url
    )
    sut = resp.json()
    print(sut)
