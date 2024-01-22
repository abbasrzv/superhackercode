import pygame
import os

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Pet():
    def __init__(self):
        self.hunger = 100
        self.hunger_decrease_rate = 1
        self.last_update_time = pygame.time.get_ticks()
        self.money = 0
        self.money_increase_rate = 1
        self.last_money_update_time = pygame.time.get_ticks()
        self.price_banana = 10  # Added price attribute for the banana

    def feed(self):
        if self.money >= self.price_banana:  # Check if there is enough money to buy the banana
            self.hunger += 10
            if self.hunger > 100:
                self.hunger = 100
            self.money -= self.price_banana  # Deduct the cost of the banana

    def update_hunger(self):
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_update_time

        if time_elapsed >= 5000:
            self.hunger -= self.hunger_decrease_rate
            if self.hunger < 0:
                self.hunger = 0
            self.last_update_time = current_time

    def update_money(self):
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_money_update_time

        if time_elapsed >= 1000:
            self.money += self.money_increase_rate
            self.last_money_update_time = current_time

    def draw_money_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Money: {self.money}', True, (0, 255, 0))
        text_rect = text.get_rect(topleft=(50, 20))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (50, 20))

    def draw_hunger_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Hunger: {self.hunger}', True, (255, 0, 255))
        text_rect = text.get_rect(topleft=(50, 70))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (50, 70))

# Function to draw the main game window
def draw_window():
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(MONKEY, (300, 220))
    player_pet.draw_money_text()
    player_pet.draw_hunger_text()
    if shop_button.draw():
        show_shop_screen()
    pygame.display.update()

# Function to draw the shop screen
def show_shop_screen():
    run_shop_screen = True

    while run_shop_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_shop_screen = False

        WIN.fill((255, 255, 255))

        # Draw banana button on the shop screen with price
        if food_button.draw():
            player_pet.feed()

        font = pygame.font.Font(None, 24)
        price_text = font.render(f'Cost: {player_pet.price_banana}', True, (0, 0, 0))
        WIN.blit(price_text, (25, 380))

        # Draw description text under the banana
        description_text = font.render("Restores 10 hunger", True, (0, 0, 0))
        WIN.blit(description_text, (0, 500))

        # Draw back button on the shop screen
        if back_button.draw():
            run_shop_screen = False

        pygame.display.update()

# Main game loop
def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player_pet.update_hunger()
        player_pet.update_money()
        draw_window()

    cleanup()

# Cleanup function to handle quitting Pygame
def cleanup():
    if pygame.get_init():
        pygame.quit()

if __name__ == "__main__":
    pygame.init()
#game window
    WIDTH, HEIGHT = 900, 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('My Little Monkey')

    FPS = 60
# images
    BACKGROUND = pygame.image.load(os.path.join('images', 'jungle.png'))
    BACKGROUND = pygame.transform.scale(BACKGROUND, (900, 600))
    MONKEY = pygame.image.load(os.path.join('images', 'littlemonkey.png'))
    MONKEY = pygame.transform.scale(MONKEY, (270, 300))
    SHOP = pygame.image.load(os.path.join('images', 'itemshop.png'))
    SHOP = pygame.transform.scale(SHOP, (180, 90))
    BACKBUTTON = pygame.image.load(os.path.join('images', 'backbutton.png'))
    BACKBUTTON = pygame.transform.scale(BACKBUTTON, (180, 90))
    BANANA = pygame.image.load(os.path.join('images', 'bananas.png'))
    BANANA = pygame.transform.scale(BANANA, (100, 100))
#buttons
    shop_button = Button(700, 500, SHOP)
    back_button = Button(20, 20, BACKBUTTON)
    food_button = Button(0, 400, BANANA)

    player_pet = Pet()

    main()
