import requests
URL_AUFGABE = "https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/1_runde/grabmal0.txt"
GRABMAL_DATA = requests.get(URL_AUFGABE).text
GRABMAL_DATA_GETRENNT = GRABMAL_DATA.splitlines()
GRABMAL_DATA_LIST = values = list(map(int, GRABMAL_DATA_GETRENNT))
ANZAHL_QUADER = GRABMAL_DATA_LIST[0]
QUADER_FREQUENZ = GRABMAL_DATA_LIST[1:]

def pruefeQuader(aktuelleZeit, aktuellerIndex):
   quaderWert = aktuelleZeit//QUADER_FREQUENZ[aktuellerIndex]
   if quaderWert % 2 == 0:
       return False
   else:
       return True

def pruefeFortschritt(aktuelleZeit, aktuellerIndex):
   naechsterQuaderWert1 = (aktuelleZeit//QUADER_FREQUENZ[aktuellerIndex-1]+1)*QUADER_FREQUENZ[aktuellerIndex-1]
   naechsterQuaderWert2 = (aktuelleZeit//QUADER_FREQUENZ[aktuellerIndex]+1)*QUADER_FREQUENZ[aktuellerIndex]
   if naechsterQuaderWert1 > naechsterQuaderWert2:
       return True
   else:
       return False

def rueckwaertsPropagatione(schrittListe, aktuellerIndex):
   if aktuellerIndex == 0:
       return False
   
   naechsterQuaderWert1 = (schrittListe[aktuellerIndex-1]//QUADER_FREQUENZ[aktuellerIndex-1]+2)*QUADER_FREQUENZ[aktuellerIndex-1]
   naechsterQuaderWert2 = (schrittListe[aktuellerIndex-2]//QUADER_FREQUENZ[aktuellerIndex-2]+1)*QUADER_FREQUENZ[aktuellerIndex-2]
   if naechsterQuaderWert1 < naechsterQuaderWert2:
       return False
   else:
       return True

def rueckwaertsPropagatioSchleife(schrittListe, aktuellerIndex):
   tempSchrittListe = schrittListe.copy()
   while True:
       if rueckwaertsPropagatione(schrittListe, aktuellerIndex) == False:
           if len(schrittListe) == 0:
               schrittListe.append((tempSchrittListe[aktuellerIndex]//QUADER_FREQUENZ[aktuellerIndex]+2)*QUADER_FREQUENZ[aktuellerIndex])
               aktuellerIndex += 1
           else:
               quaderWert = (schrittListe[aktuellerIndex-1]//QUADER_FREQUENZ[aktuellerIndex-1]+2)*QUADER_FREQUENZ[aktuellerIndex-1]
               schrittListe.pop()
               schrittListe.append(quaderWert)
           return schrittListe, aktuellerIndex
       else:
           aktuellerIndex -= 1
           schrittListe.pop()

def erstelleAnweisungen(zeitmarken):
   anweisungen = []
   anweisungen.append(f"Warte {zeitmarken[0]} Minuten")
   anweisungen.append(f"laufe in den Abschnitt 1")
   for i in range(1, len(zeitmarken)):
       warteMinuten = zeitmarken[i] - zeitmarken[i - 1]
       anweisungen.append(f"Warte {warteMinuten} Minuten")
       if i < len(zeitmarken) - 1:
           anweisungen.append(f"laufe in den Abschnitt {i + 1}")
       else:
           anweisungen.append("laufe zum Grabmal")
   
   ergebnisListe = []
   index = 0

   while index < len(anweisungen):
       if anweisungen[index] == "Warte 0 Minuten":
           if ergebnisListe:
               ergebnisListe.pop()
       else:
           ergebnisListe.append(anweisungen[index])
       index += 1
   anweisungen = ergebnisListe
   return ', '.join(anweisungen)

def rekursiveAlgorithmus():
  aktuellerIndex = 1
  aktuelleZeit = QUADER_FREQUENZ[aktuellerIndex-1]
  schrittListe = [aktuelleZeit]
  while True:
      if pruefeQuader(aktuelleZeit, aktuellerIndex):
          aktuellerIndex += 1
          schrittListe.append(aktuelleZeit)
      elif pruefeFortschritt(aktuelleZeit, aktuellerIndex):
          aktuelleZeit = (aktuelleZeit//QUADER_FREQUENZ[aktuellerIndex]+1)*QUADER_FREQUENZ[aktuellerIndex]
          aktuellerIndex += 1
          schrittListe.append(aktuelleZeit)
      else:
          schrittListe, aktuellerIndex = rueckwaertsPropagatioSchleife(schrittListe, aktuellerIndex)
          aktuelleZeit = schrittListe[-1]
      if aktuellerIndex == ANZAHL_QUADER:
          print(schrittListe)
          anweisungen = erstelleAnweisungen(schrittListe)
          print(anweisungen)
          break

rekursiveAlgorithmus()
