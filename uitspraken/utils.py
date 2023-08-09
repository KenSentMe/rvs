from rvs.openai.gpt import get_winner, get_place


def add_oordeel(uitspraak):
    if uitspraak.oordeel != 0:
        return
    index = uitspraak.inhoud.lower().find("\nbeslissing\n")
    if index != -1:
        response = get_winner(uitspraak.inhoud[index:])
    else:
        response = get_winner(uitspraak.inhoud)
    if response:
        uitspraak.oordeel = response[0]
        uitspraak.uitleg = response[1]
        uitspraak.save()
    else:
        return


def add_place(uitspraak):
    if uitspraak.inhoud and (uitspraak.plaats == ""):
        place = get_place(uitspraak.inhoud[:1000])
        uitspraak.plaats = place[0]
        uitspraak.provincie = place[1]
        uitspraak.save()

