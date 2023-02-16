# universalisHistoryDataGenerator

launchctl bootstrap gui/501 ffxiv.universalis.plist
launchctl kickstart gui/501/ffxiv.universalis
launchctl bootout gui/501/ffxiv.universalis


cat /tmp/ffxiv.universalis.out
cat /tmp/ffxiv.universalis.err

python /Users/hugues/PycharmProjects/gatheringOptiFFXIV/main.py --timeframe_hours 24 --push_to_git False