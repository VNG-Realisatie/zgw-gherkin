#language: nl

Functionaliteit: Het grote historiemodel
  Om te testen dat een zaak die bestaat ook daadwerkelijk op te halen is
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen
  Zodat ik gegevens terug krijg

  @token.set
  Scenario: Historie van een zaaktype met gerelateerde zaaktypen laat de correcte gerelateerde zaaktypen zien
    Gegeven de catalogus-api is beschikbaar
    Als er een nieuwe valide catalogus aangemaakt wordt
    En er een valide informatieobjecttype aangemaakt wordt
    En er een besluittype aangemaakt wordt met het informatieobjecttype
    En er een zaaktype aangemaakt wordt
    En er een valide eigenschap aangemaakt wordt
    En er een valide statussen aangemaakt wordt
    En er een valide rol aangemaakt wordt
    En er een valide zaaktypeinformatieobjecttype met zaaktype_url en het informatieobjecttype
    En er een zaaktype wordt aangemaakt met een gerelateerd zaaktype
    En er een valide eigenschap aangemaakt wordt
    En er een valide statussen aangemaakt wordt
    En er een valide rol aangemaakt wordt
    En deze zaaktypen worden gepubliceerd
    En het zaaktype met gerelateerd zaaktype opgevraagd wordt verwijst het gerelateerde zaaktype naar het eerste zaaktype
    En er een nieuw concept versie zaaktype met zaaktypeidentificatie van het gerelateerde zaaktype wordt aangemaakt
    En het gerelateerde zaaktype een datum van vandaag krijgt
    En het nieuwe concept wordt gepubliceerd
    En het zaaktype opgevraagd word
    Dan moeten de gerelateerdeZaaktype naar de juiste versie wijzen

  @token.set
  Scenario: Historie van een zaaktype met besluittype moet het correct besluittype laten zien
    Gegeven de catalogus-api is beschikbaar
    Als er een nieuwe valide catalogus aangemaakt wordt
    En er een valide informatieobjecttype aangemaakt wordt
    En er een besluittype aangemaakt wordt met het informatieobjecttype
    En het besluittype gepubliceerd wordt
    En het besluittype een datum van vandaag krijgt
    En er een zaaktype aangemaakt wordt met identificatie en besluittype
    En er een valide eigenschap aangemaakt wordt
    En er een valide statussen aangemaakt wordt
    En er een valide rol aangemaakt wordt
    En er een valide zaaktypeinformatieobjecttype met zaaktype_url en het informatieobjecttype
    En deze zaaktypen worden gepubliceerd
    En er een nieuwe besluittype wordt aangemaakt door de reactietermijn omhoog te zetten
    En het zaaktype opgevraagd word
    Dan moeten de besluittypen naar de juiste versie wijzen
