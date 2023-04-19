# universalisHistoryDataGenerator

launchctl bootstrap gui/501 ffxiv.universalis.plist
launchctl kickstart gui/501/ffxiv.universalis
launchctl bootout gui/501/ffxiv.universalis

launchctl bootout gui/501/ffxiv.universalis && launchctl bootstrap gui/501 ffxiv.universalis.plist && launchctl kickstart gui/501/ffxiv.universalis
launchctl bootout gui/501/ffxiv.universalis.168 && launchctl bootstrap gui/501 ffxiv.universalis.168.plist && launchctl kickstart gui/501/ffxiv.universalis.168


cat /tmp/ffxiv.universalis.out
cat /tmp/ffxiv.universalis.err