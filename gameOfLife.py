import pygame, sys, pprint
from pygame.locals import *


WIDTH = 600
HEIGHT = 400
BOARDWIDTH = 500
BOARDHEIGHT = 300
SCALE = 25
BOARDCOLS = int(BOARDWIDTH / SCALE)
BOARDROWS = int(BOARDHEIGHT / SCALE)
XMARGIN = int((WIDTH - BOARDWIDTH) / 2)
YMARGIN = int((HEIGHT - BOARDHEIGHT) / 2)
FPS = 10

LIVE = True
DEAD = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKYBLUE = (66, 134, 244)
VALVET = (242, 65, 133)
GRAY = (193, 184, 187)

BACKGROUND = GRAY
LIFE = BLACK
DEAD = WHITE


def setup():
    global lifes, DISPLAYSURF, FPSCLOCK, start_button, reset_button, stop_button, exit_button
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('gameOfLifeSimulator')

    lifes = list()
    for i in range(XMARGIN, XMARGIN + BOARDWIDTH, SCALE):
        tempList = []
        for j in range(YMARGIN, YMARGIN + BOARDHEIGHT, SCALE):
            tempList.append(Life(i, j))
        lifes.append(tempList)

    font = pygame.font.Font(None, 50)
    texts = ['start', 'reset', 'stop', 'exit']
    button_positions = get_buttons_position(font, texts)

    start_button = Button(button_positions[0], 350, SKYBLUE, texts[0])
    reset_button = Button(button_positions[1], 350, SKYBLUE, texts[1])
    stop_button = Button(button_positions[2], 350, SKYBLUE, texts[2])
    exit_button = Button(button_positions[3], 350, VALVET, texts[3])


def main():
    running = True
    activating = False

    while(running):
        DISPLAYSURF.fill(BACKGROUND)

        if(activating):
            population = list()
            for i in range(BOARDCOLS):
                temp = list()
                for j in range(BOARDROWS):
                    temp.append(find_neighbours(i, j))
                population.append(temp)

            for i in range(BOARDCOLS):
                for j in range(BOARDROWS):
                    state = lifes[i][j].state
                    neighbours = population[i][j]
                    if(state == LIVE and (neighbours > 3 or neighbours < 2)):
                        lifes[i][j].changeState()
                    elif(state == DEAD and neighbours == 3):
                        lifes[i][j].changeState()

        for i in range(BOARDCOLS):
            for j in range(BOARDROWS):
                lifes[i][j].draw()


        start_button.display()
        reset_button.display()
        stop_button.display()
        exit_button.display()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if(is_mouse_over_lifes(mouse_x, mouse_y)):
                    x = int((mouse_x - XMARGIN) / SCALE)
                    y = int((mouse_y - YMARGIN) / SCALE)
                    lifes[x][y].changeState()
                if(start_button.clicked(mouse_x, mouse_y)):
                    activating = True
                if(reset_button.clicked(mouse_x, mouse_y)):
                    activating = False
                    setup()
                if(stop_button.clicked(mouse_x, mouse_y)):
                    activating = False
                if(exit_button.clicked(mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        FPSCLOCK.tick(FPS)


class Life:
    def __init__(self,x, y):
        self.state = DEAD
        self.pos = pygame.math.Vector2(x, y)
        self.color = WHITE

    def draw(self):
        pygame.draw.ellipse(DISPLAYSURF, self.color, (self.pos.x, self.pos.y, SCALE, SCALE))

    def changeState(self):
        self.state = LIVE if self.state == DEAD else DEAD
        self.color = WHITE if self.state == DEAD else BLACK


class Button:
    def __init__(self, x, y, _color = WHITE, _text='button'):
        self.pos = pygame.math.Vector2(x, y)
        self.color = _color
        self.font = pygame.font.Font(None, 50)
        self.width, self.height = self.font.size(_text)
        self.text = self.font.render(_text, True, BLACK, self.color)

    def display(self):
        pygame.draw.rect(DISPLAYSURF, self.color, (self.pos.x, self.pos.y, self.width, self.height))
        DISPLAYSURF.blit(self.text, (self.pos.x, self.pos.y))

    def clicked(self, mouse_x, mouse_y):
        if(mouse_x > self.pos.x and mouse_x < self.pos.x + self.width and
           mouse_y > self.pos.y and mouse_y < self.pos.y + self.height):
            return True
        else:
            return False



def find_neighbours_index(target_x, target_y):
    neighbours = list()
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            x = (target_x + i + BOARDCOLS) % BOARDCOLS
            y = (target_y + j + BOARDROWS) % BOARDROWS
            neighbours.append([x, y])
    neighbours.remove([target_x, target_y])
    return neighbours

def find_neighbours(target_x, target_y):
    sum_ = 0
    neighbours = find_neighbours_index(target_x, target_y)
    for neighbour in neighbours:
        sum_ += 1 if lifes[neighbour[0]][neighbour[1]].state == LIVE else 0
    return sum_

def is_mouse_over_lifes(mouse_x, mouse_y):
    if((mouse_x > XMARGIN and mouse_x < WIDTH - XMARGIN) and
       (mouse_y > YMARGIN and mouse_y < HEIGHT - YMARGIN)):
       return True

def get_buttons_position(font, texts):
    total_width=0
    widths = list()
    for text in texts:
        width, height = font.size(text)
        widths.append(width)
    total_width = sum(widths)
    margin = (BOARDWIDTH-total_width) / (len(texts) - 1)
    positions = [XMARGIN]
    offsets = list()
    temp = XMARGIN
    for width in widths:
        print(width)
        offsets.append(width + margin)
    for offset in offsets:
        temp += offset
        positions.append(temp)
    positions.pop()
    return positions

if __name__ == '__main__':
    setup()
    main()
