import dice, json, argparse, texttable as tt
from collections import OrderedDict
from  treasure.hoard import Hoard
from treasure.magic_item import MagicItem

def main(item, gen_type=None):
    if item == 'magic':
        mag = MagicItem(gen_type)
        print(mag)
    elif item == 'horde':
        if gen_type is None:
            raise Exception('Treasure hordes need a type')
        treasure = Hoard(gen_type)
        print(treasure)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--magic", help="Generates magic item", action="store_true")
    parser.add_argument("-th", "--treasurehorde", help="Generates a treasure horde of type", action="store_true")

    parser.add_argument("-t", "--gentype", help="Specifies type of item, 'Scroll', 'Sword', or treasure type, 'A', 'B', etc")

    args = parser.parse_args()

    if args.magic:
        main("magic", args.gentype)
    elif args.treasurehorde:
        main('horde', args.gentype)
    else:
        main(None)