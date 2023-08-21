#language: nl

Functionaliteit: Catalogi items moeten aan bepaalde regels voldoen
  Om te testen dat een catalogi items aan te maken zijn
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen en waar nodig aanvullen
  Zodat ik de catalogus als basis kan gebruiken voor verdere acties

Scenario: aanmaken van een catalogus
  Gegeven de catalogus-api is beschikbaar
  En er is een valide token gezet
  Als er een nieuwe valide catalogus aangemaakt wordt
  Dan krijgt de gebruiker statuscode 201 terug

@token.set
@catalogus
Scenario: een aangemaakt catalogus is via filters terug te vinden
  Gegeven de catalogus-api is beschikbaar
  Als de catalogus wordt gezocht met parameters
  | parameter |
  | rsin      |
  | domein    |
  Dan krijgt de gebruiker de catalogus terug met de juiste informatie
