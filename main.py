from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import gui
import sys
from PyQt5 import QtWidgets
from PyQt5.Qt import QEvent, QWidget
import threading
from selenium.webdriver.chrome.options import Options


PATTERN = "[0-9.]+$"
PROXIES = 0
URL = ""
PROXIES_FILE = "proxy.txt"
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


class Parser(QtWidgets.QMainWindow, gui.Ui_MainWindow, QWidget):

    def __init__(self):
        QWidget.__init__(self)
        super().__init__(self)
        self.setupUi(self)
        self.comboBox_country.addItems(COUNTRIES)
        self.pushButton_start.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.pushButton_start and event.type() == QEvent.MouseButtonPress and \
                self.pushButton_start.isEnabled() is True:
            self.pushButton_start.setEnabled(False)
            self.start_button()
        if obj == self.pushButton_start and event.type() == QEvent.MouseButtonPress and \
                self.pushButton_start.isEnabled() is False:
            pass
        return QWidget.eventFilter(self, obj, event)

    def closeEvent(self):
        if hasattr(Parser, "self.browser"):
            self.close_browser()

    def run_browser(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)

    def close_browser(self):
        self.browser.close()

    def get_page(self, url):
        self.browser.get(url)

    def ddos_check(self):
        while True:
            try:
                self.browser.find_element_by_css_selector("#cf-content")
                time.sleep(0.1)
            except NoSuchElementException:
                break

    def check_page_proxy_end(self):
        proxies_on_page = len(self.proxy_list)
        if proxies_on_page == 0:
            return True
        else:
            return False

    def start(self, file=None):
        if file is not None:
            self.writer = Writer(self.textBrowser, self.file)
        elif file is None:
            self.writer = Writer(self.textBrowser)
        self.status = Status(self.label_status_text)
        self.status.status("Running Chrome")
        self.run_browser()
        while True:
            self.status.status("Getting page")
            self.get_page(URL)
            self.status.status("DDOS checking")
            self.ddos_check()
            self.status.status("Page parsing")
            self.proxy_list = parse_page(self.browser.page_source)
            proxy_end = self.check_page_proxy_end()
            if proxy_end is True:
                self.status.status("Ready")
                break
            else:
                for i in self.proxy_list:
                    param = i.split(":")
                    proxy, port, type = param[0], param[1], param[2]
                    self.writer._write(proxy, port, type)
                    time.sleep(0.01)
                page_changer(self.country)
        self.writer._close()
        self.close_browser()
        self.pushButton_start.setEnabled(True)

    def start_button(self):
        self.country = COUNTRIES[self.comboBox_country.currentText()]
        global URL
        URL = "https://hidemyna.me/en/proxy-list/?country={0}&start={1}#list".format(self.country, PROXIES)
        if self.checkBox.isChecked():
            self.file = PROXIES_FILE
            threading.Thread(target=self.start, args=(self.file,)).start()
        elif not self.checkBox.isChecked():
            threading.Thread(target=self.start).start()


class Writer:
    def __init__(self, text_browser, file=None):
        self.writer = text_browser
        if file is not None:
            self.file = open(file, "r+")

    def _write(self, proxy=None, port=None, type=None):
        if proxy is not None and port is not None and type is not None:
            self.writer.append('{0}:{1} \t {2:>8}'.format(proxy, port, type))
            try:
                self.file.write('{0}:{1};{2}\n'.format(proxy, port, type))
            except AttributeError:
                pass

    def _close(self):
        try:
            self.file.close()
        except AttributeError:
            pass

class Status:
    def __init__(self, status_obj):
        self.obj = status_obj

    def status(self, message):
        self.obj.setText("")
        self.obj.setText(message)


def parse_page(page_source):
    soup = BeautifulSoup(page_source, features="lxml")
    proxies = soup.findAll("td")
    raw_list = []
    for proxy in proxies:
        raw_list.append(str(proxy.get_text()))
    proxies = []
    ports = []
    types = []
    col = 0
    while True:
        try:
            proxy = raw_list[col]
            col += 1
            port = raw_list[col]
            col += 3
            type = raw_list[col]
            proxies.append(proxy)
            ports.append(port)
            types.append(type)
            col += 3
        except IndexError:
            break
    proxy_list = [x[0] + ":" + x[1] + ":" + x[2] for x in zip(proxies, ports, types)]
    return proxy_list


def page_changer(country):
    global URL
    global PROXIES
    PROXIES += 64
    URL = "https://hidemyna.me/en/proxy-list/?country={0}&start={1}#list".format(country, PROXIES)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Parser()
    window.show()
    app.exec_()
