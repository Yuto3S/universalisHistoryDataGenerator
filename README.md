# universalisHistoryDataGenerator
This project contains multiple scripts that when combined together will generate the history (over 1 or 7 days) trends for specific items for the MMORPG Final Fantasy XIV.

These trends are currently output as JSON files, and another project [universalisHistoryData](https://github.com/Yuto3S/universalisHistoryData) takes care of displaying them.
The live version is available at [https://yuto3s.github.io/universalisHistoryData/](https://yuto3s.github.io/universalisHistoryData/)

You can develop your own parser (web, script) to analyze those files. You can see how they look like by picking a specific day in [github - universalisHistoryDataGenerator - Twintania](https://github.com/Yuto3S/universalisHistoryDataGenerator/tree/main/assets/generated/history/Twintania/24). When I first started this project, I used to display transform the output into CSV to display in [google sheet.](https://docs.google.com/spreadsheets/d/1QRfrvx8pSWnRNhblzwumoaP6sD8IzEloLGzKM8DhOGs/edit#gid=1995563425)
# How to running locally
Open your favorite terminal and `cd` to the repo where you want to run this script.
```
$ git clone https://github.com/Yuto3S/universalisHistoryDataGenerator
$ cd universalisHistoryDataGenerator
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```
You can run the script manually with `python -m main` but nothing will happen because it will be lacking command line parameters.

Before delving into the command line parameters, let's explain how the

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
$ python -m main --generate_new_shopping_lists True --specific_shopping_list venture_botany
$ python -m main --server Twintania --calculate_shopping_lists True
$ python -m main --calculate_shopping_lists True --push_to_git True
$ python -m main --calculate_shopping_lists True --generate_new_shopping_lists True --servers Twintania --fetch_new_items True
```


https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ
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

# See status of the processes
launchctl list | egrep "xiv|PID"
```

### Error files
```
cat /tmp/ffxiv.universalis.24.out
cat /tmp/ffxiv.universalis.24.err
tail -f /tmp/ffxiv.universalis.24.out
tail -f /tmp/ffxiv.universalis.24.err

cat /tmp/ffxiv.universalis.168.out
cat /tmp/ffxiv.universalis.168.err
tail -f /tmp/ffxiv.universalis.168.out
tail -f /tmp/ffxiv.universalis.168.err
```
