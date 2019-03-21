import dice, json, argparse, texttable as tt
from collections import OrderedDict
from treasure.magic_item import MagicItem


def main(item, item_type=None):
    if item == 'magic':
        mag = MagicItem(item_type)
        print("{0}: {1}".format(mag.item_type, mag.item_description))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--magic", help="Generates magic item", action="store_true")
    parser.add_argument("-t", "--itemtype", help="Specifies type of item, 'Scroll', 'Sword', etc")

    args = parser.parse_args()

    if args.magic:
        main("magic", args.itemtype)
    else:
        main(None)