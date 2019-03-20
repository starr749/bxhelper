# bxhelper
D&amp;D B/X utility

## Some quick scripts that make running Moldvay Basic a little easier

### rollcharacter.py
usage: rollcharacter.py [-h] [-hero] [-f FILEPATH]

optional arguments:
  -h, --help            show this help message and exit
  -hero, --heroic       Rolls stats with 4d6 drop lowest instead of flat 3d6
  -f FILEPATH, --filepath FILEPATH, --file FILEPATH
                        Do not roll stats, instead load attribute stats from
                        json file

This script rolls up a character using 3d6 (or optionally 4d6 drop lowest with the optional -h flag) and lists out modifiers, and potential XP bonuses.
It loads data and pulls in modifier text, class metadata, etc from the general/data/character directory.

If you have a stat block in Json in the following format:
```json
{
  "Strength": 18,
  "Intelligence": 18,
  "Wisdom": 18,
  "Dexterity": 18,
  "Constitution": 18,
  "Charisma": 18
}
```
You can load that file in and use those stats instead of loading them with one of the (-f [File], --filepath [File], --file [File]) args.
For example, to load the sample character in the general/data/character directory:
`rollcharacter.py -f data/character/sample_character.json`

### encounter.py
usage: encounter.py [-h] [-f FILE] [-r] [-rt] [-et]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Load Encounter Table from JSON File instead of the
                        leveled encounter tables in the book.
  -r, --reaction        Make a Monster reaction roll
  -rt, --reactiontable  Prints the Reaction Table
  -et, --encountertable
                        Prints the Reaction Table


Running encounter.py will prompt you for the basic questions before rolling on an encounter table.
Level prompt refers to the level of encounter (levels 1-3 as contained in Moldvay Basic) and will roll on that corresponding table.
You can load a custom table given it matches the format of the current JSON files (found in general/data/encounters)

The -r flag will roll make a reaction roll after taking in modifiers.

The -rt and -et flags will print out the loaded reaction and encounter tables, respectively 
