import pygame
import os

WIDTH, HEIGHT = 900, 600  

pygame.mixer.init()
pygame.mixer.set_num_channels(2)

class Button():
    def __init__(self, x, y, image, sound=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.sound = sound

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                if self.sound:
                    pygame.mixer.Channel(1).play(self.sound)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Pet():
    def __init__(self):
        self.hunger = 100
        self.hunger_decrease_rate = 1
        self.last_update_time = pygame.time.get_ticks()
        self.money = 1000000
        self.money_increase_rate = 1
        self.last_money_update_time = pygame.time.get_ticks()
        self.price_banana = 50
        self.has_medium_monkey = False
        self.has_big_monkey = False
        self.more_coins_multiplier = 100  
        self.more_coins_clicked = False  

    def feed(self):
        if self.money >= self.price_banana:
            self.hunger += 10
            if self.hunger > 100:
                self.hunger = 100
            self.money -= self.price_banana

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
            if self.more_coins_clicked:
                self.money += 1000  
            else:
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

    def draw_money_text_shop(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Money: {self.money}', True, (0, 255, 0))
        text_rect = text.get_rect(topright=(WIDTH - 50, 20))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (text_rect.x, text_rect.y))

    def draw_hunger_text_shop(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Hunger: {self.hunger}', True, (255, 0, 255))
        text_rect = text.get_rect(topright=(WIDTH - 50, 70))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (text_rect.x, text_rect.y))

# Function to draw the main game window
def draw_window():
    WIN.blit(BACKGROUND, (0, 0))

    
    if player_pet.has_big_monkey:
        monkey_button_big.draw()
    elif player_pet.has_medium_monkey:
        monkey_button_medium.draw()
    else:
        monkey_button.draw()

    player_pet.draw_money_text()
    player_pet.draw_hunger_text()

    # Check if the hunger is zero
    if player_pet.hunger == 0:
        font = pygame.font.Font(None, 72)
        text = font.render("Your monkey is DEAD", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(1000)
        cleanup()
        return

    if shop_button.draw():
        show_shop_screen()
    coin_button.draw()
    pygame.display.update()

# Function to draw the shop screen
def show_shop_screen():
    run_shop_screen = True
    cost_font = pygame.font.Font(None, 24)  
    description_font = pygame.font.Font(None, 24)  

    while run_shop_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_shop_screen = False

        WIN.blit(WOOD, (0, 0))

       
        player_pet.draw_money_text_shop()
        player_pet.draw_hunger_text_shop()

     
        player_pet.update_hunger()
        player_pet.update_money()

        
        if food_button.draw():
            player_pet.feed()

        font = pygame.font.Font(None, 24)
        price_text = font.render(f'Cost: {player_pet.price_banana}', True, (255, 255, 255))
        WIN.blit(price_text, (25, 380))

       
        description_text = font.render("Restores 10 hunger", True, (255, 255, 255))
        WIN.blit(description_text, (0, 500))

        
        if back_button.draw():
            run_shop_screen = False

        
        medium_monkey_image = pygame.transform.scale(MIDMONKEY, (100, 100))
        medium_monkey_button = Button(50, 200, medium_monkey_image)

        if medium_monkey_button.draw() and player_pet.money >= 10000 and not player_pet.has_medium_monkey:
            player_pet.money -= 10000  
            player_pet.has_medium_monkey = True  

            
        cost_text = cost_font.render(f'Cost: 10000', True, (255, 255, 255))
        WIN.blit(cost_text, (50, 175))

            
        description_text = description_font.render("Bigger Monkey", True, (255, 255, 255))
        WIN.blit(description_text, (50, 300))

        
        big_monkey_image = pygame.transform.scale(BIGMONKEY, (100, 100))
        big_monkey_button = Button(200, 200, big_monkey_image)

        if big_monkey_button.draw() and player_pet.money >= 100000 and not player_pet.has_big_monkey:
            player_pet.money -= 100000  
            player_pet.has_big_monkey = True  

          
        big_monkey_cost_text = cost_font.render(f'Cost: 100000', True, (255, 255, 255))
        WIN.blit(big_monkey_cost_text, (200, 175))

            
        big_monkey_description_text = description_font.render("Biggest Monkey", True, (255, 255, 255))
        WIN.blit(big_monkey_description_text, (200, 300))

        
        more_coins_image = pygame.transform.scale(MORECOINS, (100, 100))
        more_coins_button = Button(350, 200, more_coins_image)  

        if more_coins_button.draw() and player_pet.money >= 10000 and not player_pet.more_coins_clicked:
            player_pet.money -= 10000  
            player_pet.more_coins_clicked = True  
            player_pet.money_increase_rate *= player_pet.more_coins_multiplier  

        
        more_coins_cost_text = cost_font.render(f'Cost: 10000', True, (255, 255, 255))
        WIN.blit(more_coins_cost_text, (350, 175))

        
        more_coins_description_text = description_font.render("Increases money rate", True, (255, 255, 255))
        WIN.blit(more_coins_description_text, (350, 300))

     
        if back_button.draw():
            run_shop_screen = False

        pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            
            if coin_button.draw():
                if player_pet.more_coins_clicked:
                    player_pet.money += 1000  
                else:
                    player_pet.money += 10  

        player_pet.update_hunger()
        player_pet.update_money()
        draw_window()

    cleanup()

# Cleanup function to handle quitting Pygame
def cleanup():
    if pygame.get_init():
        pygame.quit()

# Game window 
if __name__ == "__main__":
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('My Little Monkey')

    FPS = 60
    BACKGROUND = pygame.image.load(os.path.join('images', 'jungle.png'))
    BACKGROUND = pygame.transform.scale(BACKGROUND, (900, 600))
    MONKEY = pygame.image.load(os.path.join('images', 'littlemonkey.png'))
    MONKEY = pygame.transform.scale(MONKEY, (270, 300))
    MIDMONKEY = pygame.image.load(os.path.join('images', 'mediummonkey.png'))
    MIDMONKEY = pygame.transform.scale(MIDMONKEY, (270, 300))
    BIGMONKEY = pygame.image.load(os.path.join('images', 'bigmonkey.png'))
    BIGMONKEY = pygame.transform.scale(BIGMONKEY, (500, 400))
    SHOP = pygame.image.load(os.path.join('images', 'itemshop.png'))
    SHOP = pygame.transform.scale(SHOP, (180, 90))
    BACKBUTTON = pygame.image.load(os.path.join('images', 'backbutton.png'))
    BACKBUTTON = pygame.transform.scale(BACKBUTTON, (180, 90))
    BANANA = pygame.image.load(os.path.join('images', 'bananas.png'))
    BANANA = pygame.transform.scale(BANANA, (100, 100))
    WOOD = pygame.image.load(os.path.join('images', 'wood.jpg'))
    WOOD = pygame.transform.scale(WOOD, (900, 600))
    COIN = pygame.image.load(os.path.join('images', 'coin.png'))
    COIN = pygame.transform.scale(COIN, (100, 100))
    MORECOINS = pygame.image.load(os.path.join('images', 'morecoins.png'))
    MORECOINS = pygame.transform.scale(MORECOINS, (100, 100))

    MONKEY_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'monkeynoise.wav'))

    # Buttons
    shop_button = Button(700, 500, SHOP)
    back_button = Button(20, 20, BACKBUTTON)
    food_button = Button(0, 400, BANANA)
    coin_button = Button(800, 20, COIN)
    monkey_button = Button(300, 220, MONKEY, sound=MONKEY_SOUND)  
    monkey_button_medium = Button(300, 220, MIDMONKEY, sound=MONKEY_SOUND)
    monkey_button_big = Button(200, 220, BIGMONKEY, sound=MONKEY_SOUND)
    
    player_pet = Pet()

    # run main game loop
    main()
