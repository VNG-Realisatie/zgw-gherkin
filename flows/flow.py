from datetime import datetime, timedelta
from util import randomizer


class Flow:
    def __init__(self, client, internal_service_endpoints):

        self.client = client
        self.internal_service_endpoints = internal_service_endpoints
        self.creatie_datum = datetime.today().strftime("%Y-%m-%d")
        self.geldigheid = datetime.today().strftime("%Y-%m-%d")
        self.statustype_begin = []
        self.statustype_eind = None
        self.resultaattype_url = None
        self.resultaattypeomschrijving_url = None
        self.zaaktype_eigenschap = None
        self.zaaktype_url = None
        self.deelzaaktype_url = None
        self.procestype_url = None
        self.informatieobjecttype_url = None
        self.besluittype_url = None
        self.catalogus_url = None
        self.naam = None
        self.catalogus = None
        self.valid_resin = self._create_valid_rsin()
        self.bron_organisatie = None
        self.enkelvoudig_informatieobject_url = None
        self.informatieobject_type = None
        self.selectie_lijst_url = None
        self.zaak_url = None
        self.zaak = None

    def create_complete_aak(self, archief_status):
        self.setup_catalogus()
        self.besluittype()
        self.informatieobjecttype()
        self.deelzaaktype()
        self.zaaktype()
        self.zaaktype_informatie_relation()
        self.eigenschappen()
        self.statustype_begin_end()
        self.roltype()
        self.publish_types()
        self.enkelvoudiginformatieobject()
        self.gebruiksrechten()
        self.zaken(archiefstatus=archief_status)

    def _create_valid_rsin(self):
        found = False
        valid_rsin = ""
        while not found:
            valid_rsin = randomizer.create_random_number(9)
            found = self._validate_rsin(str(valid_rsin))
        return valid_rsin

    @staticmethod
    def _validate_rsin(value):
        if len(value) != 9 or not value.isdigit():
            return False

        total = 0
        for multiplier, char in enumerate(reversed(value), start=1):
            if multiplier == 1:
                total += -multiplier * int(char)
            else:
                total += multiplier * int(char)
        if total % 11 != 0 or total == 0:
            return False
        return True

    @staticmethod
    def _replace_with_internal_service_address(external_url, service):
        parts = external_url.split("/")
        url_builder = service
        build = []
        for index, part in enumerate(parts):
            if part == "api":
                build = parts[index:]
        for index, part in enumerate(build):
            if index < len(build):
                url_builder += "/"
            url_builder += part
        return url_builder

    def enkelvoudiginformatieobject(self, field="", value=""):
        internal_informatie_object_type_url = (
            self._replace_with_internal_service_address(
                self.informatieobject_type, self.internal_service_endpoints.ztc
            )
        )
        body = {
            "bronorganisatie": self.valid_resin,
            "creatiedatum": self.creatie_datum,
            "titel": "testobject",
            "auteur": "testauteur",
            "taal": "eng",
            "inhoud": "c3RyaW5n",
            "informatieobjecttype": internal_informatie_object_type_url,
            "bestandsomvang": 6,
        }

        if field != "":
            body[field] = value

        response = self.client.documenten.create_enkelvoudiginformatieobjecten(body)
        self.enkelvoudig_informatieobject_url = response.json()["url"]

    def gebruiksrechten(self):
        internal_informatie_object = self._replace_with_internal_service_address(
            self.enkelvoudig_informatieobject_url, self.internal_service_endpoints.drc
        )
        start_datum = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        body = {
            "informatieobject": internal_informatie_object,
            "startdatum": start_datum,
            "omschrijvingVoorwaarden": "test " + self.naam,
        }
        self.client.documenten.create_gebruiksrechten(body)

    def zaken(self, archiefstatus):
        td = timedelta(days=365)
        datum_future = (datetime.now() + td).strftime("%Y-%m-%d")

        internal_selectie_lijst_url = self._replace_with_internal_service_address(
            self.selectie_lijst_url, self.internal_service_endpoints.vrl
        )
        internal_zaak_type = self._replace_with_internal_service_address(
            self.zaaktype_url, self.internal_service_endpoints.ztc
        )
        body = {
            "bronorganisatie": self.valid_resin,
            "omschrijving": "omschrijving: " + self.naam,
            "toelichting": "toelichting: " + self.naam,
            "registratiedatum": self.creatie_datum,
            "verantwoordelijkeOrganisatie": self.valid_resin,
            "zaaktype": internal_zaak_type,
            "startdatum": datum_future,
            "einddatumGepland": "2019-04-20",
            "uiterlijkeEinddatumAfdoening": datum_future,
            "publicatiedatum": datum_future,
            "vertrouwelijkheidaanduiding": "openbaar",
            "betalingsindicatie": "geheel",
            "laatsteBetaalDatum": datum_future,
            "zaakgeometrie": {"type": "Point", "coordinates": [53, 5]},
            "opschorting": {"indicatie": True, "reden": "string"},
            "selectielijstklasse": internal_selectie_lijst_url,
            "archiefstatus": archiefstatus,
        }

        self.zaak = self.client.zaken.create_zaak(body)
        self.zaak_url = self.zaak.json()["url"]

    def setup_catalogus(self):
        random_name = randomizer.create_random_string(25)
        random_domein = randomizer.create_random_letter(5).upper()

        self.naam = random_name

        body = {
            "domein": random_domein,
            "rsin": self.valid_resin,
            "contactpersoonBeheerNaam": "TestPersoon " + random_name,
            "naam": random_name,
        }

        self.catalogus = self.client.catalogus.create_catalogus(body)
        self.catalogus_url = self.catalogus.json()["url"]

    def besluittype(self):
        body = {
            "catalogus": self.catalogus_url,
            "omschrijving": "testbesluittype" + self.naam,
            "zaaktypen": [],
            "publicatieIndicatie": False,
            "informatieobjecttypen": [],
            "beginGeldigheid": self.geldigheid,
        }

        response = self.client.catalogus.create_besluittype(body)
        self.besluittype_url = response.json()["url"]
        # if self.internal_service_endpoints.ztc != "":
        #     self.besluittype_url = self._replace_with_internal_service_address(response.json()["url"], self.internal_service_endpoints.ztc)
        return response

    def informatieobjecttype(self):
        body = {
            "catalogus": self.catalogus_url,
            "omschrijving": "testinformatieobjecttype" + self.naam,
            "vertrouwelijkheidaanduiding": "openbaar",
            "informatieobjectcategorie": "informatieobjectcategorie" + self.naam,
            "beginGeldigheid": self.geldigheid,
        }

        response = self.client.catalogus.create_informatieobjecttype(body)
        self.informatieobjecttype_url = response.json()["url"]
        self.informatieobject_type = response.json()["url"]
        # if self.internal_service_endpoints.ztc != "":
        #     self.informatieobjecttype_url = self._replace_with_internal_service_address(response.json()["url"], self.internal_service_endpoints.ztc)
        return response

    def deelzaaktype(self):
        identificatie = randomizer.create_random_string(40)

        resultaten = self.client.referentie.get_resultaten().json()
        for resultaat in resultaten["results"]:
            if resultaat["procestermijn"] == "nihil":
                self.procestype_url = resultaat["procesType"]
                self.selectie_lijst_url = resultaat["url"]
                break

        internal_proces_type_url = self._replace_with_internal_service_address(
            self.procestype_url, self.internal_service_endpoints.vrl
        )
        body = {
            "identificatie": identificatie,
            "omschrijving": "testdeelzaaktype " + self.naam,
            "verantwoordelijke": "verantwoordelijk" + self.naam,
            "vertrouwelijkheidaanduiding": "openbaar",
            "doel": "test doel",
            "aanleiding": "test aanleiding",
            "indicatieInternOfExtern": "extern",
            "handelingInitiator": "indienen",
            "onderwerp": "openbare ruimte",
            "handelingBehandelaar": "behandelen",
            "doorlooptijd": "P10D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "publicatieIndicatie": False,
            "productenOfDiensten": ["https://vng.nl/projecten/gemma-softwarecatalogus"],
            "selectielijstProcestype": internal_proces_type_url,
            "referentieproces": {"naam": "test", "link": ""},
            "catalogus": self.catalogus_url,
            "informatieobjecttypen": [],
            "besluittypen": [self.besluittype_url],
            "gerelateerdeZaaktypen": [],
            "beginGeldigheid": self.geldigheid,
            "versiedatum": self.geldigheid,
            "concept": True,
            "verlengingstermijn": "P5D",
        }

        response = self.client.catalogus.create_zaaktype(body)
        self.deelzaaktype_url = response.json()["url"]
        return response

    def zaaktype(self):
        identificatie = randomizer.create_random_string(40)

        internal_proces_type_url = self._replace_with_internal_service_address(
            self.procestype_url, self.internal_service_endpoints.vrl
        )

        body = {
            "identificatie": identificatie,
            "omschrijving": "testdeelzaaktype " + self.naam,
            "vertrouwelijkheidaanduiding": "openbaar",
            "verantwoordelijke": "verantwoordelijk" + self.naam,
            "doel": "test doel",
            "aanleiding": "test aanleiding",
            "indicatieInternOfExtern": "extern",
            "handelingInitiator": "indienen",
            "onderwerp": "openbare ruimte",
            "handelingBehandelaar": "behandelen",
            "doorlooptijd": "P10D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "publicatieIndicatie": False,
            "productenOfDiensten": ["https://vng.nl/projecten/gemma-softwarecatalogus"],
            "selectielijstProcestype": internal_proces_type_url,
            "referentieproces": {"naam": "test", "link": ""},
            "deelzaaktypen": [self.deelzaaktype_url],
            "catalogus": self.catalogus_url,
            "informatieobjecttypen": [],
            "besluittypen": [self.besluittype_url],
            "gerelateerdeZaaktypen": [],
            "beginGeldigheid": self.geldigheid,
            "versiedatum": self.geldigheid,
            "concept": True,
            "verlengingstermijn": "P5D",
        }

        response = self.client.catalogus.create_zaaktype(body)
        self.zaaktype_url = response.json()["url"]
        return response

    def zaaktype_informatie_relation(self):
        body = {
            "zaaktype": self.zaaktype_url,
            "informatieobjecttype": self.informatieobjecttype_url,
            "volgnummer": 1,
            "richting": "inkomend",
        }
        return self.client.catalogus.create_zaaktype_informatieobjecttype_relation(body)

    def eigenschappen(self):
        eigenschap_naam = randomizer.create_random_string(8)
        body = {
            "naam": "eigenschap " + eigenschap_naam,
            "definitie": "for test",
            "zaaktype": self.zaaktype_url,
            "specificatie": {
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": ["test"],
            },
        }
        response = self.client.catalogus.create_eigenschap(body)
        self.zaaktype_eigenschap = response.json()["url"]
        return response

    def resultaattypen(self):
        resultaattypeomschrijvingen = self.client.referentie.get_omschrijvingen().json()
        self.resultaattypeomschrijving_url = resultaattypeomschrijvingen[0]["url"]

        internal_selectie_lijst_url = self._replace_with_internal_service_address(
            self.selectie_lijst_url, self.internal_service_endpoints.vrl
        )
        body = {
            "zaaktype": self.zaaktype_url,
            "omschrijving": "Klaar",
            "resultaattypeomschrijving": self.resultaattypeomschrijving_url,
            "selectielijstklasse": internal_selectie_lijst_url,
            "brondatumArchiefprocedure": {
                "afleidingswijze": "afgehandeld",
                "procestermijn": None,
                "datumkenmerk": "",
                "einddatumBekend": False,
                "objecttype": "",
                "registratie": "",
            },
        }

        response = self.client.catalogus.create_resultaattype(body)
        self.resultaattype_url = response.json()["url"]
        return response

    def statustype_begin_end(self):
        omschrijvingen = ["Begin", "Einde"]

        for i, omschrijving in enumerate(omschrijvingen, 1):
            body = {
                "omschrijving": omschrijving,
                "zaaktype": self.zaaktype_url,
                "volgnummer": i,
            }
            response = self.client.catalogus.create_resultaattype(body).json()
            if i < len(omschrijvingen):
                self.statustype_begin.append(response)
            else:
                self.statustype_eind = response
        return

    def roltype(self):
        body = {
            "zaaktype": self.zaaktype_url,
            "omschrijving": "testroltype " + self.naam,
            "omschrijvingGeneriek": "adviseur",
        }

        return self.client.catalogus.create_roltype(body)

    def publish_types(self):
        if self.besluittype_url is not None:
            self.client.catalogus.publish_type(self.besluittype_url)

        if self.informatieobjecttype_url is not None:
            self.client.catalogus.publish_type(self.informatieobjecttype_url)

        if self.deelzaaktype_url is not None:
            self.client.catalogus.publish_type(self.deelzaaktype_url)

        if self.zaaktype_url is not None:
            self.client.catalogus.publish_type(self.zaaktype_url)
