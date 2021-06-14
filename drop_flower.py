import pygame
import os
import random



# Window's parameters
screen_width = 800
screen_height = 600
screen_size = (screen_width, screen_height)


# Colors
BLACK = ('#000000')
GOLD = ('#FFD700')
PINK = ('#FF69B4')
WHITE = ('#FFFFFF')
YELLOW = ('#FFFF00')
RED = ('#FF0000')

# Pygame inits
pygame.font.init()
pygame.mixer.init()

# Images
flower_image = pygame.image.load("flower.png")
bouquets_image = pygame.image.load("bouquets.png")
flower1_image = pygame.image.load("flower1.png")
flower2_image = pygame.image.load("flower2.png")
owca_image = pygame.image.load("owca.png")
background_image = pygame.image.load("background.jpg")


# Sound
correctsound = pygame.mixer.Sound("correct.wav")
wrongsound = pygame.mixer.Sound("wrong.wav")
sound = pygame.mixer.Sound("lopp.mp3")

# Window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Drop flower")


########################################
# Game
########################################


def text_objects(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


def text_on_the_screen(window, message, size, x, y, color):
    largetext = pygame.font.Font('freesansbold.ttf', size)
    textsurf, textrect = text_objects(message, largetext, color)
    textrect.center = (x, y)
    window.blit(textsurf, textrect)


def button(window, color, x, y, w, h, text_color, text_msg, action_color,  action):
    text_size = pygame.font.Font('freesansbold.ttf', 40)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(window, action_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action(window)
    else:
        pygame.draw.rect(window, color, (x, y, w, h))

    textsurf, textrect = text_objects(text_msg, text_size, text_color)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(textsurf, textrect)


def exit_the_game(window):
    pygame.display.quit()
    quit()


def update_high_scores(text_file, number_of_points):
    high_scores = open(text_file, "r")
    high_scores = high_scores.readlines()
    new_high_scores = []
    added_result = False


    for i in range(5):
        if int(high_scores[i].split('_')[0]) <= number_of_points and not added_result:
            new_high_scores.append(str(number_of_points) + '_' + os.getlogin() + '\n')
            added_result = True
        else:
            if added_result:
                new_high_scores.append(high_scores[i - 1])
            else:
                new_high_scores.append(high_scores[i])

    high_scores = open("high_scores.txt", "w")
    high_scores.writelines(new_high_scores)
    high_scores.close()


def set_difficulty_easy(window):
    high_scores = open("settings.txt", "w")
    high_scores.writelines(['difficulty: Easy'])


def set_difficulty_medium(window):
    high_scores = open("settings.txt", "w")
    high_scores.writelines(['difficulty: Medium'])


def set_difficulty_hard(window):
    high_scores = open("settings.txt", "w")
    high_scores.writelines(['difficulty: Hard'])


#######################################
#   Functions - creating interfaces of windows
########################################


def menu(window):
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        
        window.fill(PINK)

        text_on_the_screen(window, "FLOWER DROP", 50, 400, 200, BLACK)
        sound.play()
        button(window, GOLD, 400, 50, 300, 50, BLACK, 'Start', YELLOW, play)

        button(window, GOLD, 50, 320, 300, 50, BLACK, 'Rules', YELLOW, rules)
        button(window, GOLD, 450, 320, 300, 50, BLACK, 'Settings', YELLOW, settings)
        button(window, GOLD, 250, 410, 300, 50, BLACK, 'Author', YELLOW, author)
        button(window, GOLD, 50, 500, 300, 50, BLACK, 'Scores', YELLOW, scores)
        button(window, GOLD, 450, 500, 300, 50, BLACK, 'Quit', YELLOW, exit_the_game)


def play(window):
    player = Player()
    flowers = []
    owca = []
    addnewdropflower = 0
    addowca = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

        if player.lives == 0:
            update_high_scores("high_scores.txt", player.score)
            menu(window)

        if addnewdropflower == 250:
            flowers.append(Flower())
            addnewdropflower = 0

        if addowca == 250:
            owca.append(Owcas())
            addowca = 0

        window.blit(background_image, (0, 0))

        for flower in flowers:
            flower.movement()
            flower.draw()

            if flower.y >= screen_height:
                flowers.remove(flower)
                player.lives -= 1
                wrongsound.play()

            if flower.rect.colliderect(player.rect):
                flowers.remove(flower)
                player.score += 1
                correctsound.play()
    

        for owce in owca:
            owce.move()
            owce.dr()

            if owce.rect.colliderect(player.rect):
                owca.remove(owce)
                player.lives -= 1
                wrongsound.play()



        player.movement()
        player.scoreboard()
        player.showlives()
        player.draw()


        addnewdropflower += 1
        addowca += 1

        sound.stop()
        pygame.display.update()


        
def rules(window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

        window.fill(PINK)
        text_on_the_screen(window, "Rules:", 50, 400, 100, BLACK)
        text_on_the_screen(window, "Use LEFT and RIGHT arrow keys to move the bouquets.", 20, 400, 230, BLACK)
        text_on_the_screen(window, "You need to catch all flower.", 20, 400, 260, BLACK)
        text_on_the_screen(window, "Warning! You have only three lives and you need avoid NETTLE.", 20, 400, 290, BLACK)

        button(window, GOLD, 30, 20, 300, 50, BLACK, 'Back to menu', YELLOW, menu)
       
        sound.stop()
        pygame.display.update()

def author(window):
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

        window.fill(PINK)
        text_on_the_screen(window, "About me:", 50, 400, 100, BLACK)
        text_on_the_screen(window, "Adrianna Ziobroniewicz", 20, 400, 230, BLACK)
        text_on_the_screen(window, "Matematyka Stosowana, semestr 2", 20, 400, 260, BLACK)
        
        

        button(window, GOLD, 30, 20, 300, 50, BLACK, 'Back to menu', YELLOW, menu)
        sound.stop()
        pygame.display.update()

def settings(window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

        window.fill(PINK)
        text_on_the_screen(window, "Difficulty: ", 50, 400, 100, BLACK)

        button(window, GOLD, 50, 150, 200, 100, BLACK, 'Easy', GOLD,
               set_difficulty_easy)
        button(window, GOLD, 300, 150, 200, 100, BLACK, 'Medium', GOLD,
               set_difficulty_medium)
        button(window, GOLD, 550, 150, 200, 100, BLACK, 'Hard', GOLD,
               set_difficulty_hard)

        setting = open("settings.txt", "r")
        setting = setting.readlines()

        text_on_the_screen(window, setting[0], 20, 400, 350, BLACK)
        button(window, GOLD, 30, 20, 300, 50, BLACK, 'Back to menu', YELLOW, menu)
        sound.stop()
        pygame.display.update()


def scores(window):
    high_scores = open("high_scores.txt", "r")
    high_scores = high_scores.readlines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()

        window.fill(PINK)
        text_on_the_screen(window, "High scores:", 50, 400, 150, BLACK)
        for i in range(5):
            text_on_the_screen(window, str(i+1) + '.', 20, 230, 200+30*i, BLACK)
            text_on_the_screen(window, high_scores[i].split('_')[1][:-1], 20, 380, 200+30*i, BLACK)
            text_on_the_screen(window, high_scores[i].split('_')[0], 20, 550, 200+30*i, BLACK)
        button(window, GOLD, 30, 20, 300, 50, BLACK, 'Back to menu', YELLOW, menu)
        sound.stop()
        pygame.display.update()

########################################
#  Classes of objects on the screen
########################################


class Player:
    def __init__(self):
        high_scores = open("settings.txt", "r")
        high_scores = high_scores.readlines()[0].split(' ')[1]
        self.image = bouquets_image
        self.x = screen_width/2
        self.y = screen_height - 15
        if high_scores == 'Easy':
            self.speed = 3
        elif high_scores == 'Medium':
            self.speed = 2
        else:
            self.speed = 1
        self.score = 0
        self.lives = 3
        self.rect = self.image.get_rect()

    def movement(self):
        self.rect.center = (self.x, self.y)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.x > screen_width:
                self.x = screen_width
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.x < 0:
                self.x = 0

        if self.x <= 50:
            self.x = 50
        elif self.x >= screen_width - 50:
            self.x = screen_width - 50

    def draw(self):
        screen.blit(bouquets_image, (self.x-55, self.y-30))

    def scoreboard(self):
        text_on_the_screen(screen, "Points: " + str(self.score), 30, 70, 30, BLACK)

    def showlives(self):
        text_on_the_screen(screen, "Lives: " + str(self.lives), 30, 730, 30, RED)


class Flower:
    def __init__(self):
        self.image = random.choice([flower_image, flower1_image, flower2_image])
        self.x = random.randint(50, screen_width-50)
        self.y = 0
        self.speed = 1
        self.rect = self.image.get_rect()


    def movement(self):
        self.rect.center = (self.x, self.y)
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x-20, self.y-23))

class Owcas:
    def __init__(self):
        self.image = random.choice([owca_image])
        self.x = random.randint(50, screen_width-50) 
        self.y = 0
        self.speed = (round(random.uniform(0.5, 1.5), 1))
        self.rect = self.image.get_rect()

       

    def move(self):
        self.rect.center = (self.x, self.y)
        self.y += self.speed

    def dr(self):
        screen.blit(self.image, (self.x-10, self.y-18))



if __name__ == "__main__":
    menu(screen)
