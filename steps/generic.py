from behave import *


@step("er is een valide token gezet")
def step_impl(context):
    context.client.catalogus.set_token(context.token)
    context.client.documenten.set_token(context.token)
    context.client.zaken.set_token(context.token)
    return
