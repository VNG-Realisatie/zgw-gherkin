#language: nl

Functionaliteit: laden van de juiste fixture


@archiveren.valide
Scenario: registreren eindstatus zaak en afleiden juiste archiveringsparameters
  Gegeven dat een zaak bestaat
  En dat deze zaak een status heeft
  En deze zaak nog niet nog niet de eindstatus bereikt heeft
  En deze zaak de archiefststatus "nog_te_archiveren" heeft
  En dat de archiefnominatie van de zaak nog niet bekend is
  En voor alle aan deze zaak gerelateerde informatieobjecten de status "gearchiveerd" is
  En voor alle aan deze zaak gerelateerde informatieobjecten de indicatie_gebruiksrecht "true" of "false" is
  En aan dat de zaak een resultaat heeft
  En dat voor het resultaattype waarvan het zaakrestultaat een instantie is de waarde van archiefnominatie "blijvend_bewaren" of "vernietigen" is
  En dat voor het resultaattype waarvan het zaakrestultaat een instantie is de waarde van archiefactietermijn een geldige tijdsduurwaarde is
  En dat voor het resultaattype waarvan het zaakrestultaat een instantie is de afleidingswijze voor de brondatum van de archiefprocedure "afgehandeld" is
  En dat deze zaak een einddatum heeft
  Als een medewerker de eindstatus vastlegt
  Dan reageert de Zaken API met een code 201
  En registreert de Zaken API bij archiefnominatie de waarde van het gelijknamige attribuut bij het resultaattype
  En registreert de Zaken API bij archiefactietermijn de einddatum van de zaak, verhooogd met bij het resultaattype geregistreerde archiefactietermijn
  En registreert de Zaken API bij archiefstatus de waarde "gearchiveerd"