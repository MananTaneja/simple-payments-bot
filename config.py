from configparser import ConfigParser


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Config:
    def __init__(self, file_name='config.ini'):
        self.config = ConfigParser(dict_type=AttrDict)
        self._file_name = file_name
        self.config.read(file_name)
        for key in self.config._sections.keys():
            setattr(self, key, getattr(self.config._sections, key))


config = Config()
