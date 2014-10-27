__author__ = 'bardia'
import xml.etree.ElementTree as ET
import os


class Food:
    root = ET.parse(os.path.join(os.path.realpath('.'), './configuration/stu_config.xml'))
    # root = ET.parse('/home/bardia/www/reserver/configuration/stu_config.xml')

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    @staticmethod
    def get_all():
        all_food = []
        for e in Food.root.findall('.//foods/food'):
            # How to make decisions based on attributes even in 2.6:
            all_food.append(Food(e.attrib.get('id'), e.text))
        return all_food

    @staticmethod
    def get_all_name():
        all_food = []
        for e in Food.root.findall('.//foods/food'):
            # How to make decisions based on attributes even in 2.6:
            all_food.append(e.text)
        return all_food

    @staticmethod
    def get_all_id():
        all_id = []
        for e in Food.root.findall('.//foods/food'):
            all_id.append(int(e.attrib.get('id')))
        return all_id

    @staticmethod
    def get_name(food_id):
        s = './/foods/food[@id="' + str(food_id) + '"]'
        node = Food.root.find(s)
        return node.text if node is not None else 'None'


class Self:
    root = ET.parse(os.path.join(os.path.realpath('.'), './configuration/stu_config.xml'))
    # root = ET.parse('/home/bardia/www/reserver/configuration/stu_config.xml')

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    @staticmethod
    def get_all():
        all = []
        for e in Self.root.findall('.//dinings/self'):
            all.append(Self(e.attrib.get('id'), e.text))
        return all


if __name__ == "__main__":
    f = Food()
