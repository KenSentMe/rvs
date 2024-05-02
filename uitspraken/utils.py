from rvs.openai.gpt import get_place, get_metadata, get_clear_verdict, get_verdict


def add_oordeel(uitspraak):

    response = get_winner(uitspraak.beslissing[:10000])

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


def get_beslissing(uitspraak):
    beslissing = ""
    try:
        beslissing = uitspraak.inhoud.split("\nDe Afdeling bestuursrechtspraak van de Raad van State:\n")[1].split("\nAldus vastgesteld door")[0]
    except IndexError:
        pass

    if beslissing:
        uitspraak.beslissing = beslissing
        uitspraak.save()
        return 1
    else:
        return 0


def get_first_verdict(uitspraak):
    if uitspraak.beslissing:
        oordeel = get_clear_verdict(uitspraak.beslissing[:10000])
        if oordeel:
            uitspraak.oordeel = oordeel
            uitspraak.save()
            return 1
        else:
            return 0


def get_final_verdict(uitspraak):
    if uitspraak.beslissing:
        oordeel = get_verdict(uitspraak.beslissing[:10000])
        if oordeel:
            uitspraak.oordeel = oordeel
            uitspraak.save()
            return 1
        else:
            return 0
