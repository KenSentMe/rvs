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


def split_parties(uitspraak):
    text = uitspraak.inhoud
    gedingteksten = [
        "in het geding tussen:\n",
        "in de gedingen tussen:\n",
        "in het geding tussen onder meer:\n",
        "in de gedingen tussen onder meer:\n",
        "in het geding tussen[",
    ]
    procesverloopteksten = [
        "\nProcesverloop",
        ".Procesverloop",
    ]
    appellant = ""
    verweerder = ""
    for g in gedingteksten:
        if g in text:
            try:
                appellant = text.split(f"{g}")[1].split("\nen")[0][:200]
            except IndexError:
                continue
            for p in procesverloopteksten:
                if p in text:
                    try:
                        verweerder = text.split(f"{g}")[1].split("\nen\n")[1].split(p)[0][:200]
                    except IndexError:
                        continue

    if appellant and verweerder:
        uitspraak.appellant = appellant
        uitspraak.counterpart = verweerder
        uitspraak.save()
        return 1
    else:
        return 0
