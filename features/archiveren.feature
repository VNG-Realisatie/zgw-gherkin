#language: nl

Functionaliteit: laden van de juiste fixture


@token.set
@zaak.basis
Abstract Scenario: registreren eindstatus zaak en afleiden juiste archiveringsparameters
  Gegeven er wordt een valide zaak aangemaakt met <archief_status>
  En dat deze zaak een begin status heeft
  #todo
  En deze zaak nog niet de eindstatus bereikt heeft
  En dat de archiefnominatie van de zaak nog niet bekend is
  #todo fixture
  En voor alle aan deze zaak gerelateerde informatieobjecten de status <informatieobject_status> heeft en indicatie_gebruiksrecht <indicatie_gebruiksrecht>
  En er een resultaat aan de zaak wordt toegevoegd met een resultaattype
  En dat het resultaattype archiefnominatie <archiefnominatie> en archiefactietermijn <archiefactietermijn> en archiefprocedure <archiefprocedure> heeft
  En dat deze zaak geen einddatum heeft
  Als een medewerker de eindstatus vastlegt
  Dan reageert de Zaken API met een code 201
  En registreert de Zaken API bij archiefstatus de waarde <archiefstatus> en archiefnominatie <archiefnominatie>
  En registreert de Zaken API bij archiefactietermijn de einddatum van de zaak, verhooogd met bij het resultaattype geregistreerde archiefactietermijn

     Voorbeelden: ARC-001
    | archief_status    | informatieobject_status | indicatie_gebruiksrecht | archiefnominatie | archiefactietermijn | archiefprocedure | archiefstatus |
    | nog_te_archiveren | gearchiveerd            | True                    | vernietigen |          P10Y          | afgehandeld     |         gearchiveerd         |
