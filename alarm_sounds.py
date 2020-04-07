import pygame
import os

pygame.mixer.init()

median_alarm_path = os.path.abspath('assets/medium_alarm.wav')
mediumAlarm = pygame.mixer.Sound(median_alarm_path)

def playAlarm():

    if pygame.mixer.get_busy() == 1:
        pass
    else:
        mediumAlarm.play()

