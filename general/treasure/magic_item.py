import json
from collections import OrderedDict
import os
import dice

scriptDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tables')


class MagicItem:
    def __init__(self, item_type=None):
        self.item_type = item_type

        with open(os.path.join(scriptDirectory, 'magic_subtable.json')) as json_class_file:
            self.magic_item_table = json.load(json_class_file, object_pairs_hook=OrderedDict)

        self.item_description = self.get_item_description()

    def get_random_item_type(self):
        roll = dice.roll('1d%')
        self.item_type = self.roll_on_table_with_range( sum(roll), 'item_types')
        if self.item_type is None:
            raise Exception('Unable to get random item type. Check magic_subtable')

    def get_item_description(self):
        if self.item_type is None:
            self.get_random_item_type()

        specific_item_table = self.magic_item_table[self.item_type]
        roll = sum(dice.roll('1d{0}'.format(len(specific_item_table))))
        description = (specific_item_table[roll-1])[1]         # -1 because arrays start at 0

        if self.item_type == 'Weapon/Armor':
            if 'Armor' in description:
                armor = self.roll_armor_type()
                description = description.replace('Armor', armor + ' Armor')

        if self.item_type == 'Scroll' and roll <= 3: # we got a spell roll!
            cleric_scroll_roll = dice.roll('1d%')
            is_cleric_scroll = sum(cleric_scroll_roll) <= 25 # check to see if it's a cleric scroll!


            scroll_spells = []
            for i in range(roll):
                scroll_spells.append(self.get_random_spell(is_cleric_scroll))

            description = "A Spell Scroll with {0} spell{1} - {2}"\
                .format(len(scroll_spells),'s' if len(scroll_spells) > 1 else '', ', '.join(scroll_spells))

        return description

    def roll_armor_type(self):
        armor_roll = sum(dice.roll('1d8'))
        return self.roll_on_table_with_range(armor_roll, 'Armor')

    def get_random_spell(self, is_cleric_scroll=False):
        if is_cleric_scroll:
            spell_level = str(dice.roll('1d2 + 1'))
        else:
            level_roll = sum(dice.roll('1d6'))
            spell_level = str(self.roll_on_table_with_range(level_roll, 'Spell Level'))

        spell_table = self.magic_item_table['Spells']['Cleric'] if is_cleric_scroll else self.magic_item_table['Spells']['Magic-User']
        roll = sum(dice.roll('1d{0}'.format(len(spell_table[spell_level]))))
        return (spell_table[spell_level][roll-1])[1]

    def roll_on_table_with_range(self, roll, table):
        for item in self.magic_item_table[table]:
            if roll in range(int(item[0][0]), int(item[0][1] + 1)):
                return item[1]

