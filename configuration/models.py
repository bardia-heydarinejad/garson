__author__ = 'bardia'
import xml.etree.ElementTree as ET
import os


class Food:
    root = ET.parse(os.path.realpath('.') + '/configuration/stu_config.xml')

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def all_foods():
        for e in Food.root.findall('.//foods/food'):
            # How to make decisions based on attributes even in 2.6:
            yield Food(e.attrib.get('id'), e.text, int(e.attrib.get('price')))

    @staticmethod
    def max_price():
        maximum = 0
        for food in Food.all_foods():
            if food.price > maximum:
                maximum = food.price
        return maximum


if __name__ == "__main__":
    f = Food()
    print f.all_foods()