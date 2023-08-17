import openai
import traceback
import json
import os

if os.environ.get("OPENAI_KEY"):
    openai.api_key = os.environ.get("OPENAI_KEY")
else:
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
            
            1. het beroep wordt niet-ontvankelijk verklaard.
            2. de Raad van State bevestigt de aangevallen uitspraak
            3. het beroep wordt gegrond verklaard. Het bestreden besluit wordt geheel vernietigd.
            4. het beroep wordt gegrond verklaard. Het bestreden besluit wordt gedeeltelijk vernietigd. 
                Dat betekent dat het beroep voor een deel gegrond wordt verklaard en voor een deel ongegrond
            9. Anders
            
            Antwoord uitsluitend in een Python list met de volgende opzet: [<cijfer antwoord>, <text antwoord>] 
            """
    try:
        answer = send_prompt(prompt)
    except openai.error.InvalidRequestError:
        return None

    if answer:
        try:
            return json.loads(answer)
        except ValueError:
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
