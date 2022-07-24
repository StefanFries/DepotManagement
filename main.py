import os
import json
import csv, sys
# import ConfigParser
import depots
from pathlib import Path
from InvestmentTools import instruments
# from InvestmentTools import instr as instruments
from datetime import datetime

depot_800_os = {
  "depotname": "800-Prozent-Depot",
  "history": [
    {
      "timestamp": "26.06.2022",
      "items": [
        {
          "Basiswert": "Meta",
          "WKN": "JJ2HPH",
          "Anzahl": 1900,
          "Kaufkurs": "3,51 EUR",
          "Kaufdatum": "18.11.2021"
        },
        {
          "Basiswert": "Danaher",
          "WKN": "VQ9XQL",
          "Anzahl": 2800,
          "Kaufkurs": "2,40 EUR",
          "Kaufdatum": "18.11.2021"
        },
        {
          "Basiswert": "UnitedHealth",
          "WKN": "TT7Z3C",
          "Anzahl": 18000,
          "Kaufkurs": "0,44 EUR",
          "Kaufdatum": "21.04.2022"
        },
        {
          "Basiswert": "Palo Alto",
          "WKN": "JN6FUQ",
          "Anzahl": 14000,
          "Kaufkurs": "0,48 EUR",
          "Kaufdatum": "18.11.2021"
        },
        {
          "Basiswert": "McDonald’s",
          "WKN": "JA30E2",
          "Anzahl": 52000,
          "Kaufkurs": "1,49 EUR",
          "Kaufdatum": "21.04.2022"
        }
      ]
    }
  ]
}

with open("data/configs/config.json") as json_config_file:
    data = json.load(json_config_file)

json_string = json.dumps(depot_800_os, ensure_ascii = False, indent = 4)

filename = '800-Prozent-Depot.json'
with open(filename, 'w') as depot_file:
    depot_file.write(json_string)

header_prefix = ['Depotname', 'Zeitstempel']
header = header_prefix + list(depot_800_os['history'][0]['items'][0].keys())

filename = '800-Prozent-Depot.csv'
filepath = Path(filename)
print(filepath)
if not filepath.is_file():
    with open(filename, 'w', newline='') as depot_file:
        writer = csv.writer(depot_file)
        writer.writerow(header)

with open(filename, 'a', newline='') as depot_file:
    writer = csv.writer(depot_file)
    for entry in depot_800_os['history']:
        for item in entry['items']:
            row = [depot_800_os['depotname'], entry['timestamp']]
            for key in item.keys():
                row.append(str(item[key]))
            writer.writerow(row)

depotpath = os.path.join(os.path.dirname(__file__), 'data', 'depots')
print(depotpath)

# depot_800_os    = ['JJ2HPH', 'VQ9XQL', 'TT7Z3C', 'JN6FUQ', 'JA30E2']


# depot_list = [depots.depot_800_os]
# depot_list = [depots.depot_800_plus]
depot_list = [depots.depot_800_share]
# depot_list = [depots.test_indizes]
#depot_list = [depots.depot_zertifikat,\
#        depots.test_depot,\
#        depots.test_indizes,\
#        depots.test_anleihen,\
#        depots.test_etfs,\
#        depots.test_edelmetall,\
#        depots.test_currencies,\
#        depots.depot_800_share,\
#        depots.depot_800_os,\
#        depots.depot_800_plus,\
#        depots.depot_usa,\
#        depots.depot_tsi,\
#        depots.depot_premium]

Crawler = instruments.InstrumentCrawler()
# Crawler = instruments.RawDataCrawler()
# Crawler = instruments.BaseAttributesCrawler()

start = datetime.now()
counter = 0

for depot in depot_list:
    for wkn in depot:
        counter = counter + 1
        c = Crawler.crawl_base_data(wkn)
        print()
        print()
        print("Typ        : " + c.get_instrument_type())
        print("Name       : " + c.get_name())
        print("WKN        : " + c.get_identifier()['WKN'])
        print("ISIN       : " + c.get_identifier()['ISIN'])
        print("Symbol     : " + c.get_identifier()['Symbol'])
        print("ID_Notations         : " + str(c.get_id_notations()))
        print("Live Trading Plätze  : " + str(c.get_live_trading_venues()))
        print("Börsen Handelsplätze : " + str(c.get_exch_trading_venues()))
        print("Stammdaten-Attribute : " + str(c.get_master_data()))
        print()
        print()

stop = datetime.now()
elapsed = stop - start

print("Elapsed time: ", elapsed, " für ", counter, " Instrumente")
