# universalisHistoryDataGenerator

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