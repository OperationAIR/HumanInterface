import pygame

pygame.mixer.init()

mediumAlarm = pygame.mixer.Sound("/home/pi/Desktop/ProjectAIR/HumanInterface/alarm_medium_priority.wav")
highAlarm = pygame.mixer.Sound("alarm_high_priority.wav")

def playAlarm():

    if mediumAlarm.get_busy() == 1:
        pass
    else:
        mediumAlarm.play()
