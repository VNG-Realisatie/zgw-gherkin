#language: nl

Functionaliteit: Zaken moeten bevraagbaar zijn via de zaken-api
  Om te testen dat een zaak die bestaat ook daadwerkelijk op te halen is
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen
  Zodat ik gegevens terug krijg

Abstract Scenario: Een complete zaak aanmaken
  Gegeven de catalogus-api is beschikbaar
  En er is een valide token gezet
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
