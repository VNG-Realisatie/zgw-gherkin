from behave import fixture, use_fixture
import os


@fixture
def setup(context, *args, **kwargs):
    token = os.environ.get("TOKEN")
    if token is None:
        # todo we want to get a token if none is set using the token tool
        print("no token set please use ENV var")
    context.token = token
    ztc_address = os.environ.get("ZTC_ADDRESS")
    if ztc_address is None:
        ztc_address = "https://zaken-api.vng.cloud/api/v1"
    context.ztc_address = ztc_address


def before_feature(context, feature):
    use_fixture(setup, context)
