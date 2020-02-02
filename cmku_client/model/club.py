from marshmallow import Schema
from marshmallow.fields import Str, Integer, List, Nested

from ..lib.parser import (
    CMKUParser, CLUB_DETAIL_URL, BREED_STRING, ACTION_TYPE_EXHIBITION
)

from .action import _prepare_phone, ShortInfoActionSchema


class BreedSchema(Schema):
    """
    Schema of breed in club detail
    """
    id = Integer()
    url = Str()
    name = Str()


class ClubSchema(Schema):
    """
    Schema of club detail
    """
    id = Integer(default=-1)
    name = Str(default="")
    url = Str(default="")
    place = Str(default="")
    _phone = Str(default="")
    phone = List(Str)
    email = Str(default="")
    person = Str()

    # lists of data in detail
    breeds = List(Nested(BreedSchema(many=True)))
    actions = List(Nested(ShortInfoActionSchema(many=True)))

    _url = CLUB_DETAIL_URL

    @classmethod
    def load_club_detail(cls, club_id):
        """
        Loads club detail and returns instance
        :param club_id: club id from url
        :return: instance of club detail class
        """
        ins = cls()
        content = CMKUParser.get_url_soup(cls._url.format(club_id)).find(id="content")
        ins.id = club_id
        ins.name = content.find_all("h2")[0].get_text()

        breeds_list = []
        actions_list = []
        hrefs = content.find_all("a")
        for i, href in enumerate(hrefs):
            curl = href.get("href")
            if BREED_STRING in  curl:
                breeds_list.append({
                    "id":  curl.split("/")[-1],
                    "url":  curl,
                    "name": curl
                })
            if ACTION_TYPE_EXHIBITION in curl:
                actions_list.append({
                    "id": curl.split("/")[-1],
                    "name": href.get_text(),
                    "date_from": cls._find_date_by_name(href.get_text(), content.get_text()),
                    "city": "",
                    "type": ACTION_TYPE_EXHIBITION
                })
        ins.actions = actions_list
        ins.breeds = breeds_list
        children = list(content.children)
        for i, child in enumerate(children):
            if isinstance(child, str):
                continue
            key = CMKUParser.translate_label(child.get_text())
            if key != "":
                val = children[i + 1]
                if val.strip() == "":
                    val = children[i + 2].get_text()
                if isinstance(val, str):
                    val = val.strip()
                setattr(ins, key, val)
        _prepare_phone(ins)
        return ins

    @staticmethod
    def _find_date_by_name(name, content):
        """
        Finds date in splited club detail for action info
        :param name: name of action
        :param content: text of club detail
        :return: date found in clu detail
        """
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if name.lower() in line.lower():
                return lines[i].split("(")[1].split(")")[0].strip()

        return "00.00.0000"

