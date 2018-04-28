###IMPORTS
import pygame
import time
import random
from math import sqrt
pygame.init()
###IMPORTS
###DISPLAY
display_width = 1280
display_height = 960
###DISPLAY
###MUSIC
pygame.mixer.music.load("son.wav")
pygame.mixer.music.play()
###MUSIC
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')
###COLORS
black = (0,0,0)
white = (255,255,255)
green = (15, 75, 4)
Green_light = (31, 133, 11)
###COLORS
###TIME
clock = pygame.time.Clock()
###TIME
###IMAGES
background = pygame.image.load('background.png')
snakeImg = pygame.image.load('head.jpg')
pointImg = pygame.image.load('point.jpg')
corpsImg = pygame.image.load('body.jpg')
###IMAGES
###VARIABLES
snake_width = 40 
points_width = 10
###VARIABLES

def scoreboard(count): ###Fonction qui compte le nombre de points
    font = pygame.font.SysFont (None, 40)
    text = font.render("Points: "+str(count), True, Green_light)
    gameDisplay.blit(text,(0,0))


def points(posx,posy): ###Fonction qui créer les points
    gameDisplay.blit(pointImg, (posx,posy))


def crash(): ###Fonction qui stop le jeu quand on "crash" en écrivant le "vous avez perdu"
    message_display("Vous avez perdu!")


def text_objects(text,font): ###Fonction qui créer une surface de text pour permettre la deuxième fonction message_display()
    TextSurface = font.render(text, True, black)
    return TextSurface, TextSurface.get_rect()



def message_display(text): ###Fonction qui permet à crash() d'écrire le message et de relancer le jeu 
    LargeText = pygame.font.Font("freesansbold.ttf",50)
    TextSurface, TextRectangle = text_objects(text, LargeText)
    TextRectangle.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurface,TextRectangle)
    pygame.display.update()
    time.sleep(5)
    game_start_screen()




def snake(snakeLength,List): ###Positionne le snake sur l'écran après avoir été importé
    gameDisplay.blit(snakeImg, (List[-1][0],List[-1][1]))
    for XandY in List[:-1]:
        gameDisplay.blit(corpsImg, (XandY[0],XandY[1],snake_width,snake_width))
def game_start_screen(): ###Fonction qui fait le Menu quand on allume le jeu
    intro = True
    music_play = True
    pressed = False
    while intro:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            time.sleep(0.01)
            continue
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        gameDisplay.blit(background, (0,0))
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            if 400 > mouse[0] > 0 and 960 > mouse[1] > 900 and event.button == 1 and music_play == True:
                pygame.mixer.music.pause()
                music_play = False
            elif 400 > mouse[0] > 0 and 960 > mouse[1] > 900 and event.button == 1 and music_play == False:
                pygame.mixer.music.unpause()
                music_play = True
            elif 1070 > mouse[0] > 920 and 625 > mouse[1] > 575 and event.button == 1:
                game_loop()
            pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and pressed == True:
            pressed = False
            time.sleep(0.05)
    



        pygame.display.update()
        clock.tick(8)

def game_loop(): ###Fonction qui est la base et la logique du jeu

    x =  (display_width * 0.5)
    y = (display_height * 0.5)
    List=[]
    snakeLength = 1
    x_change = 0
    y_change = 0
    posx_start = random.randrange(30,display_width - points_width-20)
    posy_start = random.randrange(30,display_height-30)
    gameExit = False
    direction = 'start'
    score = 0
    

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            ############################ Déplacement du snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    y_change = 0
                    x_change = -40
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    y_change = 0
                    x_change = 40
                    direction = 'right'
                elif event.key == pygame.K_UP and direction !='down':
                    x_change = 0
                    y_change = -40
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction !='up':
                    x_change = 0
                    y_change = 40
                    direction ='down'
            
                
            ###########################
        ##
        x += x_change
        y += y_change
        ##         
        gameDisplay.fill(green)

        snakeHead = []
        snakeHead.append(x)
        snakeHead.append(y)
        List.append(snakeHead)

        if len(List) > snakeLength:
            del List[0]
        for partie in List[:-1]:
            if partie == snakeHead:
                crash()

        snake(snakeLength,List)

        scoreboard(score)
        points(posx_start,posy_start)
        if x > display_width - snake_width or x < 0 or y > display_height - snake_width or y < 0:
            crash()
        if y < posy_start + points_width and y + snake_width > posy_start and x < posx_start + points_width and x + snake_width > posx_start:
            posx_start = random.randrange(30,display_width - points_width-20)
            posy_start = random.randrange(30,display_height-30)
            score += 1
            snakeLength +=1
        

        pygame.display.update()
        clock.tick(int(8 + sqrt(sqrt(score))))

game_start_screen()
game_loop()
pygame.quit()
quit()
