# ShortTux

(Under Construction. I just recently came up with this project, everything is buggy and ugly)

With ShortTux it is possible to connect Siri Shortcuts to Linux.


## How does it work?

The Shortcut script (will be uploaded soon) writes some changes to a .json-file in Dropbox. The python script monitors the directory and when it notices changes it automatically triggers some action.


## Example usages I came up so far:

- Automatically send a notification when Focus modes are triggered

- Shortcut switches light/dark mode on iOS and Ubuntu simulatneously

- Notify about battery level


## FAQ

Why Dropbox?

- It is the best integrated cloud service both in Shortcuts and Linux I could find

Why not ssh to run scripts?

- You would need to know the IP of your computer, if you want to automate your laptop this will be handy

## Installation

- Linux (under Ubuntu): the python script need watchdog: ```pip install watchdog```

- iOS: in the shortcuts app put in every script or automation a dictionary with a suited key and value (e.g. "focus":"work" or "battery":"20%") and feed it to the shortcut (will be uploaded shortly)