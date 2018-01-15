import pygame
import random
import os
from scapy.all import *

#Intialize pygame
pygame.init()

# Main loop will continue until done is True
done = False
# When true music will be played
playingMusic = False
# When true amazon dash buttton has been detected
detectedDash = False
# Index of current song being played (or that was just played)
currentSongIndex = 0
# How long in minutes to play music before auto stopping
sleepTime = 45
# When music starts playing
startTime = time.time()
# The MAC address of the amazon dash
MAC_ADDRESS = '78:e1:03:41:6e:65'

# Initialize the sound
pygame.mixer.init()
# Grab a reference to the music channel
musicChannel = pygame.mixer.music

# List to hold music file paths
musicLibrary = []
# Loop through every file in the Music folder
for file in os.listdir("Music"):
	# If the file is a MP3
	if file.endswith(".mp3"):
		# Print that the music is being loaded
		print("Loading Music/" + file)
		# Add music path to the list
		musicLibrary.append("Music/" + file)

# Randomize the list of music
random.shuffle(musicLibrary)

# A callback function to listen for the amazon dash button
# This function is called whenever a packet is sniffed (After filtered)
def detect_button(pkt):
	# If the packet has DHCP layer
	if pkt.haslayer(DHCP):
		# If the packet's source is the amazon dash button
		if pkt[Ether].src == MAC_ADDRESS:
			# Notify that the button was detected
                        print 'Button detected'
			global detectedDash
			detectedDash = True

# Loop while not done
while not done:
    # Listen to traffic
    sniff(prn = detect_button, filter="(udp and (port 67 or68))", store=0, count=1)
    # If the button was detected by the callback function
    if detectedDash:
	print "Button was pressed"
	# Set detection to false
	detectedDash = False
	# Toggle the state of playing music
	playingMusic = not playingMusic
	# Set the start time for sleeping
        startTime = time.time()  
    # If music should not be playing and music is playing
    if not playingMusic and musicChannel.get_busy():
	# Stop playing music
	print "Stopping Music"
        musicChannel.stop()
    # If music should be playing
    if playingMusic:
	# Check the current time
        currentTime = time.time()
	# If the sleepTime is nonzero check to see if it has been extended if so...
        if (sleepTime != 0) and (currentTime - startTime > 60 * sleepTime):
		# Get ready to stop playing music
                print "Sleep timer was exceeded. Going to sleep."
                playingMusic = False
	# If no music is being played
	if not musicChannel.get_busy():
	        # Look at the next song
		currentSongIndex+=1
		# Check that you were not already at the last song and if you were
		if currentSongIndex > len(musicLibrary):
			#Shuffle the song list and startover
			print "Reached end of song list"
			currentSongIndex = 0
                        print "Shuffling songs"
                        random.shuffle(musicLibrary)
		# Load the next song and start playing it
		else:
			print "Starting Song: " + musicLibrary[currentSongIndex-1]
        		musicChannel.load(musicLibrary[currentSongIndex-1])
			musicChannel.play()
    # If pygame has an event of QUIT stop the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Drop past events
    pygame.event.pump()
