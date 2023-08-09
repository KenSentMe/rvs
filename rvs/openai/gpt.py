import openai
import traceback

import rvs.openai.key as key

openai.api_key = key.openai_key


def send_prompt(prompt):

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
        return 1


def get_place(text):

    prompt = f"""Over welke plaats gaat de volgende text:
    
                "{text}"
                
                Als antwoord wil ik de plaats en de provincie waarin de plaats ligt in de vorm van 
                een Python list.
                Antwoord:
                """
    answer = send_prompt(prompt)
    return answer


def get_winner(text):

    prompt = f"""Wie krijgt van de Raad van State gelijk in deze zaak:

            "{text}"
            
            Ik wil dat je een persoon of organisatie aanwijst als winnaar.
            Winnaar:
            """

    answer = send_prompt(prompt)
    return answer
