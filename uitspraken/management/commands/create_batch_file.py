from django.core.management.base import BaseCommand
from uitspraken.models import Uitspraak
import json


class Command(BaseCommand):
    help = "Create batch file for Uitspraken"

    def handle(self, *args, **options):
        uitspraken = Uitspraak.objects.all()
        filename = "batch_get_verdict_241112_1.jsonl"
        with open(filename, "w") as file:
            for uitspraak in uitspraken:
                # if uitspraak.beslissing and (not uitspraak.oordeel or uitspraak.oordeel == 0):
                if uitspraak.beslissing:
                    custom_id = str(uitspraak.id)
                    model = "gpt-4o"
                    method = "POST"
                    url = "/v1/chat/completions"
                    text = uitspraak.beslissing[:10000]
                    prompt = f"""     
                        ### Opdracht       
                        Je leest zo een beslissing van de Nederlandse Raad van State en bepaalt wat van toepassing is en slaat het antwoord op in de variabele [oordeel] in de vorm van een cijfer.
                        
                        ### Instructie:
                        1. Lees de volgende uitspraak van de Raad van State:
                        
                        "{text}"
                        
                        2. Als het beroep niet ontvankelijk wordt verklaard van __alle__ appellanten, dan is [oordeel] = 1. Ga naar stap 14. 
                        3. Als de bestuursrechter zich onbevoegd verklaart om uitspraak te doen, dan is [oordeel] = 2. Ga naar stap 14.
                        4. Als in de beslissing uitspraak wordt gedaan over het "niet tijdig nemen van een besluit", dan is [oordeel] = 1. Ga naar stap 14.
                        5. Als de bestuursrechter een voorlopige voorziening afwijst of toewijst en er wordt geen definitieve uitspraak gedaan, dan is [oordeel] = 3. Ga naar stap 14.
                        6. Soms worden in een beslissing meerdere uitspraken gedaan over hetzelfde plan, vaak worden in dit geval meerdere data genoemd in de beslissing. Dit is te herkennen aan bewoordingen als "gewijzigde vaststelling" of "herziene vaststelling". En vaak ook: "Vernietigt de onder ... genoemde besluiten". Daarna volgt dan het definitieve oordeel. Als dit het geval is, ga naar stap 7. Als dat niet het geval is, ga naar stap 9.
                        7. __let op__: Kijk hier naar het oordeel met de meest recente datum en negeer wat wordt gezegd over oudere uitspraken. Vaak staan de uitspraken op oplopende chronologische volgorde, dus staat de meest recente uitspraak als laatste. Kijk in dit geval naar de laatste uitspraken met meest recente datum. Als de definitieve uitspraak van een herziene of gewijzigde vaststelling (bijvoorbeeld verwoord via "op onderdelen gewijzigd is vastgesteld") voor een van de appellanten of alle appellanten __gegrond__ is, dan is [oordeel] = 4. Ga naar stap 14.
                        8. __let op__: Kijk hier naar het oordeel met de meest recente datum en negeer wat wordt gezegd over oudere uitspraken. Vaak staan de uitspraken op oplopende chronologische volgorde, dus staat de meest recente uitspraak als laatste. Kijk in dit geval naar de laatste uitspraken met meest recente datum. Als de definitieve uitspraak van een herziene of gewijzigde vaststelling (bijvoorbeeld verwoord via "op onderdelen gewijzigd is vastgesteld") voor een van de appellanten of alle appellanten __ongegrond__ is, dan is [oordeel] = 5. Ga naar stap 14. 
                        9. Als het beroep __voor alle appellanten__ geheel ongegrond wordt verklaard en/of de aangevallen uitspraak wordt geheel bevestigd en/of er wordt bepaald dat de rechtsgevolgen geheel in stand blijven en/of draagt op de geconstateerde gebreken te herstellen door een ander besluit te nemen, dan is [oordeel] = 6. Ga naar stap 14.
                        10. Als het beroep __voor alle appellanten__ geheel gegrond wordt verklaard, maar de rechtsgevolgen blijven in stand, dan is [oordeel] = 7. Ga naar stap 14.
                        11. Als het beroep __voor alle appellanten__ __geheel__ gegrond wordt verklaard, dan is [oordeel] = 8. Ga naar stap 14.
                        12. Als het beroep gedeeltelijk gegrond wordt verklaard al dan niet voor een deel van de appellanten en het bestreden besluit wordt gedeeltelijk vernietigd (te herkennen aan bewoordingen als In dit geval komen de woorden “vernietigt het besluit van …….voor zover het betreft, wat betreft” of “bepaalt dat artikel …….. komt te luiden” of “bepaalt dat deze uitspraak in de plaats treedt van het besluit voor wat betreft het vernietigde deel ” of “de rechtsgevolgen van het vernietigde gedeelte van het besluit blijven geheel in stand “ of “bepaalt dat deze uitspraak in de plaats treedt van het besluit voor wat betreft het vernietigde deel ” of “met inachtneming van wat in deze uitspraak is overwogen” of “de gebreken in het besluit van … datum … te herstellen of in plaats daarvan een gewijzigd besluit te nemen”). Dan is [oordeel] = 9. Ga naar stap 14.
                        13. In alle andere gevallen is [oordeel] = 10. Ga naar stap 14.
                        14. Geef als output de waarde van [oordeel].
                        
                        ### Voorbeelden
                        
                        - **Input: ** "I. bevestigt de uitspraak van de rechtbank;
                        II. verklaart het beroep van [partij] tegen het besluit van 10 mei 2021, kenmerk 153300, ongegrond;
                        III. veroordeelt het college van burgemeester en wethouders van Berkelland tot vergoeding van bij [partij] in verband met de behandeling van het hoger beroep van het college opgekomen proceskosten tot een bedrag van € 759,00, geheel toe te rekenen aan door een derde beroepsmatig verleende rechtsbijstand;
                        IV. bepaalt dat van het college van burgemeester en wethouders van Berkelland een griffierecht van € 541,00 wordt geheven."
                        **Output:** 6
                        - **Input: ** "I. verklaart het hoger beroep gegrond;
                        II. vernietigt de uitspraak van de rechtbank Den Haag van 26 maart 2021 in zaak nr. 19/3218;
                        III. verklaart het bij de rechtbank ingestelde beroep gegrond;
                        IV. vernietigt het besluit van het college van burgemeester en wethouders van Oegstgeest van 9 april 2019 met kenmerk Z/18/113961/244117;
                        V. draagt het college van burgemeester en wethouders van Oegstgeest op om binnen 26 weken na de verzending van deze uitspraak met inachtneming van wat daarin is overwogen een nieuw besluit op bezwaar te nemen;
                        VI. bepaalt dat tegen het nieuw te nemen besluit op bezwaar slechts bij de Afdeling bestuursrechtspraak van de Raad van State beroep kan worden ingesteld;
                        VII. gelast dat het college van burgemeester en wethouders van Oegstgeest aan Stichting Dorpscentrum Oegstgeest en andere het door hen voor de behandeling van het beroep en het hoger beroep betaalde griffierecht ten bedrage van € 717,00 vergoedt, met dien verstande dat bij betaling van genoemd bedrag aan een van hen het college aan zijn betalingsverplichting heeft voldaan."
                        **Output:** 8
                        
                        - **Input: ** I.        verklaart de beroepen van:
                        a.       [appellant sub 1];
                        b.       [appellant sub 2];
                        tegen het besluit van 13 oktober 2020 van de raad van de gemeente Wassenaar tot vaststelling van het bestemmingsplan "Wassenaar, Vreeburglaan", gegrond;
                        II.       vernietigt het besluit van 13 oktober 2020 van de raad van de gemeente Wassenaar tot vaststelling van het bestemmingsplan "Wassenaar, Vreeburglaan";
                        III.      verklaart het beroep van [appellant sub 3] tegen het besluit van 21 september 2021 van de raad van de gemeente Wassenaar niet-ontvankelijk;
                        IV.     verklaart de beroepen van:
                        a.       [appellant sub 1];
                        b.       [appellant sub 2];
                        tegen het besluit van 21 september 2021 van de raad van de gemeente Wassenaar ongegrond;
                        **Output:** 5
                        
                        ### Belangrijk
                        - Geef het antwoord uitsluitend in de vorm van een enkel cijfer van 1 tot en met 10.
                        - Geef geen toelichting bij het antwoord.
                        - Herhaal de tekst niet in je antwoord.
                        """

                    data = {
                        "custom_id": custom_id,
                        "method": method,
                        "url": url,
                        "body": {
                            "model": model,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Je bent een expert in het lezen van juridische uitspraken."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                        }
                    }
                    file.write(json.dumps(data) + "\n")

        self.stdout.write(self.style.SUCCESS("Successfully created batch file"))
