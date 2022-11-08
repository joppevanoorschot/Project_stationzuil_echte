from datetime import datetime
import random


while True:
    naam = input("Voer naam in, laat leeg als u anoniem wilt blijven")
    if ";" in naam:
        print("uw naam mag geen: ';'bevatten")
        continue
    if naam == "":
        naam = 'anoniem'
        break
    else:
        break
# ik controleer op het gebruik van ; , want misschien wil ik later mijn data splitesen dan kan dato p een ;
while True:
# dit bericht wordt later wegeschreven, bij deze loop wordt gecontroleerd of die geldig is
    bericht = input("voer hier uw bericht in")
    if ";" in bericht:
        print("uw bericht mag geen: ';'bevatten")
        continue
    if len(bericht) < 141:
        break
    elif len(bericht) > 140:
        print("Uw bericht is te lang, zorg ervoor dat uw bericht korter is dan 140 tekens")

# ik controleer op het gebruik van ; , want misschien wil ik later mijn data splitesen dan kan dato p een ;

nu = datetime.now()
datum_bericht = nu.strftime("%Y-%m-%d")
tijd_bericht = nu.strftime("%H:%M:%S")


with open("stations") as f:
    lijst_stations = f.readlines()
    random_station = random.choice(lijst_stations)


with open("berichten","a") as f:
    f.write(f'{bericht};{datum_bericht};{tijd_bericht};{naam};{random_station}')