import os
import dice, json, argparse, texttable as tt
from .magic_item import MagicItem
from collections import OrderedDict

scriptDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tables')

class Hoard:

    def __init__(self, treasure_type):
        with open(os.path.join(scriptDirectory, 'treasure_table.json')) as json_class_file:
            self.treasure_table = json.load(json_class_file, object_pairs_hook=OrderedDict)

        valid_types = [v for v in self.treasure_table.keys() if v != 'Gem Table']

        if treasure_type not in valid_types:
            raise Exception('Invalid Treasure Type. Valid Types: {0}'.format(valid_types))

        self.average = "Undefined"
        self.copper = 0
        self.silver = 0
        self.electrum = 0
        self.gold = 0
        self.platinum = 0
        self.gems = []
        self.jewelry = []
        self.magic_items = []

        self.roll_treasure(treasure_type)


    def roll_treasure(self, treasure_type):
        self.treasure_horde = self.treasure_table[treasure_type]

        self.copper = self.roll_coin('Copper')
        self.silver = self.roll_coin('Silver')
        self.electrum = self.roll_coin('Electrum')
        self.gold = self.roll_coin('Gold')
        self.platinum = self.roll_coin('Platinum')

        self.gems = self.roll_gems()
        self.jewelry = self.roll_jewelry()

        self.magic_items = self.roll_magic_items()

    def roll_coin(self, coin_type):
        #  "Copper":  {"chance":  25, "amount":  "3d8 * 1000"}

        coin = self.treasure_horde[coin_type]
        coin_existence = sum(dice.roll('1d%'))
        if coin_existence <= coin['chance']:
            return int(dice.roll(coin['amount']))
        else:
            return 0

    def roll_on_table_with_range(self, roll, table):
        for item in self.treasure_table[table]:
            if roll in range(int(item[0][0]), int(item[0][1] + 1)):
                return item[1]

    def roll_gems(self):
        # "Gems": {"chance":  50, "amount":  "1d100"}
        gem_data = self.treasure_horde['Gems']
        gems = []

        gems_present = sum(dice.roll('1d%'))
        if gems_present <= gem_data['chance']:
            gem_amount = sum(dice.roll(gem_data['amount']))
            for i in range(gem_amount):
                gems.append(self.roll_on_table_with_range(sum(dice.roll('1d%')),'Gem Table'))

        return gems

    def roll_jewelry(self):
        # "Jewelery":  {"chance":  50, "amount":  "10d4"}
        jewelry_data = self.treasure_horde['Jewelery']
        jewelry = []

        jewelry_present = sum(dice.roll('1d%'))
        if jewelry_present <= jewelry_data['chance']:
            gem_amount = sum(dice.roll(jewelry_data['amount']))
            for i in range(gem_amount):
                jewelry.append(dice.roll('3d6 * 100'))

        return jewelry

    def roll_magic_items(self):
        # "Magic Items":  {"chance":  15, "items": [{"amount": "2", "type": ["Any"]}, {"amount": "1", "type": ["potion"] }] }
        magic_item_data = self.treasure_horde['Magic Items']
        magic_items = []

        magic_items_present = sum(dice.roll('1d%'))
        if magic_items_present <= magic_item_data['chance']:
            for item in magic_item_data['items']:
                magic_items.extend(self.create_magic_items(item))

        return magic_items

    def create_magic_items(self, item):
        items = []

        for i in range(int(item['amount'])):

            type_roll = int(dice.roll('1d{0}'.format(len(item['type'])))) -1
            type = item['type'][type_roll]
            magic_item = MagicItem(type)
            items.append(magic_item)

        return items

    def __str__(self):
        treasure_string = ""
        if self.copper > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Copper Coins".format(self.copper)

        if self.silver > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Silver Coins".format(self.silver)

        if self.electrum > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Electrum Coins".format(self.electrum)

        if self.gold > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Gold Coins".format(self.gold)

        if self.platinum > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Gold Coins".format(self.platinum)

        if len(self.gems) > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Gem{1} worth {2} Gold Pieces"\
                .format(len(self.gems), 's' if len(self.gems) > 1 else '', sum(self.gems))

        if len(self.jewelry) > 0:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += "{0} Piece{1} of Jewelry worth {2} Gold Pieces" \
                .format(len(self.jewelry), 's' if len(self.jewelry) > 1 else '', sum(self.jewelry))

        for item in self.magic_items:
            treasure_string = self.conditionally_add_line_break(treasure_string)
            treasure_string += str(item)

        return treasure_string


    def conditionally_add_line_break(self, treasure_string):
        if treasure_string != "":
            return treasure_string + '\n'
        else:
            return treasure_string
