import pygame
import random
import time
import os
import sys
pygame.font.init()

current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "pachadi halne.jpg") # settin the background image path

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # setting the screen for gameplay with width and height
pygame.display.set_caption('Space Dodge')  # sets caption

BACKGROUND = pygame.transform.scale(pygame.image.load(image_path),(WIDTH, HEIGHT)) #loading the bg image (covers the
# screen)

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_VEL = 5 # player attributes

STAR_WIDTH = 20
STAR_HEIGHT = 10
STAR_VEL = 3

Font = pygame.font.SysFont('Comicsans', 30)


def draw(player, elapsed_time,stars):  # all the drawing or making happens here
    WIN.blit(BACKGROUND, (0, 0)) # drawing the bg image

    time_text = Font.render(f'Time:{round(float(elapsed_time),1)}s', 1, "white")
    WIN.blit(time_text,(10, 10))

    pygame.draw.rect(WIN, "red", player) #drawing rectangle

    for star in stars:
        pygame.draw.rect(WIN, 'white', star)

    pygame.display.update() # most code(updates the screen if not written all this is crap)

def main():
    clock = pygame.time.Clock() # creating a game clock
    start_time = time.time()
    elapsed_time = 0
    run = True

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    player = pygame.Rect(500,(HEIGHT - PLAYER_HEIGHT), PLAYER_WIDTH,PLAYER_HEIGHT) 

    while run:  # runnig while loop for holding the screen
        star_count += clock.tick(60) # slowing down the frames rate for good movement
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH- STAR_WIDTH)
                star = pygame.Rect(star_x,-STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200,star_add_increment-50)
            star_count = 0

        keys = pygame.key.get_pressed() # recording key presses and using it
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <=WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

            if hit:
                lost_text = Font.render("You lost!",1,"white")
                WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                score_text = Font.render(f'You lasted {elapsed_time}s',1,"white")
                WIN.blit(score_text,(WIDTH/2 - score_text.get_width()/2,(HEIGHT/2 - score_text.get_height()/2)+40))
                pygame.display.update()
                pygame.time.delay(4000)
                main()
                


        draw(player,elapsed_time,stars) # calling draw function(if not written all this is crap)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
