# universalisHistoryDataGenerator

This

# Running locally
Open your favorite terminal and `cd` to the repo where you want to run this script.
```
$ git clone https://github.com/Yuto3S/universalisHistoryDataGenerator
$ python -m main --should_fetch_new_items True
$ python -m
$ python -m main --server Twintania --should_calculate_shopping_lists True
$ python -m main --server Twintania,Alpha --should_calculate_shopping_lists True
```

https://universalis.app/api/v2/history/Twintania/36262,36246,36261,36630,36256,36245,36260,36244,36259,36257,36258,36255,36203,36243,36254,36253,36264,36242,27799,27800,27736,27756,27735,27852,27774,27773,27734,27851,27797,27733,27850,27732,27763,27764,20003,20004,27798

### Automated runs using launchctl & plist files
```
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
