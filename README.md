# universalisHistoryDataGenerator

This

# Running locally
Open your favorite terminal and `cd` to the repo where you want to run this script.
```
$ git clone https://github.com/Yuto3S/universalisHistoryDataGenerator
$ cd universalisHistoryDataGenerator
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

You can run the script manually with `python -m main` but nothing will happen because it will be lacking command line parameters.

## Command line parameters
- `--calculate_shopping_lists`
  - defaults `False`.
  - `True` as input will iterate over the available shopping lists manually written in _"assets/manual_input/shopping_list"_ and will generate the matching enriched files.
- `--fetch_new_items`
  - defaults `False`
  - `True` will generate a new version of _"assets/generated/config/all_items_name_to_id.json"_. This is usually required when new items are introduced into the game, for example after a patch.
- `--generate_new_shopping_lists`
  - defaults `False`
  - `True` will generate a new version of all the shopping_lists inside _"assets/generated/shopping_list"_ which should be done when the corresponding manual files are modified to track new items.
- `--push_to_git`
  - defaults `False`
  - `True` in combination with `calculate_shopping_lists`, this will push the new history trends to git so the front-end can display them.
- `--servers`
  - defaults `Alpha,Lich,Odin,Phoenix,Raiden,Shiva,Twintania,Zodiark`
  - specifies for which servers we should calculate the shopping_lists history trends. Can be a single argument `Twintania` or multiple servers `Twintania, Alpha`
- `--specific_shopping_list`
  - defaults `all`
  - specifies if we should only calculate the trends on a specific shopping_list. By default the script will run on all of them.
- `--timeframe_hours`
  - defaults `24`.
  - Takes a parameter from one of `1`, `24` or `168`, and specifies on how long a timeframe we should calculate the trends.

Examples:
```
$ python -m main --fetch_new_items True
$ python -m main --generate_new_shopping_lists True
$ python -m main --server Twintania --calculate_shopping_lists True
$ python -m main --calculate_shopping_lists True --push_to_git True
$ python -m main --calculate_shopping_lists True --generate_new_shopping_lists True --servers Twintania --fetch_new_items True
```

https://universalis.app/api/v2/history/Twintania/36262,36246,36261,36630,36256,36245,36260,36244,36259,36257,36258,36255,36203,36243,36254,36253,36264,36242,27799,27800,27736,27756,27735,27852,27774,27773,27734,27851,27797,27733,27850,27732,27763,27764,20003,20004,27798

# Automated runs using launchctl & plist files
```
~/Library/LaunchAgents$ cat ffxiv.universalis.24.plist

cd ~/Library/LaunchAgents

launchctl bootstrap gui/501 ffxiv.universalis.plist
# Starts a run outside of scheduled runs
launchctl kickstart gui/501/ffxiv.universalis
launchctl bootout gui/501/ffxiv.universalis

launchctl bootout gui/501/ffxiv.universalis.24 && launchctl bootstrap gui/501 ffxiv.universalis.24.plist && launchctl kickstart gui/501/ffxiv.universalis.24
launchctl bootout gui/501/ffxiv.universalis.168 && launchctl bootstrap gui/501 ffxiv.universalis.168.plist && launchctl kickstart gui/501/ffxiv.universalis.168
```

### Error files
```
cat /tmp/ffxiv.universalis.24.out
cat /tmp/ffxiv.universalis.24.err

cat /tmp/ffxiv.universalis.168.out
cat /tmp/ffxiv.universalis.168.err
```
