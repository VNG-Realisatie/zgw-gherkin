#language: nl

Functionaliteit: Zaken moeten bevraagbaar zijn via de zaken-api
  Om te testen dat een zaak die bestaat ook daadwerkelijk op te halen is
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen
  Zodat ik gegevens terug krijg

Scenario: zaak heeft veld: 'vertrouwelijkheidsaanduiding' met 'Openbaar'
    Gegeven de zaken-api is beschikbaar
    Als zaken wordt gezocht met de volgende parameters
    | naam                | waarde                |
    | identificatie       | ZAAK-2019-0000002193  |
    Dan heeft de response 1 zaak met de volgende gegevens
    | naam                         | waarde                               |
	| uuid                         | 1053b85b-2e72-4218-9fc3-3b67dda82c2e |
    | identificatie                | ZAAK-2019-0000002193                 |
    | vertrouwelijkheidaanduiding  | openbaar                             |
	| startdatum                   | 2019-04-09                           |
	| verantwoordelijkeOrganisatie | 000000000                            |
    | zaaktype                     | https://catalogi-api.vng.cloud/api/v1/zaaktypen/693d51a9-6c3f-4742-99e1-2d421cb75dc0 |
    | betalingsindicatie           | geheel |