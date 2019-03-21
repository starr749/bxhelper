import dice, json, argparse, texttable as tt
from collections import OrderedDict


class Treasure:

    def __init__(self, treasure_type):
        self.average = "Undefined"
        self.copper = 0
        self.silver = 0
        self.electrum = 0
        self.gold = 0
        self.gems = []
        self.jewelry = []
        self.magic_items = []

        with open('data/treasure/treasure_table.json') as json_class_file:
            self.treasure_table = json.load(json_class_file, object_pairs_hook=OrderedDict)

        self.roll_treasure(treasure_type)


    def roll_treasure(self, treasure_type):
        pass
