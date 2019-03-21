import json
from collections import OrderedDict
import os
import dice

scriptDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tables')

class MagicItem:
    def __init__(self):
        type = None

        with open(os.path.join(scriptDirectory, 'magic_subtable.json')) as json_class_file:
            self.magic_item_table = json.load(json_class_file, object_pairs_hook=OrderedDict)

    def get_random_item_type(self):
        roll = dice.roll('1d%')
        for item in self.magic_item_table['item_types']:
            if sum(roll) in range(int(item[0][0]), int(item[0][1] + 1)):
                self.type = item[1]
        if self.type == None:
            raise Exception('Unable to get random item type. Check magic_subtable')

    def get_item_attributes(self):
        if self.type is None:
            self.get_random_item_type()



mag = MagicItem()
mag.get_random_item_type()
print(mag.type)