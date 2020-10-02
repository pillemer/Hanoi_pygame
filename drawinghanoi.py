import pygame

pygame.init()

# ------------------- set up ------------------- #

# set up the window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Drawing Hanoi Puzzle')

# set up the colours
BLACK =  (0,   0,   0  )
WHITE =  (255, 255, 255)
RED =    (255, 0,   0  )
GREEN =  (0,   255, 0  )
BLUE =   (0,   0,   255)

# calculate the sizes
PADDING = 5
MARGIN_X = 20
DISC_HEIGHT = round(SCREEN_HEIGHT/8)   # adjusting needed for scaling

# x values / peg locations
LEFT_PEG = SCREEN_WIDTH / 4
MIDDLE_PEG = SCREEN_WIDTH / 2
RIGHT_PEG = SCREEN_WIDTH  * (3/4)

# y values for disc locations
BOTTOM_Y = SCREEN_HEIGHT - DISC_HEIGHT * 3   # adjusting needed for scaling
MIDDLE_Y = BOTTOM_Y - DISC_HEIGHT - PADDING
TOP_Y = MIDDLE_Y - DISC_HEIGHT - PADDING

# calculate disc width
LRG_WIDTH = SCREEN_WIDTH / 4 - (0 * MARGIN_X)
MED_WIDTH = LRG_WIDTH - (1 * MARGIN_X)
SML_WIDTH = LRG_WIDTH - (2 * MARGIN_X)

# BASE_WIDTH = SCREEN_WIDTH / 4
# for i in range(n):
#     pass

# set up the pegs
pegs = [LEFT_PEG, MIDDLE_PEG, RIGHT_PEG]
y_list = [BOTTOM_Y, MIDDLE_Y, TOP_Y]

# create the disc class
class Disc(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.movable = False
        self.width = width
        self.rect = self.image.get_rect()

# create discs and add them to group
lrgDisc = Disc(RED, LRG_WIDTH, DISC_HEIGHT)
lrgDisc.rect.x = (pegs[0] - (lrgDisc.rect.width / 2))
lrgDisc.rect.y = BOTTOM_Y

medDisc = Disc(GREEN, MED_WIDTH, DISC_HEIGHT)
medDisc.rect.x = (pegs[0] - (medDisc.rect.width / 2))
medDisc.rect.y = MIDDLE_Y

smlDisc = Disc(BLUE, SML_WIDTH, DISC_HEIGHT)
smlDisc.rect.x = (pegs[0] - (smlDisc.rect.width / 2))
smlDisc.rect.y = TOP_Y
smlDisc.movable = True # top disc is free to move

# add discs to Sprite group
all_discs = pygame.sprite.Group()
all_discs.add(lrgDisc)
all_discs.add(medDisc)
all_discs.add(smlDisc)

# board game
discs = [lrgDisc, medDisc, smlDisc]
board = [[discs[0], discs[1], discs[2]], [], []]

# start with smallest disc selected on the left peg
selection = text_selection = 2


# --------------- helper functions --------------- #

# draws base, pegs and background
def draw_board():
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, BLACK, (0, SCREEN_HEIGHT-(2*round(SCREEN_HEIGHT/8)), SCREEN_WIDTH, round(SCREEN_HEIGHT/8))) # base
    peg_a = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 4), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
    peg_b = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 2), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
    peg_c = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH * (3/4)), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))

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
    textRectObj.center = (MIDDLE_PEG, SCREEN_HEIGHT - textRectObj.height)
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
    if selection == 2 and moving_up:
        return 0
    elif selection == 0 and not moving_up:
        return 2
    else:
        return selection + (2 * int(moving_up) - 1)

# remove disc from current peg and place on new one
def move(selection, i, peg):
    temp = discs[selection] # hold the disc while we remove it from one peg and append it to the next.
    peg.remove(discs[selection])
    discs[selection].rect.y = y_list[len(board[i])]                    
    board[i].append(temp)
    discs[selection].location = i
    discs[selection].rect.x = (pegs[discs[selection].location] - (discs[selection].rect.width / 2))

def update_movable():
    for peg in board:
        if discs[selection] in peg and len(peg) < selection + 2:
            discs[selection].movable = True
            break
        else:
            discs[selection].movable = False

    # exception case for medium disc under small disc
    if selection == 1 and discs[2] in peg:
        discs[selection].movable = False
        


# ----------------- game loop ----------------- #

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # move discs left or right where possible
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg and discs[selection].movable:
                    destination = set_destination(i, False)

                    # can't move medium sized disc on top of small disc:
                    if selection == 1 and discs[2] in board[destination]:
                        text_selection = 5
                        break

                    if len(board[destination]) <= selection:
                        move(selection, destination, peg)
                    else: 
                        text_selection = 5
                    break

        if keys[pygame.K_RIGHT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg and discs[selection].movable:
                    destination = set_destination(i, True)

                    # can't move medium sized disc on top of small disc:
                    if selection == 1 and discs[2] in board[destination]:
                        text_selection = 5
                        break

                    if len(board[destination]) <= selection:
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


