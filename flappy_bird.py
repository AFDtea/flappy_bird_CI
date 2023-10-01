import pygame
from pygame.locals import *
import sys

import random


pygame.init()

FPS = fcreat
FramePerSec = pygame.time.Clock()

# Images
wallimage = "Images/pipe.png"
backgroundimage = "Images/sky.png"
birdimage = "Images/bird_pic.png"
sealevelimage = "Images/grass.png"
game_images = {}

white = pygame.Color(255,255,255)

#Setting size of the screen
screen_width = 600
screen_height = 500

# Initializing the Screen
screen = pygame.display.set_mode((screen_width,screen_height))
elevation = screen_height * .8
screen.fill(white)

# Method to setup and run the game
def flappygame():
    # Initializing variables for game and bird
    your_score = 0
    horizontal = int(screen_width/5)
    vertical = int(screen_width/2)
    ground = 0
    mytempheight = 100
  
    # Generating pipe for blitting on screen
    first_pipe = createPipe()
    # second_pipe = createPipe()
  
    # List containing lower pipes
    down_pipes = [
        {'x': screen_width+300-mytempheight,
         'y': first_pipe[1]['y']},
        # {'x': screen_width+300-mytempheight+(screen_width/2),
        #  'y': second_pipe[1]['y']},
    ]
   
    # List Containing upper pipes 
    up_pipes = [ 
        {'x': screen_width+300-mytempheight,
         'y': first_pipe[0]['y']},
        # {'x': screen_width+300-mytempheight+(screen_width/2),
        #  'y': second_pipe[0]['y']},
    ]
  
    pipeVelX = -4 #pipe velocity along x

    bird_velocity_y = -9  # bird velocity
    bird_Max_Vel_Y = 10   
    # bird_Min_Vel_Y = -8
    birdAccY = 1
      
     # velocity while flapping
    bird_flap_velocity = -8
      
    # It is true only when the bird is flapping
    bird_flapped = False  
    while True:
         
        # Handling the key pressing events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Flapping when space or up is pressed
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True 
  
        # Exiting the loop if the game is over
        if isGameOver(horizontal, vertical, up_pipes, down_pipes):
            return
  
        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + (pipeVelX * -1):
                # Printing the score
                your_score += 1
                # print(f"Your your_score is {your_score}")
                if your_score >= 10:
                    pipeVelX = -12
                elif your_score >= 8:
                    pipeVelX = -10
                elif your_score >= 5:
                    pipeVelX = -8
                elif your_score >= 3:
                    pipeVelX = -6
  
        # Down velocity if bird not flapped
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        # Updating bird height
        playerHeight = game_images['flappybird'].get_height()
        print(vertical)
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)
  
        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
  
        # Add a new pipe when the first is about
        # to cross the leftmost part of the screen
        if 240 < up_pipes[0]['x'] < (pipeVelX  * -1) + 241:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1 ])
  
        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        # Blitting game images
        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            screen.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
  
        screen.blit(game_images['sea_level'], (ground, elevation))
        screen.blit(game_images['flappybird'], (horizontal, vertical))
          
        # Fetching the digits of score
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
          
        # finding the width of score images from numbers
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (screen_width - width)/1.05
          
        # Blitting number images
        for num in numbers:
            screen.blit(game_images['scoreimages'][num], (Xoffset, screen_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
              
        # Refreshing the game screen and displaying the score
        pygame.display.update()
          
        # Set the framepersecond
        FramePerSec.tick(FPS)

def createPipe():
    offset = screen_height/3.5
    pipeHeight = game_images['pipeimage'][0].get_height()
      
    # generating random height of pipes
    y2 = offset + random.randrange(
      0, int(screen_height - game_images['sea_level'].get_height() - 1.1 * offset))  
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset 
    pipe = [
        
        # upper Pipe
        {'x': pipeX, 'y': -y1},
        
          # lower Pipe
        {'x': pipeX, 'y': y2}  
    ]
    return pipe


# Checking if bird is above the sealevel.
def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical >= elevation - 50 or vertical < 0: 
        return True
  
    # Checking if bird hits the upper pipe
    for pipe in up_pipes:    
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] 
           and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
            
    # Checking if bird hits the lower pipe
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False


# Running the main method
if __name__ == "__main__":
    pygame.init()
    FramePerSec.tick(FPS)
    pygame.display.set_caption("Flappy Bird")

    # Loading in number images for score
    game_images['scoreimages'] = (
        pygame.transform.scale(pygame.image.load('Images/0.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/1.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/2.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/3.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/4.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/5.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/6.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/7.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/8.png').convert_alpha(), (40,40)),
        pygame.transform.scale(pygame.image.load('Images/9.png').convert_alpha(), (40,40))
    )

    # Loading in all other pictures for the game
    game_images['flappybird'] = pygame.image.load(birdimage).convert_alpha() 
    game_images['flappybird'] = pygame.transform.scale(game_images["flappybird"], (70,50))          
    game_images['sea_level'] = pygame.image.load(sealevelimage).convert_alpha()
    game_images['sea_level'] = pygame.transform.scale(game_images["sea_level"], (screen_width,screen_height/2))  
    game_images['background'] = pygame.image.load(backgroundimage).convert_alpha()
    game_images['background'] = pygame.transform.scale(game_images["background"], (screen_width,screen_height/1.25))  
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(wallimage)
                                                    .convert_alpha(), 180),
                            pygame.image.load(wallimage).convert_alpha())
    game_images['pipeimage'] = pygame.transform.scale(game_images["pipeimage"][0], (85,300)), pygame.transform.scale(game_images["pipeimage"][1], (85,300))

    # Potentially making the bird rotate up and down
    # bird_rect = game_images['flappybird'].get_rect()
    # bird_center = bird_rect.center
    # game_images['flappybird'] = pygame.transform.rotate(game_images['flappybird'], 20)

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    #Game loop starts
    while True:
        # sets the coordinates of bird
        horizontal = int(screen_width/5)
        vertical = int((screen_height - game_images['flappybird'].get_height())/2)

        ground = 0
        
        for event in pygame.event.get():
                if event.type ==  QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()
                
                # if user doesn't press any key nothing happens
                else:
                    screen.blit(game_images['background'], (0, 0))
                    #rotated_rect = game_images['flappybird'].get_rect(center=bird_center)
                    #screen.blit(game_images['flappybird'], rotated_rect.topleft)
                    screen.blit(game_images['flappybird'], (horizontal, vertical))
                    screen.blit(game_images['sea_level'], (ground, elevation))
                    
                    # Refresh the screen
                    pygame.display.update()        
                    
                    # set the frame rate
                    FramePerSec.tick(FPS)