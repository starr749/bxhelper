import dice
import texttable as tt
import json

with open('data/modifiers.json') as json_file:
    modifier_data = json.load(json_file)

mod_list = {"Strength": modifier_data['str'], "Intelligence": modifier_data['int'], "Wisdom": modifier_data['wis'],
            "Dexterity": modifier_data['dex'], "Constitution": modifier_data['con'], "Charisma": modifier_data['cha']}

class_list = ["Fighter", "Magic-User", "Cleric", "Thief", "Dwarf", "Halfling", "Elf"]
recommended_classes = {}


def main():

    ability_dict = {}
    ability_scores = {}
    headings = ['Attribute', 'Score', 'Dice Rolls', 'Modifier', '', 'Class', 'Bonus']
    attributes = ["Strength", "Intelligence", "Wisdom", "Dexterity", "Constitution", "Charisma"]
    scores = []
    dice_rolls = []
    modifiers = []
    for att in attributes:
        roll = dice.roll('3d6')
        scores.append(sum(roll))
        dice_rolls.append(roll)
        modifiers.append(mod_list[att][str(sum(roll))])

        ability_dict.setdefault(sum(roll), []).append(att)
        ability_scores[att] = sum(roll)

    tab = tt.Texttable()
    tab.header(headings)

    bonuses = []
    for class_name in class_list:
        if class_name in ["Halfling", "Elf"]:
            bonuses.append(get_two_prime_stat_bonus(class_name, ability_scores))
        else:
            bonuses.append(get_one_prime_stat_bonus(class_name, ability_scores))

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


def get_one_prime_stat_bonus(class_name, ability_scores):
    class_prime_req = {"Fighter": "Strength", "Magic-User": "Intelligence", "Cleric": "Wisdom", "Thief": "Dexterity",
                       "Dwarf": "Strength"}

    if class_name == 'Dwarf' and ability_scores['Constitution'] < 9:
        return "Constitution too low to be Dwarf"

    if ability_scores[class_prime_req[class_name]] >= 16:
        recommended_classes.setdefault(2, []).append(class_name)
        return "\t+{bonus}% XP".format(bonus="10")

    if ability_scores[class_prime_req[class_name]] >= 13:
        recommended_classes.setdefault(1, []).append(class_name)
        return "\t+{bonus}% XP".format(bonus="5")

    if ability_scores[class_prime_req[class_name]] <= 8:
        return "\t-{bonus}% XP".format(bonus="10" if ability_scores[class_prime_req[class_name]] <= 5 else "5")

    else:
        return "No bonus to XP"


def get_two_prime_stat_bonus(class_name, ability_scores):
    class_prime_req = {"Elf": ["Strength", "Intelligence"],
                       "Halfling": ["Strength", "Dexterity"]}

    if class_name == 'Elf' and ability_scores['Intelligence'] < 9:
        return "Intelligence too low to be Elf"

    if class_name == 'Halfling' and (ability_scores['Dexterity'] < 9 or ability_scores['Constitution'] < 9):
        return "Dexterity / Constitution too low to be Halfling"

    bonuses = 0
    for att in class_prime_req[class_name]:
        if ability_scores[att] >= 13:
            bonuses += 1
        if ability_scores[att] <= 8:
            bonuses -= 1

    if bonuses != 0:
        recommended_classes.setdefault(bonuses, []).append(class_name)
        return "\t{sign}{bonus}% XP".format(sign="+" if bonuses > 0 else "", bonus=bonuses * 5)
    else:
        return "No bonus to XP"


if __name__ == "__main__":
    main()
