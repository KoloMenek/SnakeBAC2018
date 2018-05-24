###IMPORTS
import pygame
import time
import random
from math import sqrt
pygame.init()
pygame.mixer.init()
###DISPLAY
display_width = 1280
display_height = 960
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')
###Sounds
pygame.mixer.music.load("son.wav")
pygame.mixer.music.play(-1)
bip_sound = pygame.mixer.Sound("bip.wav")
death_sound = pygame.mixer.Sound("end.wav")
###COLORS
black = (0,0,0)
green = (15, 75, 4)
white = (0,0,0)
Green_light = (31, 133, 11)
###TIME
clock = pygame.time.Clock()
###IMAGES
background = pygame.image.load('background.png')
snakeImg = pygame.image.load('head.jpg')
pointImg = pygame.image.load('point.jpg')
corpsImg = pygame.image.load('body.jpg')
###VARIABLES
snake_width = 40 
points_width = 10
best_score = 0
highest_score1 = open("record_book.txt","r")
var = highest_score1.read()
highest_score1.close()
highest_score = int(var) if var.isdigit() else 0


def record_book(higher_score): ###Fonction qui affiche le record du jeu
    font = pygame.font.SysFont (None, 40)
    text = font.render("Record du jeu: "+str(higher_score), True, Green_light)
    gameDisplay.blit(text,(1025,0))

def affiche_best_score(best): ###Fonction qui affiche le meilleur score de la session
    font = pygame.font.SysFont (None, 40)
    text = font.render("Votre meilleur score: "+str(best), True, Green_light)
    gameDisplay.blit(text,(0,0))

def scoreboard(count): ###Fonction qui compte le nombre de points pendant une partie
    font = pygame.font.SysFont (None, 40)
    text = font.render("Points: "+str(count), True, Green_light)
    gameDisplay.blit(text,(0,30))

def points(posx,posy): ###Fonction qui permet de créer les points
    gameDisplay.blit(pointImg, (posx,posy))

def text_objects(text,font): ###Fonction qui créer une surface de text pour permettre la deuxième fonction message_display()
    TextSurface = font.render(text, True, black)
    return TextSurface, TextSurface.get_rect()

def message_display(text): ###Fonction qui permet à crash() d'écrire le message 
    LargeText = pygame.font.Font("freesansbold.ttf",50)
    TextSurface, TextRectangle = text_objects(text, LargeText)
    TextRectangle.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurface,TextRectangle)

def crash(score): ###Fonction qui stop le jeu quand on "crash" en écrivant le "vous avez perdu" + elle vérifie si le meilleur score de la session est meilleur que le record du jeu. Si c'est le cas, elle le change.
    global highest_score
    global best_score
    message_display("Vous avez perdu! Votre score: "+str(score))
    pygame.display.update()
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(death_sound)
    time.sleep(3.2)
    pygame.mixer.music.unpause()

    if highest_score < best_score:
        highest_score = best_score
        highest_score2 = open("record_book.txt","w")
        highest_score2.write(str(highest_score))
        highest_score2.close()

    game_start_screen()

def snake(snakeLength,List): ###Positionne le snake sur l'écran après avoir été importé
    gameDisplay.blit(snakeImg, (List[-1][0],List[-1][1]))
    for XandY in List[:-1]:
        gameDisplay.blit(corpsImg, (XandY[0],XandY[1],snake_width,snake_width))

def game_start_screen(): ###Fonction menu du jeu
    global best_score
    intro = True
    music_play = True
    pressed = False
    gameDisplay.blit(background, (0,0))
    affiche_best_score(best_score)
    record_book(highest_score)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
        
            if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
                mouse = pygame.mouse.get_pos()
                if 400 > mouse[0] > 0 and 960 > mouse[1] > 900 and event.button == 1 and music_play == True:   ###Gestion des boutons: Si les coordonnées X et Y de la souris se trouvent dans les emplacements et que la musique est allumée alors elle l'éteind
                    pygame.mixer.music.pause()
                    music_play = False
                elif 400 > mouse[0] > 0 and 960 > mouse[1] > 900 and event.button == 1 and music_play == False: ###Gestion des boutons: Si les coordonnées X et Y de la souris se trouvent dans les emplacements et que la musique est éteinte alors elle l'allume
                    pygame.mixer.music.unpause()
                    music_play = True
                elif 1070 > mouse[0] > 920 and 625 > mouse[1] > 575 and event.button == 1: ###Gestion des boutons: Si les coordonnées X et Y de la souris se trouvent dans les emplacements alors le jeu se lance
                    game_loop()
                pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and pressed == True: ###Une sécurité qui permet de limiter les cliques de la souris
                pressed = False
                time.sleep(0.05)

        pygame.display.update()
        clock.tick(60)

def game_loop(): ###Fonction qui est la base et la logique du jeu Tout se passe dans cette fonction
    ###On paramètre les variables
    global best_score
    x =  (display_width * 0.5)
    y = (display_height * 0.5)
    clock.tick(8)
    List=[]
    snakeLength = 1
    x_change = 0
    y_change = 0
    posx_start = random.randrange(30,display_width - points_width-20)
    posy_start = random.randrange(30,display_height-30)
    gameExit = False
    direction = 'start'
    score = 0
    
    while not gameExit: ###Permet de quiter le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break

            ############################ Déplacement du snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    y_change = 0
                    x_change = -40
                    direction = 'left'
                    break
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    y_change = 0
                    x_change = 40
                    direction = 'right'
                    break
                elif event.key == pygame.K_UP and direction !='down':
                    x_change = 0
                    y_change = -40
                    direction = 'up'
                    break
                elif event.key == pygame.K_DOWN and direction !='up':
                    x_change = 0
                    y_change = 40
                    direction ='down'
                    break    
            ############################
        
        x += x_change
        y += y_change
                 
        gameDisplay.fill(green)

        snakeHead = []
        snakeHead.append(x)
        snakeHead.append(y)
        List.append(snakeHead)

        if len(List) > snakeLength:
            del List[0]
        for partie in List[:-1]:
            if partie == snakeHead:
                crash(score)

        snake(snakeLength,List)
        affiche_best_score(best_score)
        record_book(highest_score)
        scoreboard(score)
        points(posx_start,posy_start)
        
        if best_score < score: ###Vérifie le score et augmente le meilleur score de la séssion si c'est le cas
            best_score = score

        if x > display_width - snake_width or x < 0 or y > display_height - snake_width or y < 0: ###Appel la fonction crash() si le snake sort de l'écran
            crash(score)
        if y < posy_start + points_width and y + snake_width > posy_start and x < posx_start + points_width and x + snake_width > posx_start: ###Si le snake mange un point, le point se met à un endroit différent et le score augmente ainsi que la longueur du serpent
            posx_start = random.randrange(30,display_width - points_width-20)
            posy_start = random.randrange(30,display_height-30)
            pygame.mixer.Sound.play(bip_sound)
            score += 1
            snakeLength +=1
        
        pygame.display.update()
        clock.tick(int(8 + sqrt(snakeLength))) ###Augmente la difficulté du jeu avec la vitesse. Plus le serpent est grand, plus le jeu sera rapide

game_start_screen()
pygame.quit()
quit()
