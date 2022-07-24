
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

standard_types = ['Aktie', 'Anleihe', 'ETF', 'Fonds', 'Optionsschein', 'Zertifikat'] # Test für Fonds und Zertifikate offen
special_types  = ['Edelmetall', 'Index', 'Währung']
instrument_types = standard_types + special_types

base_url = 'https://www.comdirect.de/inf/search/all.html?'

class Instrument():
    def __init__(self, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues, master_data):
        self.__identifier = identifier
        self.__name = name
        self.__instrument_type = instrument_type
        self.__id_notations = id_notations
        self.__live_trading_venues = live_trading_venues
        self.__exch_trading_venues = exch_trading_venues
        self.__master_data = master_data

    def get_identifier(self):
        return self.__identifier

    def get_name(self):
        return self.__name

    def get_instrument_type(self):
        return self.__instrument_type

    def get_id_notations(self):
        return self.__id_notations

    def get_live_trading_venues(self):
        return self.__live_trading_venues

    def get_exch_trading_venues(self):
        return self.__exch_trading_venues

    def get_master_data(self):
        return self.__master_data

class Aktie(Instrument):
    instrument_type = 'Aktie'
    # liefert Fehler, wenn zusätzliche Zeile "Comdirect Sparplan" angezeigt wird
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Aktieninformationen')).parent.parent.select('table tr')
        master_data = {}
        master_data['Wertpapiertyp'] = master_data_rows[0].select('td')[1].text
        master_data['Marktsegment'] = master_data_rows[1].select('td')[1].text
        master_data['Branche'] = master_data_rows[2].select('td')[1].text
        master_data['Geschäftsjahr'] = master_data_rows[3].select('td')[1].text
        master_data['Marktkapitalisierung'] = master_data_rows[4].select('td')[1].text.replace('\xa0', ' ')
        master_data['Streubesitz'] = master_data_rows[6].select('td')[1].text.replace('\xa0', ' ')
        master_data['Nennwert'] = master_data_rows[6].select('td')[1].text.replace('\xa0', ' ')
        master_data['Stücke'] = master_data_rows[7].select('td')[1].text.replace('\xa0', ' ')
        master_data['Symbol'] = master_data_rows[9].select('td')[1].text
        master_data['ISIN'] = master_data_rows[10].select('td')[1].text
        master_data['WKN'] = master_data_rows[11].select('td')[1].text
        if master_data['Symbol'] != '--':
            identifier['Symbol'] = master_data['Symbol']
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues,
                         master_data)

class Anleihe(Instrument):
    instrument_type = 'Anleihe'
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Stammdaten')).parent.parent.select('table tr')
        master_data = {}
        master_data['Restlaufzeit'] = master_data_rows[0].select('td')[1].text
        master_data['Fälligkeit'] = master_data_rows[1].select('td')[1].text
        master_data['Ausgabedatum'] = master_data_rows[2].select('td')[1].text
        master_data['Nominalzinssatz'] = master_data_rows[3].select('td')[1].text.replace('\xa0', ' ')
        master_data['Anleihevolumen'] = master_data_rows[4].select('td')[1].text.replace('\xa0', ' ')
        master_data['Kupon-Art'] = master_data_rows[5].select('td')[1].text
        master_data['Zinszahlung'] = master_data_rows[6].select('td')[1].text.replace('\xa0', ' ')
        master_data['Zinstermin'] = master_data_rows[7].select('td')[1].text
        master_data['Emittent'] = master_data_rows[8].select('td')[1].text
        master_data['Sitz Emitt.'] = master_data_rows[9].select('td')[1].text
        master_data['Typ'] = master_data_rows[10].select('td')[1].text
        master_data['Währung'] = master_data_rows[11].select('td')[1].text
        master_data['Mindestanlage'] = master_data_rows[12].select('td')[1].text
        master_data['ISIN'] = master_data_rows[14].select('td')[1].text
        master_data['WKN'] = master_data_rows[15].select('td')[1].text
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues,
                         master_data)

