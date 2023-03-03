from behave import fixture, use_fixture

from flows import flow
from client import zgw, endpoints
from util import randomizer

import os


@fixture
def setup(context, *args, **kwargs):
    namespace = os.environ.get("NAMESPACE", "vng")

    brc_address = os.environ.get("BRC_ADDRESS")
    if brc_address is None:
        brc_address = "http://k8s-brc-local.test"

    drc_address = os.environ.get("DRC_ADDRESS")
    if drc_address is None:
        drc_address = "http://k8s-drc-local.test"

    token_issuer = os.environ.get("TOKEN_ISSUER_ADDRESS")
    if token_issuer is None:
        token_issuer = "http://k8s-tokens-local.test"

    vrl_address = os.environ.get("VRL_ADDRESS")
    if vrl_address is None:
        vrl_address = "http://k8s-vrl-local.test"

    ztc_address = os.environ.get("ZTC_ADDRESS")
    if ztc_address is None:
        ztc_address = "http://k8s-ztc-local.test"

    zrc_address = os.environ.get("ZRC_ADDRESS")
    if zrc_address is None:
        zrc_address = "http://k8s-zrc-local.test"

    internal__brc_address = os.environ.get("INTERNAL_BRC_ADDRESS")
    if internal__brc_address is None:
        internal__brc_address = f"http://brc.{namespace}.svc.cluster.local:8000"

    internal_drc_address = os.environ.get("INTERNAL_DRC_ADDRESS")
    if internal_drc_address is None:
        internal_drc_address = f"http://drc.{namespace}.svc.cluster.local:8000"

    internal__vrl_address = os.environ.get("INTERNAL_VRL_ADDRESS")
    if internal__vrl_address is None:
        internal__vrl_address = f"http://vrl.{namespace}.svc.cluster.local:8000"

    internal_ztc_address = os.environ.get("INTERNAL_ZTC_ADDRESS")
    if internal_ztc_address is None:
        internal_ztc_address = f"http://ztc.{namespace}.svc.cluster.local:8000"

    internal_zrc_address = os.environ.get("INTERNAL_ZRC_ADDRESS")
    if internal_zrc_address is None:
        internal_zrc_address = f"http://zrc.{namespace}.svc.cluster.local:8000"

    zgw_endpoints = endpoints.EndPoints(
        ac="",
        brc=brc_address,
        drc=drc_address,
        nrc="",
        vrl=vrl_address,
        token_issuer=token_issuer,
        zrc=zrc_address,
        ztc=ztc_address,
    )

    internal_service_endpoints = endpoints.EndPoints(
        ac="",
        brc=internal__brc_address,
        drc=internal_drc_address,
        nrc="",
        token_issuer="",
        vrl=internal__vrl_address,
        zrc=internal_zrc_address,
        ztc=internal_ztc_address,
    )

    client = zgw.Client(endpoints=zgw_endpoints)
    context.client = client

    random_string = randomizer.create_random_string(12)
    client_id = "testRun" + random_string
    token = context.client.token_issuer.create_admin_token(client_id=client_id).json()
    context.token = token["authorization"]

    f = flow.Flow(
        client=context.client, internal_service_endpoints=internal_service_endpoints
    )
    context.flow = f


def before_tag(context, tag):
    if tag == "archiveren.valide":
        print("hello archiveren")
    elif tag == "catalogus":
        context.flow.setup_catalogus()
    return


def before_feature(context, feature):
    print(feature)
    use_fixture(setup, context)
