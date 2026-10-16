"""Task 5: the original forward/backtracking search with explicit inputs."""
import argparse
from input_data import read_text

def parse_input(text):
    values = list(map(int, text.split()))
    if not values or values[0] < 1 or len(values) != values[0] + 1:
        raise ValueError('Expected a positive section count and that many periods.')
    if any((period <= 0 for period in values[1:])):
        raise ValueError('Section periods must be positive integers.')
    return values[1:]

def pruefeQuader(aktuelleZeit, aktuellerIndex, periods):
    quaderWert = aktuelleZeit // periods[aktuellerIndex]
    return quaderWert % 2 == 1

def pruefeFortschritt(aktuelleZeit, aktuellerIndex, periods):
    naechsterQuaderWert1 = (aktuelleZeit // periods[aktuellerIndex - 1] + 1) * periods[aktuellerIndex - 1]
    naechsterQuaderWert2 = (aktuelleZeit // periods[aktuellerIndex] + 1) * periods[aktuellerIndex]
    return naechsterQuaderWert1 > naechsterQuaderWert2

def rueckwaertsPropagatione(schrittListe, aktuellerIndex, periods):
    if aktuellerIndex == 0:
        return False
    naechsterQuaderWert1 = (schrittListe[aktuellerIndex - 1] // periods[aktuellerIndex - 1] + 2) * periods[aktuellerIndex - 1]
    naechsterQuaderWert2 = (schrittListe[aktuellerIndex - 2] // periods[aktuellerIndex - 2] + 1) * periods[aktuellerIndex - 2]
    return naechsterQuaderWert1 >= naechsterQuaderWert2

def rueckwaertsPropagatioSchleife(schrittListe, aktuellerIndex, periods):
    tempSchrittListe = schrittListe.copy()
    while True:
        if not rueckwaertsPropagatione(schrittListe, aktuellerIndex, periods):
            if not schrittListe:
                schrittListe.append((tempSchrittListe[aktuellerIndex] // periods[aktuellerIndex] + 2) * periods[aktuellerIndex])
                aktuellerIndex += 1
            else:
                quaderWert = (schrittListe[aktuellerIndex - 1] // periods[aktuellerIndex - 1] + 2) * periods[aktuellerIndex - 1]
                schrittListe.pop()
                schrittListe.append(quaderWert)
            return (schrittListe, aktuellerIndex)
        else:
            aktuellerIndex -= 1
            schrittListe.pop()

def erstelleAnweisungen(zeitmarken):
    anweisungen = []
    anweisungen.append(f'Warte {zeitmarken[0]} Minuten')
    anweisungen.append(f'laufe in den Abschnitt 1')
    for i in range(1, len(zeitmarken)):
        warteMinuten = zeitmarken[i] - zeitmarken[i - 1]
        anweisungen.append(f'Warte {warteMinuten} Minuten')
        if i < len(zeitmarken) - 1:
            anweisungen.append(f'laufe in den Abschnitt {i + 1}')
        else:
            anweisungen.append('laufe zum Grabmal')
    ergebnisListe = []
    index = 0
    while index < len(anweisungen):
        if anweisungen[index] == 'Warte 0 Minuten':
            if ergebnisListe:
                ergebnisListe.pop()
        else:
            ergebnisListe.append(anweisungen[index])
        index += 1
    anweisungen = ergebnisListe
    return ', '.join(anweisungen)

def find_path(periods: list[int], max_steps: int=1000000) -> list[int]:
    """Run the original search; a work limit is not a claim of impossibility."""
    if not periods or any((p <= 0 for p in periods)) or max_steps < 1:
        raise ValueError('Provide positive periods and a positive search work limit.')
    if len(periods) == 1:
        return [periods[0]]
    aktuellerIndex = 1
    aktuelleZeit = periods[aktuellerIndex - 1]
    schrittListe = [aktuelleZeit]
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            raise ValueError('Search work limit reached; increase --max-steps. This does not prove no path exists.')
        if pruefeQuader(aktuelleZeit, aktuellerIndex, periods):
            aktuellerIndex += 1
            schrittListe.append(aktuelleZeit)
        elif pruefeFortschritt(aktuelleZeit, aktuellerIndex, periods):
            aktuelleZeit = (aktuelleZeit // periods[aktuellerIndex] + 1) * periods[aktuellerIndex]
            aktuellerIndex += 1
            schrittListe.append(aktuelleZeit)
        else:
            schrittListe, aktuellerIndex = rueckwaertsPropagatioSchleife(schrittListe, aktuellerIndex, periods)
            aktuelleZeit = schrittListe[-1]
        if aktuellerIndex == len(periods):
            return schrittListe

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Input file path or explicit HTTP(S) URL')
    parser.add_argument('--max-steps', type=int, default=1000000, help='Maximum search iterations (default: 1000000)')
    args = parser.parse_args()
    try:
        entries = find_path(parse_input(read_text(args.input)), args.max_steps)
        print('Section entry times: ' + ', '.join(map(str, entries)))
        print(f'Arrival time: {entries[-1]} minutes')
        print(erstelleAnweisungen(entries) if len(entries) > 1 else f'Warte {entries[0]} Minuten, laufe zum Grabmal')
    except (OSError, ValueError) as error:
        parser.exit(2, f'Error: {error}\n')
if __name__ == '__main__':
    main()