class ETF(Instrument):
    instrument_type = 'ETF'
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Stammdaten')).parent.parent.select('table tr')
        master_data = {}
        master_data['Anlagekategorie'] = master_data_rows[0].select('td')[1].text.strip()
        master_data['Währung'] = master_data_rows[1].select('td')[1].text.strip()
        master_data['Laufende Kosten'] = master_data_rows[2].select('td')[1].text.strip().replace('\xa0', ' ')
        master_data['Fondsart'] = master_data_rows[3].select('tr table tr td')[1].text.strip()
        master_data['Fondsvolumen'] = master_data_rows[5].select('td')[1].text.strip().replace('\xa0', ' ')
        master_data['Symbol'] = master_data_rows[9].select('td')[1].text.strip()
        master_data['ISIN'] = master_data_rows[10].select('td')[1].text.strip()
        master_data['WKN'] = master_data_rows[11].select('td')[1].text.strip()
        if master_data['Symbol'] != '--':
            identifier['Symbol'] = master_data['Symbol']
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues, master_data)

class Fonds(Instrument):
    instrument_type = 'Fonds'
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Stammdaten')).parent.parent.select('table tr')
        master_data = {}
        master_data['Fondskategorie Name'] = master_data_rows[0].select('td')[1].select_one('a').attrs['title']
        master_data['Fondskategorie Link'] = master_data_rows[0].select('td')[1].select_one('a').attrs['data-plugin'].split("'")[1]
        master_data['Währung'] = master_data_rows[1].select('td')[1].text
        master_data['Ausgabeaufschlag Fondsgesellschaft'] = master_data_rows[2].select('td')[1].text.strip().replace('\xa0', ' ')
        master_data['Laufende Kosten'] = master_data_rows[3].select('td')[1].text.strip().replace('\xa0', ' ')
        master_data['Art'] = master_data_rows[4].select('tr td table tr td')[1].text.strip().replace('\xa0', ' ').replace('\n', ' ').replace('  ', '')
        master_data['Fondsvolumen'] = master_data_rows[6].select('td')[1].text.strip().replace('\xa0', ' ')
        master_data['Symbol'] = master_data_rows[7].select('td')[1].text
        master_data['ISIN'] = master_data_rows[8].select('td')[1].text
        if master_data['Symbol'] != '--':
            identifier['Symbol'] = master_data['Symbol']
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues, master_data)

class Optionsschein(Instrument):
    instrument_type = 'Optionsschein'
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Stammdaten')).parent.parent.select('table tr')
        master_data = {}
        master_data['letzter Handelstag'] = master_data_rows[0].select('td')[1].text
        master_data['Fälligkeit'] = master_data_rows[1].select('td')[1].text
        master_data['Basispreis'] = master_data_rows[2].select('td')[1].text
        master_data['Basiswert Name'] = master_data_rows[3].select('td')[1].select_one('a').attrs['title']
        master_data['Basiswert Link'] = master_data_rows[3].select('td')[1].select_one('a').attrs['href']
        master_data['Basiswert ID'] = master_data['Basiswert Link'].split('/')[-1]
        master_data['Bezugsverhältnis'] = master_data_rows[5].select('td')[1].text
        master_data['Typ'] = master_data_rows[6].select('td')[1].text
        master_data['Name Emittent'] = master_data_rows[7].select('td')[1].select_one('a').attrs['title'].replace(
            ', Emittent Kontakt', '')
        master_data['Link Emittent'] = master_data_rows[7].select('td')[1].select_one('a').attrs['href']
        master_data['Währung'] = master_data_rows[8].select('td')[1].text
        master_data['Symbol'] = master_data_rows[9].select('td')[1].text
        master_data['ISIN'] = master_data_rows[10].select('td')[1].text
        master_data['WKN'] = master_data_rows[11].select('td')[1].text
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues, master_data)

class Zertifikat(Instrument):
    instrument_type = 'Zertifikat'
    def __init__(self, soup, identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues):
        master_data_rows = soup.find(text=re.compile('Stammdaten')).parent.parent.select('table tr')
        master_data = {}
        master_data['Stammdaten'] = 'für Zertifikate nicht unterstützt'
        super().__init__(identifier, name, instrument_type, id_notations, live_trading_venues, exch_trading_venues, master_data)

