from . import utils
from .hook import Hooker

debug = utils.Logger.debug()


class GameManager:
    __instance = None

    def __init__(self, path=None):
        self.path = path
        debug(self.path)

        self.pid = []

        self._init_game_info()
        list(map(Hooker.instance().attach, self.pid))
        debug(self.pid)

    @classmethod
    def instance(cls, path=None):
        if cls.__instance is None:
            cls.__instance = cls(path)

        return cls.__instance

    def _init_game_info(self):
        self.pid = utils.find_all_pid(self.path)
