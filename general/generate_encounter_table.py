import dice, json, argparse, texttable as tt
from collections import OrderedDict
from pathlib import Path


def get_file_name(encounter_dir):
    name = str(input('What do you want to name your encounter table? (.json): '))
    if not name.endswith('.json'):
        name = name + '.json'

    file_name = encounter_dir + name
    config = Path(file_name)
    if config.is_file():
        print("File already exists!")
        overwrite = str(input("Do you want to overwrite? (N/y)") or 'N')

        if overwrite.lower() == 'y':
            return file_name
        else:
            get_file_name(encounter_dir)
    else:
        return file_name


def determine_filename():
    encounter_dir = 'data/encounters/'
    print('Directory where this table will be saved is: {0}'.format(encounter_dir))

    return(get_file_name(encounter_dir))


def get_table_length():
    try:
        length = int(input("How large will the encounter table be? (default: 20)") or 20)
    except:
        print("Please enter a valid number")
        get_table_length()

    if length < 1:
        print("Please enter a positive number")
        get_table_length()

    return length


def make_table(table_length):
    encounter_table = OrderedDict()
    encounter_headings = ["Wandering Monster", "No.", "AC", "HD", "Attacks", "Damage", "Move", "Save", "Morale",
                          "Description"]

    for x in range(1, table_length+1):
        single_encounter = OrderedDict()

        for heading in encounter_headings:
            if heading == 'No.':
                single_encounter[heading] = str(input("Enter Number appearing as a dice roll (ex. 1d6): "))
            elif heading == 'Attacks':
                single_encounter[heading] = str(input("Enter Number number of attacks (Might be in Bestiary Entry): "))
            elif heading == 'Description':
                single_encounter[heading] = str(input("Enter Description found in Bestiary Entry): "))
            elif heading == 'Wandering Monster':
                single_encounter[heading] = str(input("Enter Wandering Monster #{0}: ".format(x)))
            elif heading == 'Move':
                single_encounter[heading] = str(input("Enter Movement (ex: 60' (20') ): ".format(x)))
            else:
                single_encounter[heading] = str(input("Enter {0}: ".format(heading)))

        encounter_table[str(x)] = single_encounter

    return encounter_table


def save_table(encounter_table, filename):

    headings = ['Dice Roll']
    headings.extend([key for key in encounter_table["1"].keys() if key != 'Description'])

    tab = tt.Texttable()
    tab.set_max_width(150)
    align = ['c' for header in headings]
    tab.set_cols_align(align)

    tab.header(headings)

    for k, v in encounter_table.items():
        row = [k]
        for key, value in v.items():
            if key != 'Description':
                row.append(value)
        tab.add_row(row)

    print(tab.draw())

    save = input("Save this table to {0}? (Y/n): ".format(filename)) or 'Y'

    if save.lower() == 'y':
        with open(filename, 'w') as outfile:
            json.dump(encounter_table, outfile)
            print("File Saved")




def main():
    print("All right, lets make an encounter table!")

    filename = determine_filename()
    table_length = get_table_length()

    encounter_table = make_table(table_length)
    save_table(encounter_table, filename)


if __name__ == "__main__":
        main()