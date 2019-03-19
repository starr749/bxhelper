import dice, json, argparse, texttable as tt
from collections import OrderedDict

default_encounter_file = 'data/encounters/level{0}.json'


def roll_encounter(wandering_monsters):
    return wandering_monsters[str(sum(dice.roll('1d20')))]


def get_level():
    return input('Enter the encounter level: ')


def get_surprise_possible():
    surprise = input('Is Surprise Possible? (Y/n) ') or 'Y'
    return True if surprise == 'Y' else False


def get_encounter_chance():
    chance = int(input('Enter chance (x of 6) the PCs have of encountering monsters (default is 1): ') or "1")
    if chance >= 6:
        answer = (input('Make encounter guaranteed? (Y/n)') or 'Y')
        if answer != 'Y':
            get_encounter_chance()
        else:
            return chance
    return chance


def load_file(file_path):
    with open(file_path) as json_class_file:
        return json.load(json_class_file, object_pairs_hook=OrderedDict)


def print_table(encounter, surprise_possible):
    headings = [k for k in encounter.keys() if k != 'Description']
    row = []

    for heading in headings:
        if heading == 'No.':
            number_roll = dice.roll(encounter[heading])
            row.append("{0} ({1} {2})".format(sum(number_roll), encounter[heading], number_roll))
        else:
            row.append(encounter[heading])

    headings.append("Distance")
    row.append("{0}'".format(sum(dice.roll('2d6')) * 10))

    if surprise_possible:
        headings.append("Monster Surprised?")
        surprise_roll = dice.roll('1d6')
        row.append("{0} (Roll: {1})".format('Yes!', surprise_roll) if sum(surprise_roll) <= 2
                   else "{0} (Roll: {1})".format('No', surprise_roll))

    tab = tt.Texttable()
    tab.set_max_width(150)
    align = ['c' for header in headings]
    tab.set_cols_align(align)

    tab.header(headings)
    tab.add_row(row)

    descTab = tt.Texttable()
    descTab.set_max_width(150)
    descTab.header(['Description'])
    descTab.add_row([encounter['Description']])

    print(tab.draw())
    print(descTab.draw())


def reaction_roll():
    modifier = int(input('Input any modifiers (if any) ') or 0)
    react_roll = dice.roll('2d6')
    reaction = dice_reaction(sum(react_roll, modifier))
    print_reaction(reaction, react_roll, modifier)


def dice_reaction(dice_roll):
    if dice_roll >= 12:
        return "Enthusiastic Friendship"
    if dice_roll >= 9:
        return "No attack, monster leaves or considers offers"
    if dice_roll >= 6:
        return "Uncertain, monster confused"
    if dice_roll >= 3:
        return "Hostile, possible attack"
    else:
        return "Immediate Attack"


def print_reaction(reaction, roll, modifier):
    headings = ['Dice Roll', 'Modifier', 'Reaction']
    row = ["{0} \n(Roll: {1} {2})".format(sum(roll) + modifier, sum(roll), roll),
           "{0} {1} ".format("+" if modifier > 0 else "", modifier),
           reaction]

    tab = tt.Texttable()
    tab.set_max_width(150)
    align = ['c' for header in headings]
    tab.set_cols_align(align)

    tab.header(headings)
    tab.add_row(row)

    print(tab.draw())


def main(file_path=None):
    if file_path is None:
        level = get_level()
        encounters = load_file(default_encounter_file.format(level))
    else:
        encounters = load_file(file_path)

    chance = get_encounter_chance()
    surprise = get_surprise_possible()

    roll = dice.roll('1d6')

    if sum(roll) > chance:
        print("Roll: {0} No encounter!".format(roll))
    else:
        print_table(roll_encounter(encounters), surprise)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="Load Encounter Table from JSON File instead of the leveled encounter "
                                             "tables in the book.")

    parser.add_argument("-r", "--reaction", help="Make a Monster reaction roll", action="store_true")

    args = parser.parse_args()

    if args.reaction:
        reaction_roll()
        exit()

    if args.file:
        # TODO add file validation here
        main(args.file)
    else:
        main()
