from .model.club import ClubSchema
from .model.action import TrainingActionSchema, ExhibitionActionSchema, ShortInfoActionListSchema
from .lib.parser import ACTION_TYPE_EXHIBITION, ACTION_TYPE_TRAINING
from .lib.exceptions import ActionTypeNotSpecified


class ActionTypes:
    """
    All types of actions on cmku.cz
    """
    EXHIBITION = ACTION_TYPE_EXHIBITION
    TRAINING = ACTION_TYPE_TRAINING


class CMKUCLient(object):
    """
    Client to enable access to data on CMKU
    """
    def __init__(self, cache=True):
        self._enabled_cache = cache
        self._cache = {}

    def _store_cache(self, params, result):
        """
        Stores loaded result in cache
        :param params: key based on function kwargs
        :param result: result of call
        """
        if self._enabled_cache:
            self._cache[params] = result

    def _check_cache(self, params):
        """
        Checks if result is already loaded once
        :param params: key based on function kwargs
        :return: call result if found
        """
        if not self._enabled_cache:
            return None
        return self._cache.get(params)

    def load_actions_in_range(self,  date_from=None, date_to=None, action_type=None):
        """
        Loads all actions in date range  and optional action type
        :param date_from: datetime
        :param date_to: datetime
        :param action_type: string or ActionsType member
        :return: ShortInfoActionList instance
        """
        params = (date_from, date_to, action_type, )
        cache = self._check_cache(params)
        if cache:
            return cache
        result = ShortInfoActionListSchema.load_by_date(
            date_from=date_from,
            date_to=date_to,
            action_type=action_type
        )
        self._store_cache(params, result)
        return result

    def load_action_exhibition_detail(self, action_id):
        """
        Loads action detail
        :param action_id: id from url
        :return: instance of ExhibitionAction
        """
        params = (action_id, )
        cache = self._check_cache(params)
        if cache:
            return cache
        result = ExhibitionActionSchema.load_action_detail(action_id)
        self._store_cache(params, result)
        return result

    def load_action_training_detail(self, action_id):
        """
        Loads action detail
        :param action_id: id from url
        :return: instance of TrainingAction
        """
        params = (action_id, )
        cache = self._check_cache(params)
        if cache:
            return cache
        result = TrainingActionSchema.load_action_detail(action_id)
        self._store_cache(params, result)
        return result

    def load_action_detail(self, action_id=None, action_type=None):
        """
        Loads action detail based on ID and type
        :param action_id: id from url
        :param action_type: type from ActionsTypes
        :return: instance of TrainingAction or ExhibitionAction base on action type
        """
        params = (action_id, action_type, )
        cache = self._check_cache(params)
        if cache:
            return cache
        result = None
        if action_type == ACTION_TYPE_EXHIBITION:
            result = ExhibitionActionSchema.load_action_detail(action_id)
        if action_type == ACTION_TYPE_TRAINING:
            result = TrainingActionSchema.load_action_detail(action_id)
        self._store_cache(params, result)
        if result:
            return result
        raise ActionTypeNotSpecified("Need to specify action type")

    def load_club_detail(self, club_id=None):
        """
        Loads club detail based
        :param club_id: id from url
        :return: instance of ClubSchema
        """
        params = (club_id,)
        cache = self._check_cache(params)
        if cache:
            return cache
        result = ClubSchema.load_club_detail(club_id)
        self._store_cache(params, result)
        return result

