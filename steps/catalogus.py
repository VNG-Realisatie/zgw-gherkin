from behave import *


@step("de catalogus-api is beschikbaar")
def step_impl(context):
    response = context.client.catalogus.check_available()
    assert response.status_code == 200
    return


@step("de catalogus wordt gezocht met parameters")
def step_impl(context):
    search_responses = []
    response = context.ztc.catalogus.json()
    for row in context.table:
        query_param = {row["parameter"]: response[row["parameter"]]}
        resp = context.client.catalogus.search_catalogus(query_arguments=query_param)
        search_responses.append(resp)
    context.search_responses = search_responses


@step("er een nieuwe valide catalogus aangemaakt wordt")
def step_impl(context):
    context.flow.setup_catalogus()
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


@step("krijgt de gebruiker statuscode {status_code:d} terug")
def step_impl(context, status_code):
    response = context.catalogus
    assert response.status_code == status_code


@step("krijgt de gebruiker de catalogus terug met de juiste informatie")
def step_impl(context):
    responses = context.search_responses
    for response in responses:
        assert response.status_code == 200
