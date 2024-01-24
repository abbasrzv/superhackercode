# Import necessary libraries
import pygame
import os

# Set up the dimensions of the game window
WIDTH, HEIGHT = 900, 600

# Initialize and configure the sound mixer
pygame.mixer.init()
pygame.mixer.set_num_channels(2)

# Define a class for creating buttons in the game
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

        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if the left mouse button is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                # Play a sound if provided
                if self.sound:
                    pygame.mixer.Channel(1).play(self.sound)

        # Reset clicked state when the mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on the game window
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Define a class for the player's virtual pet
class Pet():
    def __init__(self):
        # Initialize pet attributes
        self.hunger = 100
        self.hunger_decrease_rate = 1
        self.last_update_time = pygame.time.get_ticks()
        self.money = 0
        self.money_increase_rate = 1
        self.last_money_update_time = pygame.time.get_ticks()
        self.price_banana = 1000
        self.has_medium_monkey = False
        self.has_big_monkey = False
        self.more_coins_multiplier = 100
        self.more_coins_clicked = False

        # Cosmetic buttons for the pet
        self.has_chain = False
        self.chain_button = Button(600, 200, pygame.transform.scale(CHAIN, (100, 100)))

        self.has_vader = False
        self.vader_button = Button(325, 400, pygame.transform.scale(VADER, (100, 100)))

        self.has_gun = False
        self.gun_button = Button(600, 400, pygame.transform.scale(GUN, (100, 100)))

    def feed(self):
        # Feed the pet and deduct money if the player has enough money
        if self.money >= self.price_banana:
            self.hunger += 10
            if self.hunger > 100:
                self.hunger = 100
            self.money -= self.price_banana

    def update_hunger(self):
        # Update the pet's hunger over time
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_update_time

        if time_elapsed >= 5000:
            self.hunger -= self.hunger_decrease_rate
            if self.hunger < 0:
                self.hunger = 0
            self.last_update_time = current_time

    def update_money(self):
        # Update the player's money over time
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_money_update_time

        if time_elapsed >= 1000:
            if self.more_coins_clicked:
                self.money += 1000
            else:
                self.money += self.money_increase_rate
            self.last_money_update_time = current_time

    def draw_money_text(self):
        # Draw the player's money on the game window
        font = pygame.font.Font(None, 36)
        text = font.render(f'Money: {self.money}', True, (0, 255, 0))
        text_rect = text.get_rect(topleft=(50, 20))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (50, 20))

    def draw_hunger_text(self):
        # Draw the pet's hunger level on the game window
        font = pygame.font.Font(None, 36)
        text = font.render(f'Hunger: {self.hunger}', True, (255, 0, 255))
        text_rect = text.get_rect(topleft=(50, 70))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (50, 70))

    def draw_money_text_shop(self):
        # Draw the player's money on the shop screen
        font = pygame.font.Font(None, 36)
        text = font.render(f'Money: {self.money}', True, (0, 255, 0))
        text_rect = text.get_rect(topright=(WIDTH - 50, 20))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (text_rect.x, text_rect.y))

    def draw_hunger_text_shop(self):
        # Draw the pet's hunger level on the shop screen
        font = pygame.font.Font(None, 36)
        text = font.render(f'Hunger: {self.hunger}', True, (255, 0, 255))
        text_rect = text.get_rect(topright=(WIDTH - 50, 70))
        pygame.draw.rect(WIN, (0, 100, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
        WIN.blit(text, (text_rect.x, text_rect.y))

# Function to draw the main game window
def draw_window():
    # Draw the background and buttons on the game window
    WIN.blit(BACKGROUND, (0, 0))

    if player_pet.has_big_monkey:
        monkey_button_big.draw()
    elif player_pet.has_medium_monkey:
        monkey_button_medium.draw()
    else:
        monkey_button.draw()

    # Blit cosmetics on top of the monkey
    if player_pet.has_chain:
        WIN.blit(CHAIN, (340, 300))

    if player_pet.has_vader:
        WIN.blit(VADER, (320, 220))

    if player_pet.has_gun:
        WIN.blit(GUN, (160, 350))

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

        # Display cost text above the existing buttons
        price_text = font.render(f'Cost: {player_pet.price_banana}', True, (255, 255, 255))
        WIN.blit(price_text, (100, 380))
        description_text = font.render("Restores 10 hunger", True, (255, 255, 255))
        WIN.blit(description_text, (100, 500))

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

        # Cosmetic buttons in the shop
        if player_pet.chain_button.draw() and player_pet.money >= 25000 and not player_pet.has_chain:
            player_pet.money -= 25000
            player_pet.has_chain = True
        chain_cost_text = cost_font.render(f'Cost: 25000', True, (255, 255, 255))
        WIN.blit(chain_cost_text, (600, 170))
        chain_description_text = description_font.render("cool chain!", True, (255, 255, 255))
        WIN.blit(chain_description_text, (600, 310))

        if player_pet.vader_button.draw() and player_pet.money >= 75000 and not player_pet.has_vader:
            player_pet.money -= 75000
            player_pet.has_vader = True
        vader_cost_text = cost_font.render(f'Cost: 75000', True, (255, 255, 255))
        WIN.blit(vader_cost_text, (325, 370))
        vader_description_text = description_font.render("darth vader mask", True, (255, 255, 255))
        WIN.blit(vader_description_text, (325, 515))

        if player_pet.gun_button.draw() and player_pet.money >= 125000 and not player_pet.has_gun:
            player_pet.money -= 125000
            player_pet.has_gun = True
        gun_cost_text = cost_font.render(f'Cost: 125000', True, (255, 255, 255))
        WIN.blit(gun_cost_text, (600, 370))
        gun_description_text = description_font.render("big boy gun", True, (255, 255, 255))
        WIN.blit(gun_description_text, (600, 515))
        if back_button.draw():
            run_shop_screen = False

        pygame.display.update()

# Main game loop
def main():
        clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Check if the coin button is clicked
            if coin_button.draw():
                # Increase money based on whether more coins were clicked
                if player_pet.more_coins_clicked:
                    player_pet.money += 1000
                else:
                    player_pet.money += 100

        # Update pet's hunger and money
        player_pet.update_hunger()
        player_pet.update_money()

        # Draw the main game window
        draw_window()

    # Clean up and quit Pygame when the game loop exits
    cleanup()

# Cleanup function to handle quitting Pygame
def cleanup():
    if pygame.get_init():
        pygame.quit()

# Game window setup
if __name__ == "__main__":
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('My Little Monkey')

    FPS = 60

    # Load and scale images for the game
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
    CHAIN = pygame.image.load(os.path.join('images', 'chain.png'))
    CHAIN = pygame.transform.scale(CHAIN, (200, 200))
    VADER = pygame.image.load(os.path.join('images', 'darthvader.png'))
    VADER = pygame.transform.scale(VADER, (200, 200))
    GUN = pygame.image.load(os.path.join('images', 'gun.png'))
    GUN = pygame.transform.scale(GUN, (300, 200))

    # Load monkey sound effect
    MONKEY_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'monkeynoise.wav'))

    # Create buttons for the game
    shop_button = Button(700, 500, SHOP)
    back_button = Button(20, 20, BACKBUTTON)
    food_button = Button(100, 400, BANANA)
    coin_button = Button(800, 20, COIN)
    monkey_button = Button(300, 220, MONKEY, sound=MONKEY_SOUND)
    monkey_button_medium = Button(300, 220, MIDMONKEY, sound=MONKEY_SOUND)
    monkey_button_big = Button(200, 220, BIGMONKEY, sound=MONKEY_SOUND)

    # Create the player's pet
    player_pet = Pet()

    # Run the main game loop
    main()

