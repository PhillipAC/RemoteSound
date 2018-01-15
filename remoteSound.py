import pygame
import random
import os
from scapy.all import *

pygame.init()

done = False
playingMusic = False
detectedDash = False
currentSongIndex = 0
sleepTime = 45
startTime = time.time()
MAC_ADDRESS = '78:e1:03:41:6e:65'

pygame.mixer.init()

musicLibrary = []
for file in os.listdir("Music"):
	if file.endswith(".mp3"):
		print("Loading Music/" + file)
		musicLibrary.append("Music/" + file)

musicChannel = pygame.mixer.music

def detect_button(pkt):
	if pkt.haslayer(DHCP):
		if pkt[Ether].src == MAC_ADDRESS:
                        print 'Button detected'
			global detectedDash
			detectedDash = True

while not done:
    sniff(prn = detect_button, filter="(udp and (port 67 or68))", store=0, count=1)
    if detectedDash:
	print "Button was pressed"
	detectedDash = False
	playingMusic = not playingMusic
        startTime = time.time()  
    if not playingMusic and musicChannel.get_busy():
	print "Stopping Music"
        musicChannel.stop()
    if playingMusic:
        currentTime = time.time()
        if (sleepTime != 0) and (currentTime - startTime > 1000 * 60 * sleepTime):
                playingMusic = False
	if not musicChannel.get_busy():
		currentSongIndex+=1
		if currentSongIndex > len(musicLibrary):
			print "Reached end of song list"
			currentSongIndex = 0
                        print "Shuffling songs"
                        random.shuffle(musicLibrary)
		else:
			print "Starting Song: " + musicLibrary[currentSongIndex-1]
        		musicChannel.load(musicLibrary[currentSongIndex-1])
			musicChannel.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = True
    pygame.event.pump()
