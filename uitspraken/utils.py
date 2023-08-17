from rvs.openai.gpt import get_winner, get_place, get_metadata


def add_oordeel(uitspraak):
    if uitspraak.oordeel != 0:
        return
    if "\nconclusie\n" in uitspraak.inhoud.lower():
        index = uitspraak.inhoud.lower().find("\nconclusie\n")
    else:
        index = uitspraak.inhoud.lower().find("\nbeslissing\n")
    if index != -1:
        beslissing = uitspraak.inhoud[index:]
    else:
        beslissing = uitspraak.inhoud

    beslissing_kort = beslissing.lower().split("\nbijlage")[0]

    response = get_winner(beslissing_kort[:10000])

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


def add_metadata(uitspraak):
    if uitspraak.inhoud and not uitspraak.appellant:
        metadata = get_metadata(uitspraak.inhoud[:1000])
        if len(metadata) == 4:
            uitspraak.appellant = metadata[0]
            uitspraak.counterpart = metadata[1]
            uitspraak.plaats = metadata[2]
            uitspraak.provincie = metadata[3]
            uitspraak.save()
    else:
        return