class InstrumentCrawler():
    def __init__(self):
        self.search_id = ''
        self.instrument_type = ''

    def crawl_raw_data(self, search_id):
        search_id = search_id.upper()
        payload = {'SEARCH_VALUE': search_id, 'SEARCH_REDIRECT': True}
        r = requests.get(base_url, params=payload)
        #        print(r.url)
        soup = None
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
        else:
            print('Seite konnte nicht geladen werden: ', base_url)
        return soup

    def crawl_course_data(self, search_id):
        soup = self.crawl_raw_data(search_id)
        pass

    def crawl_base_data(self, search_id):
        soup = self.crawl_raw_data(search_id)
        headline_h1 = soup.select_one('h1')
        headline_h2 = soup.select_one('h2')
        name = None
        identifier = None
        instrument_type = None
        for t in instrument_types:
            if t in standard_types:
                if t in str(headline_h1):
                    name = headline_h1.text.replace(t, '').strip()        # Nur letzter String am Ende sollte ersetzt werden!!!
                    identifier = {
                        'WKN'    : headline_h2.text.strip().split()[1] ,
                        'ISIN'   : headline_h2.text.strip().split()[3] ,
                        'Symbol' : ''
                    }
                    instrument_type = t
                    break
            elif t in special_types:
                if t in str(headline_h2):
                    name = headline_h1.text.replace(t, '').strip()
                    identifier = {
                        'wkn': headline_h2.text.strip().split()[2],
                        'isin': '',
                        'symbol': ''
                    }
                    instrument_type = t
                    break
            else:
                instrument_type = "unknown"

        # Aufbau eines Dictionary mit allen Handeslplätzen und zugehörigen ID_Notations:

        id_notations_dict = {}
        id_notations_list = soup.select('body div.grid.grid--no-gutter table.simple-table option')
        if len(id_notations_list) > 0:
            # mehrere Handelsplätze verfügbar, daher Liste von 'option's gefunden
            for id in id_notations_list:
                id_notations_dict[id.attrs['label']] = id.attrs['value']
        else:
            # nur ein Handelsplatz, keine Selektion möglich, daher keine 'option's und keine 'ID_Notation's gefunden
            table_rows = soup.select('body div.grid.grid--no-gutter table.simple-table')[0].select('tr')
            name = table_rows[0].select('td')[1].text.strip()
            iden = table_rows[-1].select('td')[1].select_one('a').attrs['data-plugin'].split('ID_NOTATION%3D')[1].split('%26')[0]
            id_notations_dict[name] = iden

        # Extrahieren aller Life Trading Handeslplätze und Ergänzung um ID_Notation aus Dictionary:

        lt_venues = soup.find_all('td', {'data-label': 'LiveTrading'})
        lt_venue_dict = {}
        for v in lt_venues:
            venue = v.text.strip()
            if venue != '--':
                lt_venue_dict[venue] = id_notations_dict[venue]

        # Extrahieren aller Börsenhandeslplätze und Ergänzung um VenueID aus Dictionary:

        ex_venues = soup.find_all('td', {"data-label": "Börse"})
        ex_venue_dict = {}
        for v in ex_venues:
            venue = v.text.strip()
            if venue != '--':
                ex_venue_dict[venue] = id_notations_dict[venue]

        match instrument_type:
            case 'Aktie':
                return Aktie(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                                 ex_venue_dict)
            case 'Anleihe':
                return Anleihe(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                                 ex_venue_dict)
            case 'ETF':
                return ETF(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                             ex_venue_dict)
            case 'Fonds':
                return Fonds(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                             ex_venue_dict)
            case 'Optionsschein':
                return Optionsschein(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                             ex_venue_dict)
            case 'Zertifikat':
                return Zertifikat(soup, identifier, name, instrument_type, id_notations_dict, lt_venue_dict,
                     ex_venue_dict)

            case 'Edelmetall':
                pass

            case 'Index':
                pass

            case 'Edelmetall':
                pass
