#language: nl

Functionaliteit: Zaakdossiers moeten na afsluiten duurzaam toegankelijk gehouden worden. Om dit te mogelijk te maken moet aan een aantal voorwaarden worden voldaan.
  Als een informatiebeheerder
  wil ik dat zaakdossiers voor het afsluiten van de zaak beschikken over een minimale set kenmerken
  zodat ik deze dossiers goed kan beheren en eventueel op het juiste moment kan vernietigen

Scenario: afsluiten zaak - zaak heeft geen resultaat
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als de zaak geen resultaat (Zaak.Resultaat) heeft,
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet door de consumer eerst een resultaat worden aangemaakt.

Scenario: afsluiten zaak - indicatie gebruiksrecht niet voor alle informatieobjecten expliciet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als niet voor ieder van de aan de zaak gerelateerde informatieobjecten expliciet (true/false) een indicatie gebruiksrecht vastgelegd (Zaak.Informatieobject.indicatieGebruiksrecht) is,
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet voor de informatieobjecten zonder expliciete indicatie gebruiksrecht door de consumer eerst alsnog een expliciete (true/false) indicatie gebruiksrecht vastgelegd worden.

Scenario: afsluiten zaak - status bij niet alle informatieobjecten "gearchiveerd"
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als niet bij ieder van de aan de zaak gerelateerde informatieobjecten bij status (Zaak.Informatieobject.status) de waarde "gearchiveerd" is vastgelegd,
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet voor de informatieobjecten waar de waarde bij status niet "gearchiveerd" is door de consumer alsnog deze waarde worden vastgelegd.

Scenario: afsluiten zaak - archiefnominatie is niet vastgelegd en niet afleidbaar
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als de archiefnominatie van de zaak (Zaak.archiefnominatie) niet geregeistreerd is,
  en bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure) geen waarde vastgelegd is
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet door de consumer eerst een archiefnominatie worden vastgelegd.

Scenario: afsluiten zaak - archiefnominatie is niet vastgelegd maar wel afleidbaar
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als de archiefnominatie van de zaak (Zaak.archiefnominatie) niet geregeistreerd is,
  en bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure) de waarde "blijvend_bewaren" of "vernietigen" vastgelegd is
  dan moet de Zaken API de waarde bij de archiefnominatie bij het resultaattype overnemen bij de zaak (Zaak.archiefnominatie).

Scenario: afsluiten zaak - afleidingswijze brondatum archiefprocedure "afgehandeld" - einddatum zaak niet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door daarbij de eindstatus aan aan te maken.
  Als de afleidingswijze voor de brondatum van de archiefprocedure bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure.afleidingswijze) "afgehandeld" is,
  en bij de einddatum van de zaak (Zaak.einddatum) géén geldige datumwaarde is ingevuld,
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet door de consumer eerst de einddatum worden vastgelegd.

Scenario: afsluiten zaak - afleidingswijze brondatum archiefprocedure "afgehandeld" - einddatum zaak vastgelegd, archiefactiedatum niet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door daarbij de eindstatus aan aan te maken.
  Als bij de archiefactiedatum (Zaak.archiefactiedatum) van de zaak géén geldige datumwaarde is vastgelegd,
  en de afleidingswijze voor de brondatum van de archiefprocedure bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure.afleidingswijze) "afgehandeld" is,
  en bij de einddatum van de zaak (Zaak.einddatum) een geldige datumwaarde is ingevuld,
  dan legt de Zaken API bij archiefactiedatum (Zaak.archiefactiedatum) de datumwaarde vast die de som is van de einddatum van de zaak (Zaak.einddatum) verhoogd met de archiefactietermijn die hoort bij het resultaattype (Zaak.Resultaat.Resultaattype.archiefactietermijn) van het resultaat van de zaak.

Scenario: afsluiten zaak - afleidingswijze brondatum archiefprocedure "termijn" - einddatum zaak niet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door daarbij de eindstatus aan aan te maken.
  Als de afleidingswijze voor de brondatum van de archiefprocedure bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure.afleidingswijze) "termijn" is,
  en bij de einddatum van de zaak (Zaak.einddatum) géén geldige datumwaarde is ingevuld,
  dan kan de zaak (nog) niet worden afgesloten - daarvoor moet door de consumer eerst de einddatum worden vastgelegd.

Scenario: afsluiten zaak - afleidingswijze brondatum archiefprocedure "termijn" - einddatum zaak vastgelegd, archiefactiedatum niet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door daarbij de eindstatus aan aan te maken.
  Als bij de archiefactiedatum (Zaak.archiefactiedatum) van de zaak géén geldige datumwaarde is vastgelegd,
  en de afleidingswijze voor de brondatum van de archiefprocedure bij het resultaattype waarvan van het resultaat van de zaak een instantie is (Zaak.Resultaat.Resultaattype.brondatumArchiefprocedure.afleidingswijze) "termijn" is,
  en bij de einddatum van de zaak (Zaak.einddatum) een geldige datumwaarde is ingevuld,
  dan legt de Zaken API bij archiefactiedatum (Zaak.archiefactiedatum) de datumwaarde vast die de som is van de einddatum van de zaak (Zaak.einddatum) verhoogd met de procestermijn (Resultaat.Resultaattype.brondatumArchiefprocedure.procestermijn) én verhoogd met de archiefactietermijn (Zaak.Resultaat.Resultaattype.archiefactietermijn) die horen bij het resultaattype van het resultaat van de zaak.

Scenario: afsluiten zaak - archiefactiedatum zaak vastgelegd, archiefstatus zaak niet vastgelegd
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door daarbij de eindstatus aan aan te maken.
  Als bij archiefactiedatum (Zaak.archiefactiedatum) een geldige datumwaarde is vastgelegd, terwijl de archiefstatus (Zaak.archiefstatus) van de zaak níet is vastgelegd,
  dan legt de Zaken API bij archiefstatus (Zaak.archiefstatus) de waarde "gearchiveerd" vast.

Scenario: afsluiten zaak - status is niet eindstatus
  Gegeven dat een medewerker de zaak met uuid "095be615-a8ad-4c33-8e9c-c7612fbf6c9f" wil afsluiten door het aanmaken van de eindstatus.
  Als het statustype waarvan de aan te maken status een instantie is van alle bij het zaaktype behorende statustypen niet het hoogste volgnummer (Zaak.Status.Statustype.volgnummer) heeft,
  dan wordt de zaak (nog) niet afgesloten - daarvoor moet door de consumer eerst de eindstatus aangemaakt worden.

{::comment}
Dit is een eerste aanzetje, waarin alleen de eerste (en meest eenvoudige) twee van de acht afleidingswijzen voor de brondatum van de archiefprocedure zijn verwerkt. Om volledig te kunnen valideren moet het aantal scenario's dus nog worden uitgebreid.
{:/comment}