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
            model="gpt-4-turbo",
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
### Instructie        
Je bent een expert in het lezen van juridische uitspraken. Lees de volgende uitspraak van de Raad van State:

"{text}"

Er zijn 9 opties:

1. Het beroep wordt ongegrond verklaard en/of de uitspraak wordt bevestigd. Er worden verder **geen** voorwaarden gesteld, zoals het betalen van proceskosten.
2. De aangevallen uitspraak wordt bevestigd. Maar de wederpartij wordt veroordeeld om proceskosten te voldoen.
3. het beroep wordt gegrond verklaard en het bestreden besluit wordt geheel vernietigd
4. het beroep wordt niet-ontvankelijk verklaard.
5. De bestuursrechter kan bepalen dat de rechtsgevolgen van het vernietigde besluit of het vernietigde gedeelte daarvan geheel of gedeeltelijk in stand blijven
6. De bestuursrechter kan zo nodig een voorlopige voorziening treffen. Daarbij bepaalt hij het tijdstip waarop de voorlopige voorziening vervalt.
7. De bestuursrechter kan bepalen dat, indien of zolang het bestuursorgaan niet voldoet aan een uitspraak, het bestuursorgaan aan een door hem aangewezen partij een in de uitspraak vast te stellen dwangsom verbeurt.
8. De bestuursrechter verklaart zich onbevoegd om uitspraak te doen.
9. Anders

### Output
Geef het nummer van de optie die volgens jou van toepassing is.

### Voorbeelden

- **Input: ** "I. bevestigt de uitspraak van de rechtbank;
II. verklaart het beroep van [partij] tegen het besluit van 10 mei 2021, kenmerk 153300, ongegrond;
III. veroordeelt het college van burgemeester en wethouders van Berkelland tot vergoeding van bij [partij] in verband met de behandeling van het hoger beroep van het college opgekomen proceskosten tot een bedrag van € 759,00, geheel toe te rekenen aan door een derde beroepsmatig verleende rechtsbijstand;
IV. bepaalt dat van het college van burgemeester en wethouders van Berkelland een griffierecht van € 541,00 wordt geheven."
**Output:** 2
- **Input: ** "I. verklaart het hoger beroep gegrond;
II. vernietigt de uitspraak van de rechtbank Den Haag van 26 maart 2021 in zaak nr. 19/3218;
III. verklaart het bij de rechtbank ingestelde beroep gegrond;
IV. vernietigt het besluit van het college van burgemeester en wethouders van Oegstgeest van 9 april 2019 met kenmerk Z/18/113961/244117;
V. draagt het college van burgemeester en wethouders van Oegstgeest op om binnen 26 weken na de verzending van deze uitspraak met inachtneming van wat daarin is overwogen een nieuw besluit op bezwaar te nemen;
VI. bepaalt dat tegen het nieuw te nemen besluit op bezwaar slechts bij de Afdeling bestuursrechtspraak van de Raad van State beroep kan worden ingesteld;
VII. gelast dat het college van burgemeester en wethouders van Oegstgeest aan Stichting Dorpscentrum Oegstgeest en andere het door hen voor de behandeling van het beroep en het hoger beroep betaalde griffierecht ten bedrage van € 717,00 vergoedt, met dien verstande dat bij betaling van genoemd bedrag aan een van hen het college aan zijn betalingsverplichting heeft voldaan."
**Output:** 3

### Belangrijk
- Geef het antwoord uitsluitend in de vorm van een enkel cijfer van 1 tot en met 9.
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
