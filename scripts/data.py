import json
import os

from .components import DataObject

__all__ = ["Data"]

""" Loads all the data/configurations needed to play the game """


class Data:

    path = "data/"
    scriptable_objs = ["entities", "weapons", "engines", "bullets"]

    @classmethod
    def load(cls):
        errors = []
        for fileName in os.listdir(cls.path):
            if fileName.endswith("json"):
                with open(cls.path + fileName, "r") as fileData:

                    data = json.load(fileData)

                    try:
                        attr_name = os.path.splitext(fileName)[0]
                        if attr_name in cls.scriptable_objs:
                            cls.load_objects(attr_name, data)
                        else:
                            setattr(Data, attr_name, data)
                    except  json.JSONDecodeError:
                        errors.append(f"Error Decoding {fileName} JSON File.")
        return errors

    @classmethod
    def load_objects(cls, attr_name, objects):
        data = {}
        for name, obj in objects.items():
            data[name] = DataObject(obj)
            setattr(cls, attr_name, data)

    @classmethod
    def save(cls):
        for fileName in os.listdir(cls.path):
            if fileName.endswith("json"):
                with open(cls.path + fileName, "w") as fileData:
                    
                    attr_name = os.path.splitext(fileName)[0]
                    data = getattr(Data, attr_name)

                    if attr_name in cls.scriptable_objs:
                        data = cls.save_objects(data)
                        json.dump(data, fileData, indent=2)
                    else:
                        json.dump(data, fileData, indent=2)
    
    @classmethod
    def save_objects(cls, objects) -> dict:
        data = {}
        for name, obj in objects.items():
            data[name] = obj.to_dict()
        return data