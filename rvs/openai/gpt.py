import openai
import traceback
import json

import rvs.openai.key as key

openai.api_key = key.openai_key


def send_prompt(prompt):

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
            n=1,
        )
        answer = (
            response.choices[0]["message"]["content"].strip().strip('"').strip("!")
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


def get_winner(text):

    prompt = f"""Lees deze uitspraak van de Raad van State:

            "{text}"
            
            Welke van de volgende opties geldt voor deze uitspraak? Kies 1 antwoord.
            
            1. het beroep wordt gegrond verklaard. Het bestreden besluit wordt geheel of gedeeltelijk vernietigd
            2. het beroep wordt niet-ontvankelijk verklaard.
            3. De bestuursrechter kan bepalen dat:
                a. de rechtsgevolgen van het vernietigde besluit of het vernietigde gedeelte daarvan geheel of gedeeltelijk in stand blijven, of
                b. zijn uitspraak in de plaats treedt van het vernietigde besluit of het vernietigde gedeelte daarvan.
            4. De bestuursrechter kan het bestuursorgaan opdragen een nieuw besluit te nemen of een andere handeling te verrichten met inachtneming van zijn aanwijzingen.
            5. De bestuursrechter kan zo nodig een voorlopige voorziening treffen. Daarbij bepaalt hij het tijdstip waarop de voorlopige voorziening vervalt.
            6. De bestuursrechter kan bepalen dat, indien of zolang het bestuursorgaan niet voldoet aan een uitspraak, het bestuursorgaan aan een door hem aangewezen partij een in de uitspraak vast te stellen dwangsom verbeurt.
            7. De bestuursrechter verklaart zich onbevoegd om uitspraak te doen.
            8. Anders
            
            Antwoord uitsluitend in een Python list met de volgende opzet: [<cijfer antwoord>, <text antwoord>] 
            """

    answer = send_prompt(prompt)
    if answer:
        return json.loads(answer)

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
                3: Over welke plaats en provincie gaat deze tekst?

                Antwoord uitsluitend in een Python list met de volgende opzet: 
                ["<omschrijving appelant(en)>", "<tegenpartij>", "<plaats>", "<provincie>"]
                
                Als het antwoord onbekend is, geef dan "onbekend" op bij het betreffende deel van de Python list.
                """
    answer = send_prompt(prompt)
    if answer:
        return json.loads(answer)

    return None
