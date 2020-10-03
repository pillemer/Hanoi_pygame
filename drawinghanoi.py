import pygame
import random

pygame.init()


# ------------------- how many discs? ------------------- #

# change this number to adjust the number of discs in the puzzle (Max = 7)
disc_number = 7

# ------------------- set up ------------------- #

# set up the window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Drawing Hanoi Puzzle')

# set up the colours
BLACK =  (0,   0,   0  )
WHITE =  (255, 255, 255)
RED =    (255, 0,   0  )
ORANGE = (255, 128, 0  )
YELLOW = (255, 255, 0  )
GREEN =  (0,   255, 0  )
AQUA =   (0,   255, 255)
BLUE =   (0,   0,   255)
PURPLE = (255, 0,   255)
colour_list = [RED, ORANGE, YELLOW, GREEN, AQUA, BLUE, PURPLE]
random.shuffle(colour_list)

# set the size parameters
PADDING = 5
MARGIN_X = 20
DISC_HEIGHT = round(SCREEN_HEIGHT/16)   # possible adjusting needed for scaling

# x values / peg locations
pegs = [SCREEN_WIDTH / 4, SCREEN_WIDTH / 2, SCREEN_WIDTH  * (3/4)]

# create the Disc class
class Disc(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.movable = False
        self.width = width
        self.rect = self.image.get_rect()

# create discs
discs = []
y_list = []
all_discs = pygame.sprite.Group()

for i in range(disc_number):
    y_value = (SCREEN_HEIGHT-(round(SCREEN_HEIGHT / 8))) - ((3 + i) * DISC_HEIGHT) - i * (PADDING)
    y_list.append(y_value)
    disc_width = SCREEN_WIDTH / 4 - (i * MARGIN_X)
    disc = Disc(colour_list.pop(), disc_width, DISC_HEIGHT)
    disc.rect.x = (pegs[0] - (disc.width / 2))
    disc.rect.y = y_list[i]
    all_discs.add(disc)
    discs.append(disc)

# game board 
board = [[], [], []]
board[0] = discs[:]

# start with smallest disc selected on the left peg
selection =  disc_number - 1
text_selection = 2

# --------------- helper functions --------------- #

# draws base, pegs and background
def draw_board():
    SCREEN.fill(WHITE)
    # base (x,y,w,h)
    pygame.draw.rect(SCREEN, BLACK, (0, SCREEN_HEIGHT * (3/4), SCREEN_WIDTH, round(SCREEN_HEIGHT/8)))
    # left peg
    pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 4), 
                                    SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), 
                                    round(SCREEN_WIDTH / 70), 
                                    round(SCREEN_HEIGHT * (3/5))))
    # middle peg
    pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 2), 
                                    SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), 
                                    round(SCREEN_WIDTH / 70), 
                                    round(SCREEN_HEIGHT * (3/5))))
    # right peg
    pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH * (3/4)),
                                    SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), 
                                    round(SCREEN_WIDTH / 70), 
                                    round(SCREEN_HEIGHT * (3/5))))

# text prompt selection and draw function
def draw_prompt(selection):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    text_options = ['Large disc Selected', 
                    'Medium disc selected', 
                    'Small disc selected', 
                    'Cannot move left', 
                    'cannot move right', 
                    'cannot place big disc on smaller', 
                    'cannot move disc underneath another']
    text = fontObj.render(text_options[selection], True, BLUE)
    textRectObj = text.get_rect()
    textRectObj.center = (pegs[1], SCREEN_HEIGHT - textRectObj.height)
    SCREEN.blit(text, textRectObj)

# set destination peg for each direction
def set_destination(origin, moving_right):
    if origin == 0 and not moving_right:
        return 2
    elif origin == 2 and moving_right:
        return 0
    else:
        return origin + (2 * int(moving_right) - 1)

# set new selection for playing disc:
def select_disc(selection, moving_up):
    if selection == len(discs) - 1 and moving_up:
        return 0
    elif selection == 0 and not moving_up:
        return len(discs) - 1
    else:
        return selection + (2 * int(moving_up) - 1)

# remove disc from current peg and place on new one
def move(selection, i, peg):
    temp = discs[selection] # hold the disc while we remove it from one peg and append it to the next.
    peg.remove(discs[selection])
    discs[selection].rect.y = y_list[len(board[i])]                    
    board[i].append(temp)
    discs[selection].location = i
    discs[selection].rect.x = (pegs[discs[selection].location] - (discs[selection].width / 2))

def update_movable():   
    for peg in board:
        if discs[selection] in peg and discs[selection].width <= min(peg, key=lambda x: x.width).width:
            discs[selection].movable = True
            break
        else:
            discs[selection].movable = False

# ----------------- game loop ----------------- #

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # move discs left or right when allowed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg and discs[selection].movable:
                    destination = set_destination(i, False)
                    if board[destination] == [] or discs[selection].width <= min(board[destination], key=lambda x: x.width).width:
                        move(selection, destination, peg)
                    else: 
                        text_selection = 5
                    break

        if keys[pygame.K_RIGHT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg and discs[selection].movable:
                    destination = set_destination(i, True)
                    if board[destination] == [] or discs[selection].width <= min(board[destination], key=lambda x: x.width).width:
                        move(selection, destination, peg)
                    else: 
                        text_selection = 5
                    break

        # switch selection between discs
        if keys[pygame.K_UP]:
            selection = text_selection = select_disc(selection, True)
            update_movable()
            if not discs[selection].movable:
                text_selection = 6

        if keys[pygame.K_DOWN]:
            selection = text_selection = select_disc(selection, False)
            update_movable()
            if not discs[selection].movable:
                text_selection = 6

    draw_board()
    all_discs.draw(SCREEN)
    draw_prompt(text_selection)
    pygame.display.update()
