import pygame
import os

WIDTH, HEIGHT = 900,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Little Monkey')

WHITE=(255,255,255)

FPS = 60

MONKEY = pygame.image.load(os.path.join('images','littlemonkey.png'))
MONKEY = pygame.transform.scale(MONKEY, (270,300))

def draw_window():
    WIN.fill((WHITE))
    WIN.blit(MONKEY, (300,220))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()

