import string
import urllib
from urllib.parse import urljoin

import requests
from client.endpoints import EndPoints


class BaseClient:
    def __init__(self):
        self.application = "application/json"
        self.token = ""

    @staticmethod
    def parse_url(*args):
        url = ""
        for i, arg in enumerate(args):
            url = urljoin(url, arg)
            if not url.endswith("/") and len(args) != i + 1:
                url = url + "/"
        return url

    @staticmethod
    def parse_query(query_parameters):
        return "?" + (urllib.parse.urlencode(query_parameters))

    def _get_header(self):
        return {
            "Accept": self.application,
            "Content-Type": self.application,
            "Authorization": self.token,
        }

    def _get_full_header(self):
        return {
            "Content-Crs": "EPSG:4326",
            "Accept-Crs": "EPSG:4326",
            "Accept": self.application,
            "Content-Type": self.application,
            "Authorization": self.token,
        }

    def _get_header_without_auth(self):
        return {
            "Accept": self.application,
            "Content-Type": self.application,
        }

    def set_token(self, token: str):
        self.token = token


class Client(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, endpoints: EndPoints):
        super().__init__()
        self.endpoints = endpoints
        self.besluiten = BesluitenApi(base_url=endpoints.brc)
        self.catalogus = CatalogusApi(base_url=endpoints.ztc)
        self.documenten = DocumentenApi(base_url=endpoints.drc)
        self.token_issuer = TokenIssuerApi(base_url=endpoints.token_issuer)
        self.referentie = ReferentieApi(base_url=endpoints.vrl)
        self.zaken = ZakenApi(base_url=endpoints.zrc)


class BesluitenApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.version = "/api/v1"

    def check_available(self):
        method = "GET"
        header = self._get_header_without_auth()
        response = requests.request(method, self.base_url, headers=header)
        return response


class CatalogusApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.publish = "publish"
        self.catalogussen_endpoint = "catalogussen"
        self.besluittype_endpoint = "besluittypen"
        self.informatieobjecttypen_endpoint = "informatieobjecttypen"
        self.zaaktype_endpoint = "zaaktypen"
        self.zaaktype_informatie_endpoint = "zaaktype-informatieobjecttypen"
        self.eigenschappen_endpoint = "eigenschappen"
        self.resultaattype_endpoint = "resultaattypen"
        self.statustype_endpoint = "statustypen"
        self.roltype_endpoint = "roltypen"
        self.base_url = base_url
        self.version = "/api/v1"

    def check_available(self):
        method = "GET"
        header = self._get_header_without_auth()
        response = requests.request(method, self.base_url, headers=header)
        return response

    def create_catalogus(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.catalogussen_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_besluittype(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.besluittype_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_informatieobjecttype(self, body: dict):
        method = "POST"
        url = self.parse_url(
            self.base_url, self.version, self.informatieobjecttypen_endpoint
        )
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_zaaktype(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.zaaktype_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_zaaktype_informatieobjecttype_relation(self, body):
        method = "POST"
        url = self.parse_url(
            self.base_url, self.version, self.zaaktype_informatie_endpoint
        )
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_eigenschap(self, body):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.eigenschappen_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_resultaattype(self, body):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.resultaattype_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_statustype(self, body):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.statustype_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_roltype(self, body):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.roltype_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def publish_type(self, reference_url):
        method = "POST"
        header = self._get_header()
        body = {}
        url = self.parse_url(reference_url, self.publish)
        response = requests.request(method, url, headers=header, json=body)
        return response

    def search_catalogus(self, query_arguments: dict):
        method = "GET"
        param = self.parse_query(query_arguments)
        base = self.parse_url(self.base_url, self.version, self.catalogussen_endpoint)
        url = urljoin(base, param)
        header = self._get_header()
        response = requests.request(method, url, headers=header)
        return response


class DocumentenApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.enkelvoudiginformatieobjecten = "enkelvoudiginformatieobjecten"
        self.gebruiksrechten = "gebruiksrechten"
        self.version = "/api/v1"

    def check_available(self):
        method = "GET"
        header = self._get_header_without_auth()
        response = requests.request(method, self.base_url, headers=header)
        return response

    def create_enkelvoudiginformatieobjecten(self, body: dict):
        method = "POST"
        url = self.parse_url(
            self.base_url, self.version, self.enkelvoudiginformatieobjecten
        )
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_gebruiksrechten(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.gebruiksrechten)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response


class TokenIssuerApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.token_endpoint = "register/"
        self.base_url = base_url
        self.version = "/api/v1"

    def create_admin_token(self, client_id):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.token_endpoint)
        header = self._get_header()
        body = {
            "clientIds": [client_id],
            "label": "testAdminToken",
            "heeftAlleAutorisaties": True,
            "autorisaties": [],
        }
        response = requests.request(method, url, headers=header, json=body)
        return response

    def create_token(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.token_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response


class ReferentieApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.resultaten = "resultaten"
        self.omschrijvingen = "resultaattypeomschrijvingen"
        self.version = "/api/v1"

    def check_available(self):
        method = "GET"
        header = self._get_header_without_auth()
        response = requests.request(method, self.base_url, headers=header)
        return response

    def get_resultaten(self):
        method = "GET"
        header = self._get_header()
        url = self.parse_url(self.base_url, self.version, self.resultaten)
        response = requests.request(method, url, headers=header)
        return response

    def get_omschrijvingen(self):
        method = "GET"
        header = self._get_header()
        url = self.parse_url(self.base_url, self.version, self.omschrijvingen)
        response = requests.request(method, url, headers=header)
        return response


class ZakenApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.zaken_endpoint = "zaken"
        self.base_url = base_url
        self.version = "/api/v1"

    def check_available(self):
        method = "GET"
        header = self._get_header_without_auth()
        response = requests.request(method, self.base_url, headers=header)
        return response

    def create_zaak(self, body: dict):
        method = "POST"
        url = self.parse_url(self.base_url, self.version, self.zaken_endpoint)
        header = self._get_full_header()
        response = requests.request(method, url, headers=header, json=body)
        return response

    def search_zaak(self, params: str):
        method = "GET"
        header = self._get_full_header()
        url = self.parse_url(self.base_url, self.version, self.zaken_endpoint, params)
        response = requests.request(method, url, headers=header)
        return response
