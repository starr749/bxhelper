import dice, argparse
import texttable as tt
import json
import math
from collections import OrderedDict

with open('data/modifiers.json') as json_file:
    mod_list = json.load(json_file, object_pairs_hook=OrderedDict)

with open('data/classes.json') as json_class_file:
    class_data = json.load(json_class_file, object_pairs_hook=OrderedDict)

class_list = [class_name for class_name in class_data.keys()]
recommended_classes = {}


def main(heroic, loaded_character=None):

    ability_dict = {}
    ability_scores = {}
    headings = ['Attribute', 'Score', 'Dice Rolls', 'Modifier', '', 'Class', 'Bonus']

    if loaded_character is not None:
        attributes, dice_rolls, modifiers, scores = pull_stats_from_char(ability_dict, ability_scores, loaded_character)
    else:
        attributes, dice_rolls, modifiers, scores = roll_stats(ability_dict, ability_scores, heroic)

    tab = tt.Texttable()
    tab.header(headings)

    bonuses = []
    for class_name in class_list:
        bonuses.append(calc_stat_bonus(class_name, ability_scores, class_data))

    gold_roll = dice.roll('3d6')

    attributes.append("Gold")
    scores.append("{0} GP".format(sum(gold_roll) * 10))
    dice_rolls.append(gold_roll)
    modifiers.append('-')

    for row in zip(attributes, scores, dice_rolls, modifiers, ['|'] * 7, class_list, bonuses):
        tab.add_row(row)

    tab.set_max_width(150)
    tab.set_deco(tt.Texttable.HEADER | tt.Texttable.BORDER | tt.Texttable.HLINES)
    tab.set_cols_align(['l', 'l', 'c', 'c', 'c', 'c', 'c'])

    s = tab.draw()
    print(s)

    recommend_classes(scores)


def roll_stats(ability_dict, ability_scores, heroic):
    attributes = [att for att in mod_list.keys()]
    scores = []
    dice_rolls = []
    modifiers = []
    for att in attributes:
        if heroic:
            roll = dice.roll('4d6^3')
        else:
            roll = dice.roll('3d6')
        scores.append(sum(roll))
        dice_rolls.append(roll)
        modifiers.append(mod_list[att][str(sum(roll))])

        ability_dict.setdefault(sum(roll), []).append(att)
        ability_scores[att] = sum(roll)
    return attributes, dice_rolls, modifiers, scores


def pull_stats_from_char(ability_dict, ability_scores, loaded_character):
    attributes = [att for att in mod_list.keys()]
    scores = []
    dice_rolls = []
    modifiers = []
    for att in attributes:
        scores.append(loaded_character[att])
        dice_rolls.append("-")
        modifiers.append(mod_list[att][str(loaded_character[att])])

        ability_dict.setdefault(loaded_character[att], []).append(att)
        ability_scores[att] = loaded_character[att]
    return attributes, dice_rolls, modifiers, scores


def recommend_classes(scores):
    bad_rolls = 0
    good_rolls = 0
    for score in scores[:-1]:
        if score <= 6:
            bad_rolls += 1
        if score > 9:
            good_rolls += 1
    if bad_rolls >= 2:
        print("!!!!!!!!! More than 1 skill 6 or lower, Recommended ReRoll !!!!!!!!!")
    if good_rolls == 0:
        print("!!!!!!!!! No good skills, Recommended ReRoll !!!!!!!!!")
    if len([v for v in [1, 2] if v in recommended_classes.keys()]) <= 0:
        print("\nNo class has any bonuses. Maybe go with Magic-User or Fighter?\n")
    if 2 in recommended_classes.keys():
        print("STRONGLY RECOMMENDED CLASSES: " + ", ".join(recommended_classes[2]))
    if 1 in recommended_classes.keys():
        print("Recommended Classes: " + ", ".join(recommended_classes[1]))


def calc_stat_bonus(class_name, ability_scores, class_data):
    too_low_att = []

    for prime_req, req_value in class_data[class_name]["Requirements"].items():
        if ability_scores[prime_req] < req_value:
            too_low_att.append(prime_req)

    if len(too_low_att) > 0:
        return "{0} too low to be {1}".format(", ".join(too_low_att), class_name)

    bonuses = 0
    if len(class_data[class_name]["Prime-Requisite"]) == 2:

        # Stupid elf having special prime-requisites making it extra hard to earn xp
        # I'm adding this logic that completely breaks my nice clean data abstraction
        # But I don't have to like it.
        if class_name == 'Elf':
            if ability_scores["Intelligence"] >= 13 and ability_scores["Strength"] >= 13:
                bonuses += 1
                if ability_scores["Intelligence"] >= 16:
                    bonuses += 1
        else:
            for att in class_data[class_name]["Prime-Requisite"]:
                if ability_scores[att] >= 13:
                    bonuses += 1
                if ability_scores[att] <= 8:
                    bonuses -= 1

    if len(class_data[class_name]["Prime-Requisite"]) == 1:
        att = class_data[class_name]["Prime-Requisite"][0]
        if ability_scores[att] >= 13:
            bonuses = 2 if ability_scores[att] >= 16 else 1
        if ability_scores[att] <= 8:
            bonuses = -2 if ability_scores[att] <= 5 else -1

    if bonuses != 0:
        recommended_classes.setdefault(bonuses, []).append(class_name)
        return "\t{sign}{bonus}% XP".format(sign="+" if bonuses > 0 else "", bonus=bonuses * 5)
    else:
        return "No bonus to XP"


def load_json_character(filepath):
    with open(filepath) as json_character_file:
        return json.load(json_character_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-hero", "--heroic", help="Rolls stats with 4d6 drop lowest", action="store_true")
    parser.add_argument("-f", "--filepath", "--file", help="Do not roll stats, instead load attribute stats from json file")

    args = parser.parse_args()

    if args.filepath:
        character = load_json_character(args.filepath)
        main(args.heroic, character)
    else:
        main(args.heroic)
