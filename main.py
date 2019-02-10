from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

PATTERN = "[0-9.]+$"
PROXIES = 0
URL = ""
COUNTRIES = {
    "All": "ALADAOARAMAUATAZBDBYBEB" \
    "JBOBABWBRBGBFBIKHCMCACLCOCGCDCRCIHRCYC" \
    "ZDKDJDOECEGSVGQEEFIFRGEDEGHGRGTGNHTHNHKHUI" \
    "NIDIQIEILITJMJPKZKEKRKWKGLALVLBLSLYLTLUMKMGMWMYMV" \
    "MLMTMUMXMDMNMEMAMZMMNANPNLNZNINGNOPKPSPAPYPEPHPLPTPRROR" \
    "URWMFRSSCSGSKSISOZAESLKSDSECHSYTWTJTZTHTGTRUGUAGBUSVEVNZMZW",
    "Argentina": "AR",
    "Albania": "AL",
    "Andorra": "AD",
    "Angola": "AO",
    "Azerbaijan": "AZ",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Bangladesh": "BD",
    "Belarus": "BY",
    "Belgium": "BE",
    "Benin": "BJ",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Congo": "CG",
    "Congo, The Democratic Republic of the": "CD",
    "Costa Rica": "CR",
    "Cote D'Ivoire": "CI",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hong Kong": "HK",
    "Hungary": "HU",
    "India": "IN",
    "Indonesia": "ID",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Kazakstan": "KZ",
    "Kenya": "KE",
    "Korea": "KR",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Lao People's Democratic Republic": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Libyan Arab Jamahiriya": "LY",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Macedonia": "MK",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Mauritius": "MU",
    "Mexico": "MX",
    "Moldova": "MD",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Nigeria": "NG",
    "Norway": "NO",
    "Pakistan": "PK",
    "Palestinian Territory": "PS",
    "Panama": "PA",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Romania": "RO",
    "Russian Federation": "RU",
    "Rwanda": "RW",
    "Saint Martin": "MF",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "South Africa": "ZA",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syrian Arab Republic": "SY",
    "Taiwan": "TW",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Turkey": "TR",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Kingdom": "GB",
    "United States": "US",
    "Uruguay": "UY",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Virgin Islands, U.S.": "VI",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}


class Parser:

    def __init__(self):
        country = input("Enter country code from country dict or enter 2 or more codes like 'ARAL' or enter 'all': ").upper()
        self.browser = webdriver.Chrome()
        self.file = open("proxy.txt", "r+")
        global URL
        print(country)
        if country == "ALL":
            URL = "https://hidemyna.me/en/proxy-list/?country={0}&start={1}#list".format(COUNTRIES["All"], PROXIES)
        else:
            URL = "https://hidemyna.me/en/proxy-list/?country={0}&start={1}#list".format(country, PROXIES)

    def get_page(self, url):
        self.browser.get(url)

    def parse_page(self):
        page = self.browser.page_source
        soup = BeautifulSoup(page, features="lxml")
        self.proxies = soup.findAll("td")
        raw_list = []
        for i in self.proxies:
            raw_list.append(str(i.get_text()))
        proxies = []
        ports = []
        num = 0
        while True:
            try:
                proxy = raw_list[num]
                num += 1
                port = raw_list[num]
                proxies.append(proxy)
                ports.append(port)
                num += 6
            except IndexError:
                break
        self.proxy_list = [str(x[0]) + ":" + x[1] for x in zip(proxies, ports)]

    def write_proxies(self):
        for proxy in self.proxy_list:
            self.file.write(proxy + "\n")

    def ddos_check(self):
        while True:
            try:
                self.browser.find_element_by_css_selector("#cf-content")
                time.sleep(0.5)
            except NoSuchElementException:
                break

    def check_page_proxy_end(self):
        proxies_on_page = len(self.proxy_list)
        if proxies_on_page == 0:
            return True
        else:
            return False
        
    def page_changer(self):
        global URL
        global PROXIES
        PROXIES += 64
        URL = "https://hidemyna.me/en/proxy-list/?country=UA&start={0}#list".format(PROXIES)

    def start(self):
        while True:
            self.get_page(URL)
            self.ddos_check()
            a.parse_page()
            proxy_end = self.check_page_proxy_end()
            if proxy_end is True:
                print("Ready!")
                break
            else:
                a.write_proxies()
                a.page_changer()
        self.browser.close()


if __name__ == "__main__":
    a = Parser()
    a.start()
    # URL = "https://hidemyna.me/en/proxy-list/?country={0}&start={1}#list".format(COUNTRIES["All"], PROXIES)
    # print(URL)