# universalisHistoryDataGenerator

launchctl bootstrap gui/501 ffxiv.universalis.plist
launchctl kickstart gui/501/ffxiv.universalis
launchctl bootout gui/501/ffxiv.universalis

launchctl bootout gui/501/ffxiv.universalis && launchctl bootstrap gui/501 ffxiv.universalis.plist && launchctl kickstart gui/501/ffxiv.universalis

cat /tmp/ffxiv.universalis.out
cat /tmp/ffxiv.universalis.err