__author__ = 'bardia'
import xml.etree.ElementTree as ET
import os


class Food:
    root = ET.parse(os.path.realpath('.') + '/configuration/stu_config.xml')

    def __init__(self, id_, name, price):
        self.id_ = id_
        self.name = name
        self.price = price

    @staticmethod
    def get_all():
        all = []
        for e in Food.root.findall('.//foods/food'):
            # How to make decisions based on attributes even in 2.6:
            all.append(Food(e.attrib.get('id'), e.text, int(e.attrib.get('price'))))
        return all

    @staticmethod
    def get_all_id():
        all_id = []
        for e in Food.root.findall('.//foods/food'):
            all_id.append(int(e.attrib.get('id')))
        return all_id

    @staticmethod
    def max_price():
        maximum = 0
        for food in Food.get_all():
            if food.price > maximum:
                maximum = food.price
        return maximum

    @staticmethod
    def get_name(food_id):
        s = './/foods/food[@id="' + str(food_id) + '"]'
        node = Food.root.find(s)
        return node.text if node is not None else 'None'

    @staticmethod
    def get_price(food_id):
        s = './/foods/food[@id="' + str(food_id) + '"]'
        node = Food.root.find(s)
        return node.attrib.get('price') if node is not None else 'None'


class Self:
    root = ET.parse(os.path.realpath('.') + '/configuration/stu_config.xml')

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
    print f.get_all()