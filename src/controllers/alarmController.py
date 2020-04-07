import pygame
import os
from pathlib import Path

ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

pygame.mixer.init()
print(ROOT_DIR + "/resources/sounds/vent.wav")

mediumAlarm = pygame.mixer.Sound(ROOT_DIR + "/resources/sounds/vent.wav")
#highAlarm = pygame.mixer.Sound("alarm_high_priority.wav")

def playAlarm():

    if pygame.mixer.get_busy() == 1:
        pass
    else:
        pygame.time.wait(1000)
        mediumAlarm.play()

