import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

url = 'https://www.atletiek.nu/wedstrijden/#{%22c%22:%22NL%22,%22s%22:%22Athletic%20champs%22,%22e%22:[%22in%22,%22out%22],%22pdst%22:2,%22r%22:[],%22cat%22:[],%22events%22:[],%22sd%22:1704060000,%22ed%22:1726955999}'

driver = webdriver.Chrome()
driver.get(url)

time.sleep(5)  # Wacht een paar seconden zodat de pagina volledig laadt

soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', class_='table calendarTable')

events = []

if table:
    # Zoek alle rijen in de tabel (behalve de header)
    rows = table.find_all('tr')

    # Loop door elke rij en zoek de eventnaam
    for row in rows:
        # Zoek de cel met de class 'eventnaam'
        event_td = row.find('td', class_='eventnaam')
        if event_td:
            # Zoek de <span> met de class 'hidden-xs' binnen de td
            event_span = event_td.find('span', class_='hidden-xs')
            event_spanExtra = event_td.find('span', class_='aantaldeelnemers')
           
           
            eventnaam = event_span.get_text(strip=True) if event_span else "Geen naam"
            deelnemers = event_spanExtra.get_text(strip=True) if event_spanExtra else "Geen deelnemers"

           
         #   if event_span:
        #        eventnaam = event_span.get_text(strip=True)
         #       print("Eventnaam:", eventnaam)
          #  if event_spanExtra:
           #     deelnemers = event_spanExtra.get_text(strip=True)
            #    print("Deelnemers:", deelnemers)

            events.append({
                'Eventnaam': eventnaam,
                'Aantal Deelnemers': deelnemers
            })


df = pd.DataFrame(events)

# Schrijf de DataFrame naar een CSV-bestand
df.to_csv('events.csv', index=False, encoding='utf-8')

print("Data succesvol naar events.csv geschreven.")

#print(soup)

#table = soup.find('table', class_ = 'table calendarTable')
#print(table)




