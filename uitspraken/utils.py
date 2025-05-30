from rvs.openai.gpt import get_place, get_metadata, get_clear_verdict, get_verdict, get_letter_labels, get_appellant_type_label, get_plaats_label
from uitspraken.models import Letter, AppellantType
import re


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
        if metadata and len(metadata) == 4:
            print(f"found metadata for {uitspraak.id}")
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

    try:
        beslissing = uitspraak.inhoud.split("\nDe voorzieningenrechter van de Afdeling bestuursrechtspraak van de Raad van State:\n")[1].split("\nAldus vastgesteld door")[0]
    except IndexError:
        pass

    try:
        beslissing = re.split(r'(?<=\.Beslissing)(?=\S)', uitspraak.inhoud)[1].split(".Aldus vastgesteld door")[0]
    except IndexError:
        pass

    try:
        beslissing = uitspraak.inhoud.split("\nDe Afdeling bestuursrechtspraak van de Raad van State\n")[1].split("\nAldus vastgesteld door")[0]
    except IndexError:
        pass

    try:
        beslissing = uitspraak.inhoud.split(
            "\nDe voorzieningenrechter:\n")[1].split(
            "\nAldus vastgesteld door")[0]
    except IndexError:
        pass

    if beslissing:
        uitspraak.beslissing = beslissing
        uitspraak.save()
        return 1
    else:
        return 0


def get_first_verdict(uitspraak):
    if uitspraak.beslissing and not uitspraak.oordeel:
        oordeel = get_clear_verdict(uitspraak.beslissing[:10000])
        if oordeel == 1:
            uitspraak.oordeel = oordeel
            uitspraak.save()
            return 1
    return 0


def get_final_verdict(uitspraak):
    print(f"Checking {uitspraak.id}")

    beslissing = ""

    if uitspraak.beslissing:
        beslissing = uitspraak.beslissing
    else:
        beslissing = uitspraak.inhoud

    if beslissing and (not uitspraak.oordeel or uitspraak.oordeel == 0):
        print(f"Getting final verdict for {uitspraak.id}")
        oordeel = get_verdict(uitspraak.beslissing[:10000])
        print(f"GOT {oordeel} for {uitspraak.id}")
        if oordeel:
            uitspraak.oordeel = oordeel
            uitspraak.save()
            return 1
    else:
        print(f"Already has verdict for {uitspraak.id}")
    return 0


def get_letter(uitspraak):
    if uitspraak.beslissing and not uitspraak.letters.all():
        available_letters = Letter.objects.all()
        letter_dict = {}
        for letter in available_letters:
            letter_dict[letter.letter] = letter.description
        collected_letters = get_letter_labels(uitspraak.beslissing[:10000], letter_dict)
        if collected_letters:
            for letter in collected_letters:
                uitspraak.letters.add(Letter.objects.get(letter=letter))
            uitspraak.save()
            return 1
    return 0


def get_appellant_type(uitspraak):
    uitspraak.beslissing and (uitspraak.appellant_type is None or uitspraak.appellant_type == "UNK")
    available_types = AppellantType.objects.all()

    appellant_type = get_appellant_type_label(uitspraak.inhoud[:1000])

    if appellant_type:
        uitspraak.appellant_type = appellant_type
        uitspraak.save()
        return 1
    return 0


def get_plaats(uitspraak):
    if uitspraak.beslissing and not uitspraak.plaats:
        plaats = get_plaats_label(uitspraak.inhoud[:1000])
        if plaats:
            uitspraak.plaats = plaats
            uitspraak.save()
            return 1
    return 0