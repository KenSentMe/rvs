from openai import OpenAI, OpenAIError
import traceback
import json
import os

if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
else:
    import rvs.openai.key as key
    client = OpenAI(
        api_key=key.openai_key,
    )


def send_prompt(prompt):

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
            n=1,
        )
        answer = (
            response.choices[0].message.content.strip().strip('"').strip("!")
        )

        return answer
    except Exception as e:
        print(prompt)
        print(e)
        traceback.print_exc()
        return None


def get_place(text):

    prompt = f"""Over welke plaats gaat de volgende text:
    
                "{text}"
                
                Als antwoord wil ik de plaats en de provincie waarin de plaats ligt in de vorm van 
                een Python list. Als je geen antwoord hebt, geef dan als antwoord ["onbekend", "onbekend"] op.
                Antwoord:
                """
    answer = send_prompt(prompt)
    if answer:
        return json.loads(answer)

    return None


def get_clear_verdict(text):

        prompt = f"""     
### Instructie        
Je bent een expert in het lezen van juridische uitspraken. Lees de volgende uitspraak van de Raad van State:

"{text}"

Er zijn 2 opties:

1. Het beroep wordt ongegrond verklaard, de uitspraak van de rechtbank wordt bevestigd. Er worden verder **geen** voorwaarden gesteld, zoals het betalen van proceskosten.
2. Anders

### Output
Geef het nummer van de optie die volgens jou van toepassing is.

### Voorbeelden

- **Input: ** "I. bevestigt de uitspraak van de rechtbank;
II. verklaart het beroep van [partij] tegen het besluit van 10 mei 2021, kenmerk 153300, ongegrond;
III. veroordeelt het college van burgemeester en wethouders van Berkelland tot vergoeding van bij [partij] in verband met de behandeling van het hoger beroep van het college opgekomen proceskosten tot een bedrag van € 759,00, geheel toe te rekenen aan door een derde beroepsmatig verleende rechtsbijstand;
IV. bepaalt dat van het college van burgemeester en wethouders van Berkelland een griffierecht van € 541,00 wordt geheven."
**Output:** 2
- **Input: ** "I. bevestigt de uitspraak van de rechtbank, voor zover aangevallen;"
**Output:** 

### Belangrijk
- Geef het antwoord uitsluitend in de vorm van een enkel cijfer 1 of 2.
- Geef geen toelichting bij het antwoord.
"""
        try:
            answer = send_prompt(prompt)
        except OpenAIError as e:
            print(e)
            return None

        if answer:
            try:
                return int(answer)
            except TypeError:
                return None


def get_verdict(text):

    prompt = f"""
### Opdracht       
Je bent een expert in het lezen van juridische uitspraken. Je leest zo een beslissing van de Nederlandse Raad van State
en bepaalt wat van toepassing is en slaat het antwoord op in de variabele [oordeel] in de vorm van een cijfer.


### Instructie:
1. Lees de volgende uitspraak van de Raad van State:

"{text}"

2. Als het beroep niet ontvankelijk wordt verklaard van __alle__ appellanten, dan is [oordeel] = 1. Ga naar stap 13. 
3. Als de bestuursrechter zich onbevoegd verklaart om uitspraak te doen, dan is [oordeel] = 2. Ga naar stap 13.
4. Als de bestuursrechter een voorlopige voorziening afwijst of toewijst en er wordt geen definitieve uitspraak gedaan, dan is [oordeel] = 3. Ga naar stap 13.
5. Soms worden in een beslissing meerdere uitspraken gedaan over hetzelfde plan. Dit is te herkennen aan bewoordingen als "gewijzigde vaststelling" of "herziene vaststelling". En vaak ook: "Vernietigt de onder ... genoemde besluiten". Daarna volgt dan het definitieve oordeel. Als dit het geval is, ga naar stap 6. Als dat niet het geval is, ga naar stap 8.
6. Als de definitieve uitspraak van een herziene of gewijzigde vaststelling voor een van de appellanten of alle appellanten __gegrond__ is, dan is [oordeel] = 4. Ga naar stap 13.
7. Als de definitieve uitspraak van een herziene of gewijzigde vaststelling voor een van de appellanten of alle appellanten __ongegrond__ is dan is [oordeel] = 5. Ga naar stap 13. 
8. Als het beroep __voor alle appellanten__ geheel ongegrond wordt verklaard en/of de aangevallen uitspraak wordt geheel bevestigd en/of er wordt bepaald dat de rechtsgevolgen geheel in stand blijven en/of draagt op de geconstateerde gebreken te herstellen door een ander besluit te nemen, dan is [oordeel] = 6. Ga naar stap 13.
9. Als het beroep __voor alle appellanten__ geheel gegrond wordt verklaard, maar de rechtsgevolgen blijven in stand, dan is [oordeel] = 7. Ga naar stap 13.
10. Als het beroep __voor alle appellanten__ __geheel__ gegrond wordt verklaard, dan is [oordeel] = 8. Ga naar stap 13.
11. Als het beroep gedeeltelijk gegrond wordt verklaard al dan niet voor een deel van de appellanten en het bestreden besluit wordt gedeeltelijk vernietigd (te herkennen aan bewoordingen als In dit geval komen de woorden “vernietigt het besluit van …….voor zover het betreft, wat betreft” of “bepaalt dat artikel …….. komt te luiden” of “bepaalt dat deze uitspraak in de plaats treedt van het besluit voor wat betreft het vernietigde deel ” of “de rechtsgevolgen van het vernietigde gedeelte van het besluit blijven geheel in stand “ of “bepaalt dat deze uitspraak in de plaats treedt van het besluit voor wat betreft het vernietigde deel ” of “met inachtneming van wat in deze uitspraak is overwogen” of “de gebreken in het besluit van … datum … te herstellen of in plaats daarvan een gewijzigd besluit te nemen”). Dan is [oordeel] = 9. Ga naar stap 13.
12. In alle andere gevallen is [oordeel] = 10. Ga naar stap 13.
13. Geef als output de waarde van [oordeel].

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

### Belangrijk
- Geef het antwoord uitsluitend in de vorm van een enkel cijfer van 1 tot en met 10.
- Geef geen toelichting bij het antwoord.
- Herhaal de tekst niet in je antwoord.
"""

    try:
        answer = send_prompt(prompt)
    except OpenAIError:
        return None

    if answer:
        try:
            return int(answer)
        except:
            return None


