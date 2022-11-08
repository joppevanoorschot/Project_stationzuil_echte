import psycopg2
import tkinter as tk
import requests

conn = psycopg2.connect(
    host="localhost",
    database="project_stations_zuil",  # database naam
    user="postgres",  # user naam
    password="3555")  # wachtwoord van de user

cursor1 = conn.cursor()

# de query selecteert de benodigde tabellen, om te controleren of de berichten zijn goedgekeurd (bij de where = 1).
# en dan de 5 laatste berichten

cursor1.execute('select station_city, ov_bike, elevator, toilet, park_and_ride, bericht, station '
                'from gebruikers_bericht inner join station_service '
                'on gebruikers_bericht.station = station_service.station_city '
                'where goed_of_afgekeurd = 1 '
                'order by bericht_nummer desc limit 5;')

#  ov_fiets , lift, toilet, park and ride

mijn_lijst = cursor1.fetchall()
lege_lijst2 = []
x = 0

# ik wil van de data overal waar True staat, vervangen met de desbetrefende voorziening. dat doe ik door
# eerst een lege lijst te maken om vervolgens door de "mijn_lijst" heen te loopen en daar overal te controleren of het
# True is . als het True is voeg ik het toe aan een nieuwe lijst met de juiste voorzieningen.
# om door elke te loopen doe ik x = x+1

lijst_met_lijsten = []
for u in mijn_lijst:
    lege_lijst2.append(u[:-2])
    lijst_metinformatie1 = []
    lijst_metinformatie1.append(lege_lijst2[x][0])
    if lege_lijst2[x][1] == True:

        lijst_metinformatie1.append("OV Fiets")

    if lege_lijst2[x][2] == True:
        lijst_metinformatie1.append("Lift")

    if lege_lijst2[x][3] == True:
        lijst_metinformatie1.append("Toilet")

    if lege_lijst2[x][4] == True:
        lijst_metinformatie1.append("park and ride")
    lijst_met_lijsten.append(lijst_metinformatie1)

    x = x+1





# deze loop is om specifiek alleen de berichten te isoleren.
lege_lijst = []
for i in mijn_lijst:
    lege_lijst.append(i[5])




cursor1.close()

huidige_station = "Utrecht"


# om het weer op te vragen heb ik de locatie nodig.
# om de locatie te krijgen vraag ik de latitude en de longtitude op van een stad(waar het station ligt).
# aan het einde krijg ik het weer in kelvin. vandaar dat ik er nog 273.15 vanaf haal zodat het in graden celcius is.

def krijg_weer(station):
    locatie = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?"
                           f"q={station},NL&appid=969b2894989ecb5a84023a30af2f4a7b")
    locatie_json = locatie.json()
    lat = locatie_json[0]["lat"]
    lon = locatie_json[0]["lon"]
    weer = requests.get(f"https://api.openweathermap.org/data/2.5/weather?"
                     f"lat={lat}&lon={lon}&exclude=%7Bpart%7D&appid=969b2894989ecb5a84023a30af2f4a7b")
    weer_json = weer.json()
    return round(weer_json["main"]["temp"]-273.15, 1)


window = tk.Tk()

window.geometry("1400x700")
window.title("Stationshalscherm")

# dit zijn de labels voor de stationrows

column_aantal = 5
window.rowconfigure(0, weight=1)
label1 = tk.Label(window, text="Station")
label2 = tk.Label(window, text="Voorziening 1")
label3 = tk.Label(window, text="Voorziening 2")
label4 = tk.Label(window, text="Voorziening 3")
label5 = tk.Label(window, text="Voorziening 4")
label6 = tk.Label(window, text="Bericht")
label7 = tk.Label(window, text="Weer")
label1.grid(column=0, row=0)
label2.grid(column=1, row=0)
label3.grid(column=2, row=0)
label4.grid(column=3, row=0)
label5.grid(column=4, row=0)
label6.grid(column=5, row=0)
label7.grid(column=6, row=0)
labeltemp = tk.Label(window, text=krijg_weer(huidige_station))
labeltempstad = tk.Label(window, text=huidige_station)
labeltemp.grid(column=6, row=2)
labeltempstad.grid(column=6, row=1)


# met deze for-loop bepaal ik hoe breedt de colums moetten zijn en hoeveel columns ik moet hebben
# die laatste heeft een weight 3, omdat die tekst langer kan zijn.


for col in range(column_aantal):
    window.columnconfigure(col, weight=1)
window.columnconfigure(column_aantal, weight=1)
# hiermee vul ik mn stationnamen in de tinker. die i+1 is om te zorgen dat het telkens op een nieuwe row komt.
for i in range(len(lijst_met_lijsten)):
    window.rowconfigure(i+1, weight=1)
    lijst = lijst_met_lijsten[i]
    station = lijst[0]
    station_label = tk.Label(window, text=station)
    station_label.grid(column=0 ,row=i+1)
# met deze for loop vul ik in welke voorzieneingen er zijn.
    for j in range(1, len(lijst)):
        voorziening = lijst[j]
        voorziening_label = tk.Label(window, text=voorziening)
        voorziening_label.grid(column=j, row=i+1)
        pass
# hier vul ik de berichten in
    bericht = lege_lijst[i]
    bericht_label = tk.Label(window, text=bericht)
    bericht_label.grid(column=column_aantal, row=i+1)




window.mainloop()
