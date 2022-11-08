# import van een extra module
# tip: deze moet je wel eerst installeren met pip install psycopg2
# tip: op een mac met een m1 chip: check met je docent
import psycopg2
from datetime import datetime

# Press the green button in the gutter to run the script.
if __name__ == '__main__':  # start van python script
    print('Start de connectie met de postgress databse')

# maak de connectie met de database
conn = psycopg2.connect(
    host="localhost",
    database="project_stations_zuil",  # database naam
    user="postgres",  # user naam
    password="3555")  # wachtwoord van de user

# maak een cursor
cursor1 = conn.cursor()
# execute a statement
# print('Check of het werk door de PostgreSQL database version op te vragen:')
cursor1.execute('SELECT version()')
db_version = cursor1.fetchone()
# print(' db version:' + db_version[0])

# maal een nieuwe cursor aan
cursor = conn.cursor()

# maak de sql query aan die je naar de database wilt sturen
sql_query1 = 'select * from gebruikers_bericht'  # van de klant tabel


naam_moderator = input("voer hier de naam van de moderator in")
email_moderator = input("voer hier het email adres van de moderator in")
# HEB DEZE 2 BUITEN DE LOOP STAAN ZODAT HET NIET ELKE KEER OPNIEUW WORDT GEVRAAGD
with open("berichten", 'r+') as f:
    lijst_met_berichten = f.readlines()

while True:

    oudste_bericht = lijst_met_berichten[0].replace("\n", "")
    gekeurd = input("vul 'goedgekeurd' in als het bericht is goedgekeurd, of vul 'afgekeurd' in als het bericht is afgekeurd")
    if gekeurd == "goedgekeurd":
        tijd_nu = datetime.now()
        tijd_beoordeling = tijd_nu.strftime("%H:%M:%S")
        datum_beoordeling = tijd_nu.strftime("%Y-%m-%d")
        gekeurd = '1'
        bericht_met_alles = f'{oudste_bericht};{gekeurd};{tijd_beoordeling};{naam_moderator};{email_moderator};{datum_beoordeling}'
        bericht_met_alles_gesplit = bericht_met_alles.split(';')
# met deze query stop ik de hierbovengeschreven data in de database.
        cursor.execute("INSERT INTO public.gebruikers_bericht(bericht, datum_bericht, tijd_bericht,"
                           " naam_reiziger, station, goed_of_afgekeurd, tijd_beoordeling,"
                           " naam_moderator, email_moderator, datum_beoordeling) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           bericht_met_alles_gesplit)
        conn.commit()
        lijst_met_berichten.remove(lijst_met_berichten[0])
        if len(lijst_met_berichten) != 0:
            continue
        else:
            open("berichten", 'w').close()

            break
        break
    if gekeurd == "afgekeurd":
        tijd_nu = datetime.now()
        tijd_beoordeling = tijd_nu.strftime("%H:%M:%S")
        datum_beoordeling = tijd_nu.strftime("%Y-%m-%d")
        gekeurd = '0'
# dit is hetzelfde als bij de vorige, maar hier wordt gekeurd: '0' ipv '1'
        bericht_met_alles = f'{oudste_bericht};{gekeurd};{tijd_beoordeling};{naam_moderator};{email_moderator};{datum_beoordeling}'
        bericht_met_alles_gesplit = bericht_met_alles.split(';')
        cursor.execute("INSERT INTO public.gebruikers_bericht(bericht, datum_bericht, tijd_bericht,"
                       " naam_reiziger, station, goed_of_afgekeurd, tijd_beoordeling,"
                       " naam_moderator, email_moderator, datum_beoordeling) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       bericht_met_alles_gesplit)
        conn.commit()
        lijst_met_berichten.remove(lijst_met_berichten[0])
        if len(lijst_met_berichten) != 0:
            continue
        else:
            open("berichten", 'w').close()
            break

    else:
        print("voer alleen 'goedgekeurd' of 'afgekeurd' in.")
        continue


cursor.close()