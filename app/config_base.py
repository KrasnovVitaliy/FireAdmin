import logging
import json


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class ConfigBase(Singleton):
    __methods_names__ = [
        'get_properties_list',
        'set_property',
        'get_property',
        'dict',
        'dumps',
        'loads',
    ]

    def get_properties_list(self):
        class_properties = []
        for i in [i for i in dir(self) if i[:1] != '_']:
            if i not in self.__methods_names__:
                class_properties.append(i)
        return class_properties

    def set_property(self, property, value):
        setattr(self, property, value)

    def get_property(self, property):
        return getattr(self, property)

    def dict(self):
        config = {}
        for p in self.get_properties_list():
            config[p] = self.get_property(p)
        return config

    def dumps(self):
        config = {}
        for p in self.get_properties_list():
            config[p] = self.get_property(p)
        return json.dumps(config)

    def loads(self, value):
        config = json.loads(value)
        for k in config.keys():
            self.set_property(k, config[k])
