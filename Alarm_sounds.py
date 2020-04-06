import pygame


pygame.mixer.init()

mediumAlarm = pygame.mixer.Sound("/home/pi/Desktop/ProjectAIR/HumanInterface/vent.wav")
#highAlarm = pygame.mixer.Sound("alarm_high_priority.wav")

def playAlarm():

    if pygame.mixer.get_busy() == 1:
        pass
    else:
        pygame.time.wait(1000)
        mediumAlarm.play()

