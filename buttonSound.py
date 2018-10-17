import pygame
import random
import os
import RPi.GPIO as GPIO
from scapy.all import *

# Intialize pygame
pygame.init()

# Setup GPIO for wired button detection
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# The state of the last wired button press
lastInput = True


# Main loop will continue until done is True
done = False
# When true music will be played
playingMusic = False
# When true amazon dash or wire button has been detected
detectedButton = False
# Index of current song being played (or that was just played)
currentSongIndex = 0
# How long in minutes to play music before auto stopping
sleepTime = 45
# When music starts playing
startTime = time.time()

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

print 'All music loaded'

# Randomize the list of music
random.shuffle(musicLibrary)

print 'Music shuffled. Ready to play'

# This function checks if the push button from ground to pin 18 is pressed
def detect_wireButton():
	global lastInput
	# Get the state of the button
	input_state = GPIO.input(18)
	# Check if the button is pressed but only execute if the last time was not a press
	# This is to keep from getting issues with one press registering as multiple.
	if input_state == False and lastInput != False:
		print 'Wired Button detected'
		global detectedButton
		detectedButton = True
	# Store the current state for the next check
	lastInput = input_state
		
	

# Loop while not done
while not done:
    # Listen to traffic
    detect_wireButton()
    # If the button was detected by either the wired or dash button
    if detectedButton:
	print 'Swapping state of music'
	# Set detection to false
	detectedButton = False
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
