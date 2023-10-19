import json
import os

from .components import DataObject

__all__ = ["Data"]

""" Loads all the data/configurations needed to play the game """


class Data:

    path = "data/"
    # config = {}
    # levels = {}   
    # entities = {}

    @classmethod
    def load(cls):
        errors = []
        for fileName in os.listdir(cls.path):
            if fileName.endswith("json"):
                with open(cls.path + fileName, "r") as fileData:

                    data = json.load(fileData)

                    try:
                        attr_name = os.path.splitext(fileName)[0]
                        if attr_name == "entities":
                            newData = {}
                            for name, entity in data.items():
                                newData[name] = DataObject(entity)
                                setattr(Data, attr_name, newData)
                        else:
                            setattr(Data, attr_name, data)
                    except  json.JSONDecodeError:
                        errors.append(f"Error Decoding {fileName} JSON File.")
        return errors

    @classmethod
    def save(cls):
        for fileName in os.listdir(cls.path):
            if fileName.endswith("json"):
                with open(cls.path + fileName, "w") as fileData:
                    
                    attr_name = os.path.splitext(fileName)[0]
                    data = getattr(Data, attr_name)

                    if attr_name == "entities":
                        new_data = {}
                        for name, entity in data.items():
                            new_data[name] = entity.to_dict()

                        json.dump(new_data, fileData, indent=4)
                    else:
                        json.dump(data, fileData, indent=4)