from behave import *


@step("er een valide enkelvoudiginformatieobject aangemaakt wordt")
def step_impl(context):
    context.flow.enkelvoudiginformatieobject()
    return


@step("er valide gebruiksrechten worden aangemaakt")
def step_impl(context):
    context.flow.gebruiksrechten()
    return


@step("er een valide enkelvoudiginformatieobject aangemaakt wordt met {veld} {waarde}")
def step_impl(context, veld, waarde):
    """
    :type context: behave.runner.Context
    :type veld: str
    :type waarde: str
    """
    context.flow.enkelvoudiginformatieobject(field=veld, value=waarde)
