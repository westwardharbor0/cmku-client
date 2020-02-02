from datetime import datetime

from marshmallow import Schema
from marshmallow.fields import Str, Integer, DateTime, Nested, List

from ..lib.parser import (
    CMKUParser, ACTION_LIST_URL, ACTION_EXHIBITION_DETAIL_URL, ACTION_TRAINING_DETAIL_URL,
    ACTION_TYPE_EXHIBITION, ACTION_TYPE_TRAINING
)


def _parse_action_date(date, position=0):
    """
    Post processing if date
    :param date: date string
    :param position: 1 or 0 , if date is from or to
    :return: datetime with parsed date
    """
    if "-" in date:
        return datetime.strptime(date.split("-")[position].strip(), "%d.%m.%Y")
    return datetime.strptime(date, "%d.%m.%Y")


def _prepare_date(ins):
    """
    Post processing of date which can contain from and to date
    :param ins: action instance
    """
    ins.date_from = _parse_action_date(ins._date)
    ins.date_to = _parse_action_date(ins._date, position=1)


def _prepare_phone(ins):
    """
    Post processing of phone string which can contain multiple
    :param ins: action instance
    :return: array of phone strings
    """
    if not hasattr(ins, "phone"):
        ins.phone = ""
        return
    phone = ins._phone
    if "," in phone:
        ins.phone = [p.strip() for p in phone.split(",")]
        return
    ins.phone = [phone.strip()]


class ActionGeneralSchema(Schema):
    """
    General schema for action
    """
    _url = ""
    id = Integer(default="")
    name = Str(default="")
    _date = Str(default="")
    date_from = DateTime()
    date_to = DateTime()
    url = Str(default="")
    place = Str(default="")
    _phone = Str(default="")
    phone = List(Str)
    email = Str(default="")
    organizer = Str(default="")
    award = Str(default="")



    @classmethod
    def load_action_detail(cls, action_id):
        """
        Loads detail of action
        :param action_id: int from URL
        :return: instance of called action detail class
        """
        ins = cls()
        content = CMKUParser.get_url_soup(cls._url.format(action_id)).find(id="content")
        ins.id = action_id
        ins.name = content.find_all("h2")[0].get_text()
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
        _prepare_date(ins)
        _prepare_phone(ins)
        return ins


class ExhibitionActionSchema(ActionGeneralSchema):
    """
    Class for action exhibition actions loading
    """
    _url = ACTION_EXHIBITION_DETAIL_URL


class TrainingActionSchema(ActionGeneralSchema):
    """
    Class for action training actions loading
    """
    _url = ACTION_TRAINING_DETAIL_URL


class ShortInfoActionSchema(Schema):
    """
    Class for short type record of action
    """
    date_from = DateTime(format="%d.%m.%Y")
    name = Str()
    city = Str()
    id = Integer()
    type = Str()

    @staticmethod
    def get_action_type(url):
        """
        Returns type of action stored in url
        :param url: url string from action href
        :return: action type string
        """
        if ACTION_TYPE_EXHIBITION in url:
            return ACTION_TYPE_EXHIBITION
        return ACTION_TYPE_TRAINING

    def load_action_detail(self):
        """
        Loads full action detail
        :return: instance of action detail
        """
        if self.type == ACTION_TYPE_EXHIBITION:
            return ExhibitionActionSchema.load_action_detail(self.id)
        return TrainingActionSchema.load_action_detail(self.id)


class ShortInfoActionListSchema(Schema):
    """
    Class for listing short records of actions
    """
    list = List(Nested(ShortInfoActionSchema(many=True)))
    total = Integer()

    @classmethod
    def load_by_date(cls, date_from=None, date_to=None, action_type=None):
        """
        Loads action list in date range and specific optional type
        :param date_from: datetime instance
        :param date_to: datetime instance
        :param action_type: type of action string
        :return: instance of short type action list
        """
        ins, raw_list = cls(), []
        params = CMKUParser.generate_list_actions_params(date_from, date_to, action_type)
        content = CMKUParser.post_url_soup(ACTION_LIST_URL, params).find(id="content")
        for tr in content.find_all("tr"):
            tds = tr.find_all("td")
            name_date = tds[1].get_text().replace("\n", "")
            url = tr.find_all("a")[0].get("href")
            raw_list.append({
                "date_from": tds[0].get_text(),
                "name": name_date.split("(")[0].strip(),
                "city": name_date.split("(")[1].replace(")", "").strip(),
                "id": url.split("/")[-1],
                "type": ShortInfoActionSchema.get_action_type(url)
            })
        ins.list = raw_list
        ins.total = len(raw_list)
        return ins
