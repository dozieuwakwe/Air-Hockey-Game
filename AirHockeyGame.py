import pygame  # Import the pygame module
import random  # Import random for random numbers

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

#Define colors needed
red = (255, 0, 0) 
red2 = (204, 0, 0)
blue = (0, 0, 128)
blue2 = (0, 0, 255)
blue3 = (0, 128, 255)
yellow = (255, 255, 153)
black = (0, 0, 0)

#Define fonts and button properties
def header(text, font):
    textSurface = font.render(text, True, yellow)
    return textSurface, textSurface.get_rect()

def header2(text, font):
    textSurface = font.render(text, True, blue3)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()     
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
        
    buttonfont = pygame.font.SysFont("times new roman",20)
    textSurf, textRect = header(msg, buttonfont)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((blue3))
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
        self.surf.fill((black))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(20, SCREEN_WIDTH-20), 10,
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
    
def game():
    screen.fill(blue3)
    global intro
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mainloop()
                
        headerfont = pygame.font.SysFont("arial black",75)
        TextSurf, TextRect = header("Air Hockey Game", headerfont)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/3))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        button("Start Game",150,450,125,50,blue,blue2,mainloop)
        button("Quit",550,450,100,50,red2,red,quitgame)

def mainloop():
    global player, ball, running
    player = Player()   # Instantiate player and ball
    ball = Ball()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(ball)
    clock = pygame.time.Clock()   # Setup the clock for a decent framerate
    
    running = True   # Variable to keep the main loop running
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_ESCAPE:  #Space bar and Escape buttons are used to pause the game
                    paused()
            elif event.type == QUIT:
                running = False
                pygame.quit()
                
        pressed_keys = pygame.key.get_pressed()    # Get the set of keys pressed and check for user input
        ball.update()  # Update ball position
        player.update(pressed_keys)  # Update the player sprite based on user keypresses
        screen.fill((yellow))   # Fill the screen with background color

        for entity in all_sprites:   # Draw all sprites
            screen.blit(entity.surf, entity.rect)
            
        if ball.rect.bottom>=SCREEN_HEIGHT:   #criteria for losing the game
            ball.kill()
            player.kill()
            gameover()

        pygame.display.flip()   # Update the display
        clock.tick(300)   # Ensure program maintains a rate of 300 frames per second
    
def paused():
    global pause
    pause=True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE):
                unpause()
    
        largeText = pygame.font.SysFont("arial black",75)
        TextSurf, TextRect = header2("Paused", largeText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/3))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        button("Continue",150,450,100,50,blue,blue2,unpause)
        button("Quit",550,450,100,50,red2,red,quitgame)
    
def unpause():
    global pause
    pause=False
    
def gameover():
    screen.fill(blue3)
    global lose
    lose=True
    while lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mainloop()
    
        largeText = pygame.font.SysFont("arial black",75)
        TextSurf, TextRect = header("Game Over!", largeText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/3))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        button("Restart Game",150,450,150,50,blue,blue2,mainloop)
        button("Quit",550,450,100,50,red2,red,quitgame)
    
def quitgame():
    global intro, pause, running, lose
    intro=False
    pause=False
    running=False
    lose=False

pygame.init()   # Initialize pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   # Create the screen object
pygame.display.set_caption('Air Hockey Game') 
game()
pygame.quit()