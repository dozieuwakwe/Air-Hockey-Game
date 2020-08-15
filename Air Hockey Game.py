# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 128, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT))

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
                
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
                    
# Define the ball object
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(1, SCREEN_WIDTH-1), 10,
            )
        )
        self.speed=1
        self.speedx=random.randint(-2,2)
    
    #The ball bounces off the player and wall surfaces
    #It may change speed/direction when it hits the top of the screen
    def update(self):
        if self.rect.bottom==player.rect.top and self.rect.centerx>=player.rect.left and self.rect.centerx<=player.rect.right:
            self.speed=-self.speed
        elif self.rect.top<=0:    
            self.speed=-self.speed
            self.speedx=random.randint(-3,3)
            
        if self.rect.left<=0 or self.rect.right>= SCREEN_WIDTH:
            self.speedx=-self.speedx
            
        if self.rect.bottom>player.rect.top and (self.rect.left==player.rect.right or self.rect.right==player.rect.left):
            self.speedx=-self.speedx
        
        self.rect.move_ip(self.speedx, self.speed)
            
# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player and ball
player = Player()
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

# Variable to keep the main loop running
running = True

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False    
            # The game is paused and unpaused using the space bar key 
            elif event.key == K_SPACE:
                while True:
                    event = pygame.event.wait()    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        break
        
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
 
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    
    # Update ball position
    ball.update()
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Fill the screen with background color
    screen.fill((255, 255, 153))
    
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    if ball.rect.bottom>=SCREEN_HEIGHT:
        ball.kill()
        player.kill()
        running = False
    
    # Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 300 frames per second
    clock.tick(300)
    
pygame.quit()
