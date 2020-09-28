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

# draw base and background
SCREEN.fill(WHITE)
pygame.draw.rect(SCREEN, BLACK, (0, SCREEN_HEIGHT-(2*round(SCREEN_HEIGHT/8)), SCREEN_WIDTH, round(SCREEN_HEIGHT/8))) # base
peg_a = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 4), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
peg_b = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH / 2), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))
peg_c = pygame.rect.Rect(pygame.draw.rect(SCREEN, BLACK, ((SCREEN_WIDTH * (3/4)), SCREEN_HEIGHT - round(SCREEN_HEIGHT * (3/4)), round(SCREEN_WIDTH / 70), round(SCREEN_HEIGHT * (3/5)))))

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

# create the disc class
class Disc(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.movable = False
        self.rect = self.image.get_rect()

# create discs and add them to group
lrgDisc = Disc(RED, LRG_WIDTH, DISC_HEIGHT)
lrgDisc.rect.x = (LEFT_PEG - (LRG_WIDTH / 2))
lrgDisc.rect.y = BOTTOM_Y

medDisc = Disc(GREEN, MED_WIDTH, DISC_HEIGHT)
medDisc.rect.x = (LEFT_PEG - (MED_WIDTH / 2))
medDisc.rect.y = MIDDLE_Y

smlDisc = Disc(BLUE, SML_WIDTH, DISC_HEIGHT)
smlDisc.rect.x = (LEFT_PEG - (SML_WIDTH / 2))
smlDisc.rect.y = TOP_Y
smlDisc.movable = True # top disc is free to move

all_discs = pygame.sprite.Group()
all_discs.add(lrgDisc)
all_discs.add(medDisc)
all_discs.add(smlDisc)

# board game
pegs = [LEFT_PEG, MIDDLE_PEG, RIGHT_PEG]

A = [lrgDisc, medDisc, smlDisc]
B = []
C = []

# TODO function that checks if selection is legal
def is_movable(disc):
    pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_disc = [disc for disc in all_discs if disc.rect.collidepoint(event.pos)]
            if selected_disc[0].movable == True:
                

    all_discs.draw(SCREEN)
    pygame.display.update()