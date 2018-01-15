# Remote Sound

## About
Remote Sound is an application that listens in for network traffic
from an Amazon Dash button. Upon detection the application will begin
playing or stopping music. The original design was to use this application
to play music in my son's room with the click of a button.

## Setup
### Dependences
* pygame - for music
* random - for shuffling the playlist
* os     - for locating music files
* scapy  - for detecting Amazon Dash

### Modifications
* Create a folder called Music
* Add mp3 files you want to add to the library
* Change MAC_ADDRESS to your Amazon Dash button's MAC address
* Change sleepTime to how many minutes you want music to play before going to stopping (0 for no sleeping)

## Future Ideas
* Add a way to exit the application smoothly
* A GUI to allow modification while the program is running
* Option for autoplay if a mircophone picks up a loud sound (e.g. crying)
* Option for autoplay if a PIR sensor detects movement