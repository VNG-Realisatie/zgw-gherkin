from datetime import datetime, timedelta

from util import randomizer


class Flow:
    def __init__(self, client, internal_service_endpoints):
        self.deelzaak_type = None
        self.besluit_type = None
        self.zaaktypen_list = []
        self.zaak_uuid = None
        self.zaak_eigenschap_url = None
        self.client = client
        self.internal_service_endpoints = internal_service_endpoints
        self.creatie_datum = datetime.today().strftime("%Y-%m-%d")
        self.geldigheid = datetime.today().strftime("%Y-%m-%d")
        self.statustype_begin = None
        self.statustype_eind = None
        self.resultaattype_url = None
        self.resultaattypeomschrijving_url = None
        self.zaaktype_eigenschap_url = None
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
        self.resultaattype = None
        self.resultaat_url = None
        self.roltype_url = None
        self.status = None
        self.rol_url = None
        self.zaakinformatieobject_url = None

    def prerequisites_zaak(self):
        self.setup_catalogus()
        self.besluittype()
        self.informatieobjecttype()
        self.deelzaaktype()
        self.zaaktype()
        self.zaaktype_informatie_relation()
        self.eigenschappen()
        self.resultaattypen()
        self.statustype_begin_end()
        self.roltype()
        self.publish_types()
        self.enkelvoudiginformatieobject()
        self.gebruiksrechten()

    def complete_zaak(self):
        self.prerequisites_zaak()
        self.zaken(archiefstatus="nog_te_archiveren")
        self.resultaten()
        self.rollen()
        self.statussen()
        self.zaakobjecten()
        self.zaakeigenschappen()
        self.zaakinformatieobjecten_kopppeling()
        self.klantcontacten()

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

    def resultaten(self):
        resultaatype_url = self.resultaattype_url
        if self.internal_service_endpoints is not None:
            resultaatype_url = self._replace_with_internal_service_address(
                self.resultaattype_url, self.internal_service_endpoints.ztc
            )

        body = {"zaak": self.zaak_url, "resultaattype": resultaatype_url}

        response = self.client.zaken.create_resultaat(body)
        self.resultaat_url = response.json()["url"]

    def zaakinformatieobjecten_kopppeling(self):
        informatieobject_url = self.enkelvoudig_informatieobject_url
        if self.internal_service_endpoints is not None:
            informatieobject_url = self._replace_with_internal_service_address(
                self.enkelvoudig_informatieobject_url,
                self.internal_service_endpoints.drc,
            )

        body = {
            "zaak": self.zaak_url,
            "informatieobject": informatieobject_url,
            "titel": "titel" + self.naam,
            "beschrijving": "beschrijving" + self.naam,
        }

        response = self.client.zaken.relate_informatieobject(body)

        if response.status_code == 201:
            self.zaakinformatieobject_url = response.json()["url"]

    def statussen(self, datum_gezet="", close=True):
        status_url = self.statustype_eind
        if self.internal_service_endpoints is not None:
            status_url = self._replace_with_internal_service_address(
                self.statustype_eind, self.internal_service_endpoints.ztc
            )
        if not close:
            status_url = self.statustype_begin
            if self.internal_service_endpoints is not None:
                status_url = self._replace_with_internal_service_address(
                    self.statustype_begin, self.internal_service_endpoints.ztc
                )

        if datum_gezet == "":
            # datetime.now() returns a 400
            datum_gezet = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        body = {
            "zaak": self.zaak_url,
            "statustype": status_url,
            "datumStatusGezet": datum_gezet,
        }

        response = self.client.zaken.create_status(body)
        self.status = response.json()["url"]
        return response

    def enkelvoudiginformatieobject(self, field="", value=""):
        informatie_object_type = self.informatieobjecttype_url
        if self.internal_service_endpoints is not None:
            informatie_object_type = self._replace_with_internal_service_address(
                self.informatieobjecttype_url, self.internal_service_endpoints.ztc
            )
        body = {
            "bronorganisatie": self.valid_resin,
            "creatiedatum": self.creatie_datum,
            "titel": "testobject",
            "auteur": "testauteur",
            "taal": "eng",
            "inhoud": "c3RyaW5n",
            "informatieobjecttype": informatie_object_type,
            "bestandsomvang": 6,
        }

        if field != "":
            body[field] = value

        response = self.client.documenten.create_enkelvoudiginformatieobjecten(body)
        self.enkelvoudig_informatieobject_url = response.json()["url"]

    def gebruiksrechten(self):
        informatie_object = self.enkelvoudig_informatieobject_url
        if self.internal_service_endpoints is not None:
            informatie_object = self._replace_with_internal_service_address(
                self.enkelvoudig_informatieobject_url,
                self.internal_service_endpoints.drc,
            )

        start_datum = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        body = {
            "informatieobject": informatie_object,
            "startdatum": start_datum,
            "omschrijvingVoorwaarden": "test " + self.naam,
        }
        self.client.documenten.create_gebruiksrechten(body)

    def zaken(self, archiefstatus="nog_te_archiveren"):
        selectie_lijst_url = self.selectie_lijst_url
        if self.internal_service_endpoints is not None:
            selectie_lijst_url = self._replace_with_internal_service_address(
                self.selectie_lijst_url, self.internal_service_endpoints.vrl
            )

        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        td = timedelta(days=30)
        delta = datetime.utcnow() + td
        einddatum = delta.strftime("%Y-%m-%d")

        td = timedelta(days=10)
        delta = datetime.utcnow() + td
        betaaldatum = delta.strftime("%Y-%m-%d")

        body = {
            "bronorganisatie": self.valid_resin,
            "omschrijving": "omschrijving: " + self.naam,
            "toelichting": "toelichting: " + self.naam,
            "registratiedatum": self.creatie_datum,
            "verantwoordelijkeOrganisatie": self.valid_resin,
            "zaaktype": zaaktype_url,
            "startdatum": self.creatie_datum,
            "einddatumGepland": einddatum,
            "uiterlijkeEinddatumAfdoening": einddatum,
            "publicatiedatum": self.creatie_datum,
            "vertrouwelijkheidaanduiding": "openbaar",
            "betalingsindicatie": "geheel",
            "laatsteBetaalDatum": betaaldatum,
            "zaakgeometrie": {"type": "Point", "coordinates": [53, 5]},
            "opschorting": {"indicatie": True, "reden": "string"},
            "selectielijstklasse": selectie_lijst_url,
            "archiefstatus": archiefstatus,
        }

        self.zaak = self.client.zaken.create_zaak(body)
        self.zaak_url = self.zaak.json()["url"]
        self.zaak_uuid = self.zaak.json()["uuid"]

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
        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )
        body = {
            "catalogus": catalogus_url,
            "omschrijving": "testbesluittype" + self.naam,
            "zaaktypen": [],
            "publicatieIndicatie": False,
            "informatieobjecttypen": [],
            "beginGeldigheid": self.geldigheid,
        }

        response = self.client.catalogus.create_besluittype(body)
        self.besluittype_url = response.json()["url"]
        self.besluittype = response.json()
        return response

    def besluittype_with_return(self, body):
        response = self.client.catalogus.create_besluittype(body)
        return response

    def besluittype_with_informatieobjecttype(self):
        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )

        omschrijving = "testbesluittype" + self.naam

        td = timedelta(days=10)
        d = datetime.utcnow() - td
        geldigheid = d.strftime("%Y-%m-%d")
        iso = "P1Y0M0D"

        iot_omschrijving = self.informatieobject_type["omschrijving"]
        body = {
            "catalogus": catalogus_url,
            "omschrijving": omschrijving,
            "zaaktypen": [],
            "reactietermijn": iso,
            "publicatieIndicatie": False,
            "informatieobjecttypen": [iot_omschrijving],
            "beginGeldigheid": geldigheid,
        }

        response = self.client.catalogus.create_besluittype(body)
        self.besluittype_url = response.json()["url"]
        self.besluit_type = response.json()
        return response

    def informatieobjecttype(self, omschrijving=None):
        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )

        if omschrijving is None:
            omschrijving = "testinformatieobjecttype" + self.naam
        body = {
            "catalogus": catalogus_url,
            "omschrijving": omschrijving,
            "vertrouwelijkheidaanduiding": "openbaar",
            "informatieobjectcategorie": "informatieobjectcategorie" + self.naam,
            "beginGeldigheid": self.geldigheid,
        }

        response = self.client.catalogus.create_informatieobjecttype(body)
        self.informatieobjecttype_url = response.json()["url"]
        self.informatieobject_type = response.json()

        return response

    def deelzaaktype(self):
        identificatie = randomizer.create_random_string(40)

        resultaten = self.client.referentie.get_resultaten().json()
        for resultaat in resultaten["results"]:
            if resultaat["procestermijn"] == "nihil":
                self.procestype_url = resultaat["procesType"]
                self.selectie_lijst_url = resultaat["url"]
                break

        procestype_url = self.procestype_url
        if self.internal_service_endpoints is not None:
            procestype_url = self._replace_with_internal_service_address(
                self.procestype_url, self.internal_service_endpoints.vrl
            )

        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )

        besluittypen = []
        if self.besluit_type is not None:
            besluittypen.append(self.besluit_type["omschrijving"])

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
            "selectielijstProcestype": procestype_url,
            "referentieproces": {"naam": "test", "link": ""},
            "catalogus": catalogus_url,
            "informatieobjecttypen": [],
            "besluittypen": besluittypen,
            "gerelateerdeZaaktypen": [],
            "beginGeldigheid": self.geldigheid,
            "versiedatum": self.geldigheid,
            "concept": True,
            "verlengingstermijn": "P5D",
        }

        response = self.client.catalogus.create_zaaktype(body)
        self.deelzaak_type = response.json()
        self.deelzaaktype_url = response.json()["url"]
        return response

    def update_zaaktype_with_geldigheid(self, uuid, geldigheid):
        body = {
            "eindeGeldigheid": geldigheid,
        }
        response = self.client.catalogus.patch_zaaktype(uuid, body)
        return response

    def update_besluittype_with_geldigheid(self, uuid, geldigheid):
        body = {
            "eindeGeldigheid": geldigheid,
        }
        response = self.client.catalogus.patch_besluittype(uuid, body)
        return response
    def zaaktype_with_return(self, identificatie, other_id=None):
        if self.procestype_url is None:
            resultaten = self.client.referentie.get_resultaten().json()
            for resultaat in resultaten["results"]:
                if resultaat["procestermijn"] == "nihil":
                    self.procestype_url = resultaat["procesType"]
                    self.selectie_lijst_url = resultaat["url"]
                    break

        procestype_url = self.procestype_url
        if self.internal_service_endpoints is not None:
            procestype_url = self._replace_with_internal_service_address(
                self.procestype_url, self.internal_service_endpoints.vrl
            )

        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )

        gerelateerd_zaaktype = {
                    "zaaktype": identificatie,
                    "aardRelatie": "vervolg",
                    "toelichting": f"gerealteerd: {identificatie}",
                }

        new_id = randomizer.create_random_string(40)
        td = timedelta(days=1)
        d = datetime.utcnow() + td
        geldigheid = d.strftime("%Y-%m-%d")
        body = {
            "identificatie": new_id,
            "omschrijving": "thisisanothergeneratedtest " + self.naam,
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
            "toelichting": "handmatige ophoging",
            "verlengingMogelijk": True,
            "publicatieIndicatie": False,
            "productenOfDiensten": ["https://vng.nl/projecten/gemma-softwarecatalogus"],
            "selectielijstProcestype": procestype_url,
            "referentieproces": {"naam": "test", "link": ""},
            "deelzaaktypen": [],
            "catalogus": catalogus_url,
            "informatieobjecttypen": [],
            "besluittypen": [],
            "gerelateerdeZaaktypen": [],
            "beginGeldigheid": geldigheid,
            "versiedatum": geldigheid,
            "concept": True,
            "verlengingstermijn": "P5D",
        }
        if gerelateerd_zaaktype is not None:
            body["gerelateerdeZaaktypen"] = [gerelateerd_zaaktype]
        response = self.client.catalogus.create_zaaktype(body)
        return response

    def zaaktype(
        self, gerelateerd_zaaktype=None, add_deelzaak=True, add_besluittype=True
    ):
        identificatie = randomizer.create_random_string(40)

        if self.procestype_url is None:
            resultaten = self.client.referentie.get_resultaten().json()
            for resultaat in resultaten["results"]:
                if resultaat["procestermijn"] == "nihil":
                    self.procestype_url = resultaat["procesType"]
                    self.selectie_lijst_url = resultaat["url"]
                    break

        procestype_url = self.procestype_url
        if self.internal_service_endpoints is not None:
            procestype_url = self._replace_with_internal_service_address(
                self.procestype_url, self.internal_service_endpoints.vrl
            )

        catalogus_url = self.catalogus_url
        if self.internal_service_endpoints is not None:
            catalogus_url = self._replace_with_internal_service_address(
                self.catalogus_url, self.internal_service_endpoints.ztc
            )

        besluitentypen = []
        if self.besluit_type is not None and add_besluittype:
            besluitentypen.append(self.besluit_type["omschrijving"])

        deelzaken = []
        if self.deelzaak_type is not None and add_deelzaak:
            deelzaken.append(self.deelzaak_type["identificatie"])

        td = timedelta(days=10)
        delta = datetime.utcnow() - td
        geldigheid = delta.strftime("%Y-%m-%d")
        body = {
            "identificatie": identificatie,
            "omschrijving": "testzaaktype " + self.naam,
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
            "selectielijstProcestype": procestype_url,
            "referentieproces": {"naam": "test", "link": ""},
            "deelzaaktypen": deelzaken,
            "catalogus": catalogus_url,
            "informatieobjecttypen": [],
            "besluittypen": besluitentypen,
            "gerelateerdeZaaktypen": [],
            "beginGeldigheid": geldigheid,
            "versiedatum": geldigheid,
            "concept": True,
            "verlengingstermijn": "P5D",
        }

        if gerelateerd_zaaktype is not None:
            body["gerelateerdeZaaktypen"] = gerelateerd_zaaktype

        response = self.client.catalogus.create_zaaktype(body)
        self.zaaktype_url = response.json()["url"]
        return response

    def zaaktype_list(
        self, gerelateerd_zaaktype=False, add_deelzaaktype=False, add_besluittype=False
    ):
        if gerelateerd_zaaktype:
            zaaktypen = []
            for zaaktype in self.zaaktypen_list:
                body = {
                    "zaaktype": zaaktype["identificatie"],
                    "aardRelatie": "vervolg",
                    "toelichting": f"gerealteerd: {zaaktype['identificatie']}",
                }
                zaaktypen.append(body)
            response = self.zaaktype(
                gerelateerd_zaaktype=zaaktypen,
                add_deelzaak=add_deelzaaktype,
                add_besluittype=add_besluittype,
            )
            self.zaaktypen_list.append(response.json())
            return response
        response = self.zaaktype(
            add_deelzaak=add_deelzaaktype, add_besluittype=add_besluittype
        )
        self.zaaktypen_list.append(response.json())
        return response

    def zaaktype_informatie_relation(self):
        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        informatieobjecttype_url = self.informatieobjecttype_url
        if self.internal_service_endpoints is not None:
            informatieobjecttype_url = self._replace_with_internal_service_address(
                self.informatieobjecttype_url, self.internal_service_endpoints.ztc
            )

        body = {
            "zaaktype": zaaktype_url,
            "informatieobjecttype": informatieobjecttype_url,
            "volgnummer": 1,
            "richting": "inkomend",
        }
        return self.client.catalogus.create_zaaktype_informatieobjecttype_relation(body)

    def eigenschappen(self):
        eigenschap_naam = randomizer.create_random_string(8)
        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        body = {
            "naam": "eigenschap " + eigenschap_naam,
            "definitie": "for test",
            "zaaktype": zaaktype_url,
            "specificatie": {
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": ["test"],
            },
        }
        response = self.client.catalogus.create_eigenschap(body)
        self.zaaktype_eigenschap_url = response.json()["url"]
        return response

    def resultaattypen(self):
        resultaattypeomschrijvingen = self.client.referentie.get_omschrijvingen().json()
        self.resultaattypeomschrijving_url = resultaattypeomschrijvingen[0]["url"]

        selectie_lijst_url = self.selectie_lijst_url
        if self.internal_service_endpoints is not None:
            selectie_lijst_url = self._replace_with_internal_service_address(
                self.selectie_lijst_url, self.internal_service_endpoints.vrl
            )

        resultaattypeomschrijving_url = self.resultaattypeomschrijving_url
        if self.internal_service_endpoints is not None:
            resultaattypeomschrijving_url = self._replace_with_internal_service_address(
                self.resultaattypeomschrijving_url, self.internal_service_endpoints.vrl
            )

        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        body = {
            "zaaktype": zaaktype_url,
            "omschrijving": "Klaar",
            "resultaattypeomschrijving": resultaattypeomschrijving_url,
            "selectielijstklasse": selectie_lijst_url,
            "brondatumArchiefprocedure": {
                "afleidingswijze": "afgehandeld",
                "procestermijn": None,
                "datumkenmerk": "",
                "einddatumBekend": False,
                "objecttype": "",
                "registratie": "",
            },
        }

        resp = self.client.catalogus.create_resultaattype(body)
        self.resultaattype = resp
        self.resultaattype_url = resp.json()["url"]

    def statustype_begin_end(self):
        omschrijvingen = ["Begin", "Einde"]

        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        for i, omschrijving in enumerate(omschrijvingen, 1):
            body = {
                "omschrijving": omschrijving,
                "zaaktype": zaaktype_url,
                "volgnummer": i,
            }
            response = self.client.catalogus.create_statustype(body).json()
            if i < len(omschrijvingen):
                self.statustype_begin = response["url"]
            else:
                self.statustype_eind = response["url"]
        return

    def roltype(self):
        zaaktype_url = self.zaaktype_url
        if self.internal_service_endpoints is not None:
            zaaktype_url = self._replace_with_internal_service_address(
                self.zaaktype_url, self.internal_service_endpoints.ztc
            )

        body = {
            "zaaktype": zaaktype_url,
            "omschrijving": "testroltype",
            "omschrijvingGeneriek": "adviseur",
        }

        response = self.client.catalogus.create_roltype(body)
        self.roltype_url = response.json()["url"]

    def rollen(self):
        roltype_url = self.roltype_url
        if self.internal_service_endpoints is not None:
            roltype_url = self._replace_with_internal_service_address(
                self.roltype_url, self.internal_service_endpoints.ztc
            )

        body = {
            "zaak": self.zaak_url,
            "betrokkene": "http://example.com/2d0815580af94ee0a15aa677aa646e1a",
            "betrokkeneType": "natuurlijk_persoon",
            "rolomschrijving": "behandelaar",
            "roltoelichting": "testrol",
            "roltype": roltype_url,
        }

        response = self.client.zaken.create_rollen(body)
        self.rol_url = response.json()["url"]

    def zaakeigenschappen(self):
        zaaktype_eigenschap_url = self.zaaktype_eigenschap_url
        if self.internal_service_endpoints is not None:
            zaaktype_eigenschap_url = self._replace_with_internal_service_address(
                self.zaaktype_eigenschap_url, self.internal_service_endpoints.ztc
            )

        body = {
            "zaak": self.zaak_url,
            "eigenschap": zaaktype_eigenschap_url,
            "waarde": "test",
        }

        response = self.client.zaken.create_zaakeigenschappen(
            body=body, uuid=self.zaak_uuid
        )
        self.zaak_eigenschap_url = response.json()["url"]

    def zaakobjecten(self):
        body = {
            "zaak": self.zaak_url,
            "objectType": "pand",
            "objectIdentificatie": {"identificatie": "test"},
        }

        response = self.client.zaken.create_zaakobjecten(body)

    def klantcontacten(self):
        body = {
            "zaak": self.zaak_url,
            "datumtijd": datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
        }

        response = self.client.zaken.create_klantcontacten(body)

    def publish_types(self):
        if self.besluittype_url is not None:
            self.client.catalogus.publish_type(self.besluittype_url)

        if self.informatieobjecttype_url is not None:
            self.client.catalogus.publish_type(self.informatieobjecttype_url)

        if self.deelzaaktype_url is not None:
            self.client.catalogus.publish_type(self.deelzaaktype_url)

        if self.zaaktype_url is not None:
            self.client.catalogus.publish_type(self.zaaktype_url)
