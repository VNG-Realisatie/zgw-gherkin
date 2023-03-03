import configparser
import os
from datetime import datetime

from behave import fixture, use_fixture

from client import endpoints, zgw
from flows import flow
from util import randomizer

VALID_TAGS = ["archiveren.valide", "catalogus", "zaak.basis", "zaak.compleet"]


@fixture
def setup(context, *args, **kwargs):
    # variables will be read from the config.ini
    env = os.environ.get("ENV", "test")

    config = configparser.ConfigParser()
    config.read("config.ini")
    api_config = config[env]

    zgw_endpoints = get_external_endpoints(api_config)

    client = zgw.Client(endpoints=zgw_endpoints)
    context.client = client

    if env == "kubernetes":
        internal_service_endpoints = get_internal_service_endpoints()
        context.internal_service_endpoints = internal_service_endpoints

    context.token = _token(client=client)["authorization"]
    print(context.token)
    return


@fixture()
def setup_flow(context, *args, **kwargs):
    try:
        internal_endpoints = context.internal_service_endpoints
    except AttributeError:
        print("internal endpoints left empty")
        internal_endpoints = None
    f = flow.Flow(
        client=context.client,
        internal_service_endpoints=internal_endpoints,
    )
    context.flow = f


def _token(client: zgw):
    random_string = randomizer.create_random_string(12)
    client_id = "testRun" + random_string
    return client.token_issuer.create_admin_token(client_id=client_id).json()


def get_external_endpoints(config):
    brc_address = config["brc"]
    from_env = os.environ.get("BRC_ADDRESS")
    if from_env is not None:
        brc_address = from_env

    drc_address = config["drc"]
    from_env = os.environ.get("DRC_ADDRESS")
    if from_env is not None:
        drc_address = from_env

    token_issuer = config["token-issuer"]
    from_env = os.environ.get("TOKEN_ISSUER_ADDRESS")
    if from_env is not None:
        token_issuer = from_env

    vrl_address = config["vrl"]
    from_env = os.environ.get("VRL_ADDRESS")
    if from_env is not None:
        vrl_address = from_env

    ztc_address = config["ztc"]
    from_env = os.environ.get("ZTC_ADDRESS")
    if from_env is not None:
        ztc_address = from_env

    zrc_address = config["zrc"]
    from_env = os.environ.get("ZRC_ADDRESS")
    if from_env is not None:
        zrc_address = from_env

    return endpoints.EndPoints(
        brc=brc_address,
        drc=drc_address,
        vrl=vrl_address,
        token_issuer=token_issuer,
        zrc=zrc_address,
        ztc=ztc_address,
    )


def get_internal_service_endpoints():
    namespace = os.environ.get("NAMESPACE", "zgw")

    internal_brc_address = os.environ.get("INTERNAL_BRC_ADDRESS")
    if internal_brc_address is None:
        internal_brc_address = f"http://brc.{namespace}.svc.cluster.local:8000"

    internal_drc_address = os.environ.get("INTERNAL_DRC_ADDRESS")
    if internal_drc_address is None:
        internal_drc_address = f"http://drc.{namespace}.svc.cluster.local:8000"

    internal_vrl_address = os.environ.get("INTERNAL_VRL_ADDRESS")
    if internal_vrl_address is None:
        internal_vrl_address = f"http://vrl.{namespace}.svc.cluster.local:8000"

    internal_ztc_address = os.environ.get("INTERNAL_ZTC_ADDRESS")
    if internal_ztc_address is None:
        internal_ztc_address = f"http://ztc.{namespace}.svc.cluster.local:8000"

    internal_zrc_address = os.environ.get("INTERNAL_ZRC_ADDRESS")
    if internal_zrc_address is None:
        internal_zrc_address = f"http://zrc.{namespace}.svc.cluster.local:8000"

    internal_token_address = os.environ.get("INTERNAL_TOKEN_ADDRESS")
    if internal_token_address is None:
        internal_token_address = (
            f"http://token-issuer.{namespace}.svc.cluster.local:8000"
        )

    internal_service_endpoints = endpoints.EndPoints(
        brc=internal_brc_address,
        drc=internal_drc_address,
        vrl=internal_vrl_address,
        zrc=internal_zrc_address,
        ztc=internal_ztc_address,
        token_issuer=internal_token_address,
    )

    return internal_service_endpoints


def set_token(context):
    context.client.catalogus.set_token(context.token)
    context.client.documenten.set_token(context.token)
    context.client.zaken.set_token(context.token)
    return


def before_tag(context, tag):
    print(f"working on tag: {tag}")
    match tag:
        case "catalogus":
            use_fixture(setup_flow, context)
            context.flow.setup_catalogus()
        case "token.set":
            set_token(context)
        case "zaak.basis":
            use_fixture(setup_flow, context)
            context.flow.prerequisites_zaak()
        case "zaak.compleet":
            use_fixture(setup_flow, context)
            context.flow.complete_zaak()
        case _:
            print(f"unknown tag: {tag}")

    return


def before_feature(context, feature):
    print(f'starttime: {datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")}')
    print(f"working on feature: {feature}")
    use_fixture(setup, context)


def before_scenario(context, scenario):
    print(f"working on scenario: {scenario}")
    for tag in scenario.tags:
        for inner_tag in VALID_TAGS:
            if inner_tag == tag:
                return
    use_fixture(setup_flow, context)
