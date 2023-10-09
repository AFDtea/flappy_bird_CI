import pygame
from pygame.locals import *
import sys

import random

pygame.init()


# reset
# reward
# play (action) -> jump
# game iteration
# is_collision

class FlappyGame:
    def __init__(self, w=600, h=500):
        self.w = w
        self.h = h
        self.playerMidPos = 0
        self.pipeMidPos = 0
        self.horizontal = 0
        self.vertical = 0
        self.pipe = [{'x': 0, 'y': 0}]
        self.bird_flapped = False
        self.score = 0
        self.ground = 0
        self.mytempheight = 100
        self.pipeVelX = 0
        self.bird_velocity_y = 0
        self.bird_Max_Vel_Y = 0   
        self.birdAccY = 0
        self.up_pipes = [{'x': 0, 'y': 0}]
        self.down_pipes = [{'x': 0, 'y': 0}]        
        self.bird_flap_velocity = 0


        self.screen = pygame.display.set_mode((self.w,self.h))
        self.elevation = self.h * .8

        self.FPS = 32
        self.FramePerSec = pygame.time.Clock()

        # Images
        wallimage = "Images/pipe.png"
        backgroundimage = "Images/sky.png"
        birdimage = "Images/bird_pic.png"
        sealevelimage = "Images/grass.png"
        self.game_images = {}

        pygame.display.set_caption("Flappy Bird")

        # Loading in number images for score
        self.game_images['scoreimages'] = (
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
        self.game_images['flappybird'] = pygame.image.load(birdimage).convert_alpha() 
        self.game_images['flappybird'] = pygame.transform.scale(self.game_images["flappybird"], (70,50))          
        self.game_images['sea_level'] = pygame.image.load(sealevelimage).convert_alpha()
        self.game_images['sea_level'] = pygame.transform.scale(self.game_images["sea_level"], (self.w,self.h/2))  
        self.game_images['background'] = pygame.image.load(backgroundimage).convert_alpha()
        self.game_images['background'] = pygame.transform.scale(self.game_images["background"], (self.w,self.h/1.25))  
        self.game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(wallimage)
                                                        .convert_alpha(), 180),
                                pygame.image.load(wallimage).convert_alpha())
        self.game_images['pipeimage'] = pygame.transform.scale(self.game_images["pipeimage"][0], (85,300)), pygame.transform.scale(self.game_images["pipeimage"][1], (85,300))

    
    # Method to setup and run the game
    def play_step(self, action):
        # Handling the key pressing events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Flapping when space or up is pressed
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                action = 1

        if(action == 1):
            if self.vertical > 0:
                    self.bird_velocity_y = self.bird_flap_velocity
                    self.bird_flapped = True

        # Exiting the loop if the game is over
        g_over = False
        reward = 0
        if self.isGameOver(self.horizontal, self.vertical, self.up_pipes, self.down_pipes):
            g_over = True
            self.reset()
            reward = -100
            return reward, g_over, self.score

        # check for your_score
        self.playerMidPos = self.horizontal + self.game_images['flappybird'].get_width()/2
        for pipe in self.up_pipes:
            self.pipeMidPos = pipe['x'] + self.game_images['pipeimage'][0].get_width()/2
            if self.pipeMidPos <= self.playerMidPos < self.pipeMidPos + (self.pipeVelX * -1):
                # Printing the score
                self.score += 1
                reward = 100
                if self.score >= 10:
                    self.pipeVelX = -12
                elif self.score >= 8:
                    self.pipeVelX = -10
                elif self.score >= 5:
                    self.pipeVelX = -8
                elif self.score >= 3:
                    self.pipeVelX = -6

        # Down velocity if bird not flapped
        #if self.bird_velocity_y < self.bird_Max_Vel_Y and not self.bird_flapped:
        if not self.bird_flapped:
            self.bird_velocity_y += self.birdAccY

        if self.bird_flapped:
            self.bird_flapped = False
        # Updating bird height
        playerHeight = self.game_images['flappybird'].get_height()
        self.vertical = self.vertical + min(self.bird_velocity_y, self.elevation - self.vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(self.up_pipes, self.down_pipes):
            upperPipe['x'] += self.pipeVelX
            lowerPipe['x'] += self.pipeVelX

        # Add a new pipe when the first is about
        # to cross the leftmost part of the screen
        if 240 < self.up_pipes[0]['x'] < (self.pipeVelX  * -1) + 241:
            reward = reward + 100
            newpipe = self.createPipe()
            self.up_pipes.append(newpipe[0])
            self.down_pipes.append(newpipe[1 ])

        # if the pipe is out of the screen, remove it
        if self.up_pipes[0]['x'] < -self.game_images['pipeimage'][0].get_width():
            self.up_pipes.pop(0)
            self.down_pipes.pop(0)

        self.update_ui()  

        return 10, g_over, self.score
    
    def reset(self):
        # Initializing variables for game and bird
        self.score = 0
        self.horizontal = int(self.w/5)
        self.vertical = int(self.w/2)
        self.ground = 0
        self.mytempheight = 100

        self.pipeVelX = -4 #pipe velocity along x
 
        self.bird_velocity_y = -9  # bird velocity
        self.bird_Max_Vel_Y = 10   
        self.birdAccY = 1
        
        # velocity while flapping
        self.bird_flap_velocity = -8
        
        # It is true only when the bird is flapping
        self.bird_flapped = False

        # Generating pipe for blitting on screen
        first_pipe = self.createPipe()
    
        # List containing lower pipes
        self.down_pipes = [
            {'x': self.w+240-self.mytempheight,
            'y': first_pipe[1]['y']}
        ]
    
        # List Containing upper pipes 
        self.up_pipes = [ 
            {'x': self.w+240-self.mytempheight,
            'y': first_pipe[0]['y']}
        ]  

    def createPipe(self):
        offset = self.h/3.5
        pipeHeight = self.game_images['pipeimage'][0].get_height()
        
        # generating random height of pipes
        y2 = offset + random.randrange(
        0, int(self.h - self.game_images['sea_level'].get_height() - 1.1 * offset))  
        pipeX = self.w + 10
        y1 = pipeHeight - y2 + offset 
        pipe = [
            
            # upper Pipe
            {'x': pipeX, 'y': -y1},
            
            # lower Pipe
            {'x': pipeX, 'y': y2}  
        ]
        return pipe
    
    # Checking if bird is above the sealevel.
    def isGameOver(self, horizontal, vertical, up_pipes, down_pipes):
        if vertical >= self.elevation - 50 or vertical < 0: 
            return True
    
        # Checking if bird hits the upper pipe
        for pipe in up_pipes:    
            pipeHeight = self.game_images['pipeimage'][0].get_height()
            if(vertical < pipeHeight + pipe['y'] 
            and abs(horizontal - pipe['x']) < self.game_images['pipeimage'][0].get_width()):
                return True
                
        # Checking if bird hits the lower pipe
        for pipe in down_pipes:
            if (vertical + self.game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < self.game_images['pipeimage'][0].get_width():
                return True
        return False

    def update_ui(self):
         # Blitting game images
        self.screen.blit(self.game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(self.up_pipes, self.down_pipes):
            self.screen.blit(self.game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            self.screen.blit(self.game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
            
        self.screen.blit(self.game_images['flappybird'], (self.horizontal, self.vertical))
        self.screen.blit(self.game_images['sea_level'], (0, self.elevation))

        # Fetching the digits of score
        numbers = [int(x) for x in list(str(self.score))]
        width = 0
         
        # finding the width of score images from numbers
        for num in numbers:
            width += self.game_images['scoreimages'][num].get_width()
        Xoffset = (self.w - width)/1.05
        
        # Blitting number images
        for num in numbers:
            self.screen.blit(self.game_images['scoreimages'][num], (Xoffset, self.w*0.02))
            Xoffset += self.game_images['scoreimages'][num].get_width()
        
        # Refresh the screen
        pygame.display.update()  

        self.FramePerSec.tick(self.FPS)

    def update_bird_ui(self):
        # sets the coordinates of bird
        horizontal = int(self.w/5)
        vertical = int((self.h - self.game_images['flappybird'].get_height())/2)

        ground = 0

        self.screen.blit(self.game_images['background'], (0, 0))
        self.screen.blit(self.game_images['flappybird'], (horizontal, vertical))
        self.screen.blit(self.game_images['sea_level'], (ground, self.elevation))
        
        # Refresh the screen
        pygame.display.update()

        self.FramePerSec.tick(self.FPS)

if __name__ == "__main__":
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    game = FlappyGame()

    while True:
        for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Flapping when space or up is pressed
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    game.reset()
                    while True:
                        reward, game_over, score = game.play_step()

                        if game_over == True:
                            break
                else:
                    game.update_bird_ui()


    

    #print('Final Score', score)    