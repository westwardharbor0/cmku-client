import requests

from bs4 import BeautifulSoup

# ACTION TYPES
ACTION_TYPE_ALL = "vse"
ACTION_TYPE_EXHIBITION = "vystavy"
ACTION_TYPE_TRAINING = "vycvikove_akce"

BREED_STRING = "seznam_plemen"

# USED URLS FOR DATA MINING
ACTION_LIST_URL = "https://www.cmku.cz/cz/kalendar-147/"
ACTION_EXHIBITION_DETAIL_URL = "https://www.cmku.cz/cz/vystavy-137/{}"
ACTION_TRAINING_DETAIL_URL = "https://www.cmku.cz/cz/vycvikove-akce-141/{}"
CLUB_DETAIL_URL = "https://www.cmku.cz/cz/clenske-subjekty-116/{}"

# KEYS FOR IN TEXT WORDS TO ASSIGN TO SCHEMAS
DETAIL_KEY_TRANSLATION = {
    "Místo konání": "place",
    "WWW": "url",
    "E-mail": "email",
    "Telefon": "_phone",
    "Termín konání": "_date",
    "Pořadatel": "organizer",
    "Titul": "award",
    "Číslo": "number",
    "Mobilní telefon": "_phone",
    "Kontaktní osoba": "person",
    "Adresa": "location"
}


class CMKUParser(object):
    """
    Class to parse data from web and supply to structure
    """
    @staticmethod
    def generate_list_actions_params(date_from=None, date_to=None, actions_type=ACTION_TYPE_EXHIBITION):
        return {
            'kalendar_typ': actions_type,
            'kalendar_od': date_from.strftime("%d.%m.%Y"),
            'kalendar_do': date_to.strftime("%d.%m.%Y")
        }

    @staticmethod
    def post_url_soup(url, params={}):
        """
        Loads data from url and stores in bs class
        :param url: path to web page endpoint
        :param params: form params to post
        :return: bs instance
        """
        res = requests.post(url, params)
        res.encoding = 'utf-8'
        return BeautifulSoup(res.text, "lxml")

    @staticmethod
    def get_url_soup(url):
        """
        Loads data from url and stores in bs class
        :param url: path to web page endpoint
        :param data:
        :return: bs instance
        """
        res = requests.get(url)
        res.encoding = 'utf-8'
        return BeautifulSoup(res.text, "lxml")

    @staticmethod
    def translate_label(label):
        """
        Finds label in text and returns key to be assigned
        :param label: text to be searched for key
        :return: key to schema
        """
        for la in DETAIL_KEY_TRANSLATION:
            if la in label.strip():
                return DETAIL_KEY_TRANSLATION[la]
        return ""
