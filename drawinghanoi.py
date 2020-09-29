import pygame

pygame.init()

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
DISC_HEIGHT = round(SCREEN_HEIGHT/8)

# x values / peg locations
LEFT_PEG = SCREEN_WIDTH / 4
MIDDLE_PEG = SCREEN_WIDTH / 2
RIGHT_PEG = SCREEN_WIDTH  * (3/4)

# y values for disc locations
BOTTOM_Y = SCREEN_HEIGHT - DISC_HEIGHT * 3
MIDDLE_Y = BOTTOM_Y - DISC_HEIGHT - PADDING
TOP_Y = MIDDLE_Y - DISC_HEIGHT - PADDING

# calculate disc width
LRG_WIDTH = SCREEN_WIDTH / 4 
MED_WIDTH = LRG_WIDTH - (2 * MARGIN_X)
SML_WIDTH = LRG_WIDTH - (4 * MARGIN_X)

# draws base, pegs and background
def draw_board():
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, BLACK, (0, SCREEN_HEIGHT-(2*round(SCREEN_HEIGHT/8)), SCREEN_WIDTH, round(SCREEN_HEIGHT/8))) # base
    peg_a = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 4), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
    peg_b = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 2), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
    peg_c = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH * (3/4)), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))

def draw_prompt(selection):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    text_options = ['Large disc Selected', 'Medium disc selected', 'Small disc selected', 'Cannot move left', 'cannot move right', 'cannot place big disc on smaller']
    text = fontObj.render(text_options[selection], True, BLUE)
    textRectObj = text.get_rect()
    textRectObj.center = (MIDDLE_PEG, 0 + textRectObj.height/2)
    SCREEN.blit(text, textRectObj)


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
        self.location = 0
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

def move(selection, i, peg):
    temp = discs[selection] # hold the disc while we remove it from one peg and append it to the next.
    peg.remove(discs[selection])
    discs[selection].rect.y = y_list[len(board[i])]                    
    board[i].append(temp)
    discs[selection].location = i
    discs[selection].rect.x = (pegs[discs[selection].location] - (discs[selection].rect.width / 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg:
                    if i == 0:
                        destination = 2
                    else:
                        destination = i - 1
                    if len(board[destination]) <= selection:
                        move(selection, destination, peg)
                    else: 
                        text_selection = 3
                    break

        if keys[pygame.K_RIGHT]:
            for i, peg in enumerate(board):
                if discs[selection] in peg:
                    if i == 2:
                        destination = 0
                    else:
                        destination = i + 1
                    if len(board[destination]) <= selection:
                        move(selection, destination, peg)
                    else: 
                        text_selection = 3
                    break

        # switch selection between discs
        if keys[pygame.K_UP]:
            if selection == 2:
                selection = 0
                text_selection = 0
            else:
                selection += 1
                text_selection = selection

        if keys[pygame.K_DOWN]:
            if selection == 0:
                selection = 2
                text_selection = 0
            else:
                selection -= 1   
                text_selection = selection


    draw_board()
    all_discs.draw(SCREEN)
    draw_prompt(text_selection)
    pygame.display.update()