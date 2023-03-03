#language: nl

Functionaliteit: Zaken moeten bevraagbaar zijn via de zaken-api
  Om te testen dat een zaak die bestaat ook daadwerkelijk op te halen is
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen
  Zodat ik gegevens terug krijg

  @token.set
  Abstract Scenario: Een complete zaak aanmaken
    Gegeven de catalogus-api is beschikbaar
    En de zaken-api is beschikbaar
    Als er een nieuwe valide catalogus aangemaakt wordt
    En er een valide besluittype aangemaakt wordt
    En er een valide informatieobjecttype aangemaakt wordt
    En er een valide deelzaaktype aangemaakt wordt
    En er een valide zaaktype aangemaakt wordt
    En er een relatie wordt gelegd tussen het zaaktype en informatieobjecttype
    En er een valide eigenschap aangemaakt wordt
    En er een valide statussen aangemaakt wordt
    En er een valide rol aangemaakt wordt
    En de benodigde typen worden gepubliceerd
    En er een valide enkelvoudiginformatieobject aangemaakt wordt
    En er valide gebruiksrechten worden aangemaakt
    En er een valide enkelvoudiginformatieobject aangemaakt wordt met <veld> <waarde>
    En er wordt een valide zaak aangemaakt met <archief_status>
    Dan is er een zaak aangemaakt met statuscode 201 terug
    En is de zaak terug te vinden

   Voorbeelden: Zaak
     | veld                   | waarde |  archief_status    |
     | indicatieGebruiksrecht | null   |  nog_te_archiveren |

  @token.set
  @zaak.basis
  Abstract Scenario: Zaak sluiten zet einddatum, archiefactiedatum en archiefnominatie (ZRC-008-A)
    Gegeven de zaken-api is beschikbaar
    Als er wordt een valide zaak aangemaakt met <archief_status>
    En er een resultaat aan de zaak wordt toegevoegd met een resultaattype
    En er een eindstatus met de datum van vandaag aan de zaak wordt toegevoegd
    Dan staan einddatum op vandaag, archiefactiedatum op <archiefactiedatum> jaar in de toekomst en archiefnominatie op <archiefnominatie>

   Voorbeelden: ZRC-008-A
    |  archief_status    | archiefactiedatum | archiefnominatie |
    | nog_te_archiveren  | 10                | vernietigen      |

  @token.set
  @zaak.basis
  Abstract Scenario: Zaak afsluiten en heropenen zet einddatum, archiefactiedatum en archiefnominatie op null (ZRC-008-B)
    Gegeven de zaken-api is beschikbaar
    Als er wordt een valide zaak aangemaakt met <archief_status>
    En er een resultaat aan de zaak wordt toegevoegd met een resultaattype
    En er een eindstatus met de datum van vandaag aan de zaak wordt toegevoegd
    En de zaak wordt heropend met een begin statustype
    Dan staan einddatum, archiefactiedatum en archiefnominatie op null

   Voorbeelden: ZRC-008-B
    |  archief_status    |
    | nog_te_archiveren  |

  @token.set
  @zaak.compleet
  Abstract Scenario: Expand op de zaken-api get mogelijk
    Gegeven er is een zaak beschikbaar
    Als het veld <veld> geexpand wordt bij de list operatie
    Dan is het veld <veld> opgenomen in de response

   Voorbeelden: Expand
    | veld      |
    | zaaktype,rollen.statussen.zaak.rollen,status.zaak,zaakobjecten,zaakinformatieobjecten |
    | status.zaak.zaaktype.zaak.zaaktype.zaak |


  @token.set
  @zaak.compleet
  Abstract Scenario: Expand op de zaken-api get niet mogelijk bij te lange of te diepe queries
    Gegeven er is een zaak beschikbaar
    Als het veld <veld> geexpand wordt bij de list operatie
    Dan krijgt de gebruiker statuscode 400 terug

   Voorbeelden: Expand
    | veld      |
    | rollen.zaak.rollen.zaak.rollen.zaak.rollen.zaak |