def get_parties(text):

    prompt = f"""Lees deze uitspraak van de Raad van State:

            "{text}"
            
            Beantwoord 2 vragen:
            
            1: Wie is de appelant of wie zijn de appelanten, geef een omschrijving?
            2: Tegen welke tegenpartij hebben zij een geding?
            
            Antwoord uitsluitend in een Python list met de volgende opzet: ["<omschrijving appelant(en)>", "<tegenpartij>"]
            """
    answer = send_prompt(prompt)
    if answer:
        return json.loads(answer)

    return None


def get_metadata(text):

    prompt = f"""Lees deze uitspraak van de Raad van State:

                "{text}"

                Beantwoord 2 vragen:

                1: Wie is de appelant of wie zijn de appelanten, geef een omschrijving?
                2: Tegen welke tegenpartij hebben zij een geding?
                3: Over welke plaats gaat deze tekst?
                4: Over welke provincie gaat deze tekst?

                Antwoord uitsluitend in een Python list met de volgende opzet: 
                ["<omschrijving appelant(en)>", "<tegenpartij>", "<plaats>", "<provincie>"]
                
                Als het antwoord onbekend is, geef dan "onbekend" op bij het betreffende deel van de Python list.
                """
    answer = send_prompt(prompt)
    if answer:
        try:
            return json.loads(answer)
        except ValueError:
            return None


def get_letter_labels(text, labels):

    collected_letters = []

    for letter, label in labels.items():

        prompt = f"""
    ### Instructie        
    Je bent een expert in het lezen van juridische uitspraken. Lees de volgende uitspraak van de Raad van State:
    
    "{text}"
    
    Is het volgende van toepassing op deze uitspraak?
    
    {label}
    
    ### Output
    Antwoord met ja of nee.
    
    ### Belangrijk
    - Geef als antwoord uitsluitend ja of nee.
    - Geef geen toelichting bij het antwoord.
    - Herhaal de tekst niet in je antwoord.
        """

        print("Checking for label: ", label)
        answer = send_prompt(prompt)

        if answer.lower().strip() == "ja":
            print(f"Dit is van toepassing op deze uitspraak.")
            collected_letters.append(letter)

    return collected_letters


def get_appellant_type_labels(text, types):

    collected_types = []

    for t in types:

        prompt = f"""
    ### Instructie        
    Je bent een expert in het lezen van juridische uitspraken. Lees de tekst van de Raad van State:
    
    "{text}"
    
    Is de appellant of een van de appellanten van het volgende type?
    
    {t}
    
    ### Output
    Antwoord met ja of nee.
    
    ### Belangrijk
    - Geef als antwoord uitsluitend ja of nee.
    - Geef geen toelichting bij het antwoord.
    - Herhaal de tekst niet in je antwoord.
        """

        print("Checking for type: ", t)
        answer = send_prompt(prompt)

        if answer.lower().strip() == "ja":
            print(f"Dit is van toepassing op deze uitspraak.")
            collected_types.append(t)

    return collected_types
