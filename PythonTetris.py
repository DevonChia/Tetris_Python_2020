import pygame
import random
from pygame.locals import *

colors = [0,(184,15,10), (76, 187, 23), (0,139,139), (255,192,203), (255,140,0), (0,255,255)]


class Block:
    shape = [[[1,5,9,13],[4,5,6,7]],
              [[1,2,5,6]],
              [[1,4,5,6],[1,5,6,9],[0,1,2,5],[1,4,5,9]],
              [[1,5,6,7],[1,2,5,9],[0,1,2,6],[1,5,8,9]]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.randint(1,len(colors)-1)
        self.type = random.randint(0,len(self.shape)-1)
        self.rotation = 0

    @property
    def get_rotation(self):
        return self.rotation

    @get_rotation.setter
    def set_rotation(self, rotation):
        self.rotation = rotation

    def current_block(self):
        x = self.shape[self.type][self.rotation]
        return x

    def block_shape(self):
        return self.shape[self.type]


class Tetris:
    width = 10
    height = 20
    block = None

    def __init__(self, x, y):
        self.gridState = []
        self.score = 0
        self.state = 'new'
        self.x = 100
        self.y = 60

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(0)
            self.gridState.append(line)

    def new_block(self):
        self.block = Block(3,0)
        return self.block

    def collide(self):
        collided = False
        for i in range(4):
            for j in range(4):
                if i*4+j in self.block.current_block():
                    if self.block.y + i > self.height - 1 or \
                            self.block.x + j < 0 or \
                            self.block.x + j > self.width -1 or \
                            self.block.y < 0 or \
                            self.gridState[self.block.y + i][self.block.x + j] > 0:
                        collided = True
        return collided

    def complete_row(self):
        full_row = 0
        for i in range(20):
            completed = 0
            for j in range(10):
                if self.gridState[i][j] == 0:
                    completed = 1
            if completed == 0:
                full_row += 1
                for i2 in range(i,0,-1):
                    for j2 in range(j,-1,-1):
                        self.gridState[i2][j2] = self.gridState[i2-1][j2]
        # score multipler for multiple complete rows
        self.score += 1 * full_row

    def move_down(self):
        prev_blocklocation = self.block.y
        self.block.y += 1
        if self.collide() or self.block is None:
            self.block.y = prev_blocklocation
            self.stop_block()
            self.complete_row()
            self.next_block()

    def move_side(self, direction):
        if self.block is None:
            # to prevent error when detect user input of moving side right before a collision where system will
            # take it as a combination of move_side and move_down in one instance
            pass
        else:
            prev_blocklocation = self.block.x
            self.block.x += direction
            if self.collide():
                self.block.x = prev_blocklocation

    def stop_block(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.block.current_block():
                    self.gridState[self.block.y + i][self.block.x + j] = self.block.color

    def next_block(self):
        self.block = None

    def rotate_block(self):
        if self.block is None:
            pass
        else:
            prev_rotation = self.block.rotation
            self.block.rotation = (self.block.rotation + 1) % len(self.block.block_shape())
            if self.collide():
                self.block.rotation = prev_rotation


def main():

    GREY = (150, 150, 150)
    BLACK = (0,0,0)
    GOLD = (255,215,0)

    pygame.init()
    game_display = pygame.display.set_mode((400, 500))
    pygame.display.set_caption('Tetris Project')
    running = True
    new_game = Tetris(20,10)
    clock = pygame.time.Clock()
    speed = 6

    while running:
        clock.tick(speed)
        if new_game.block is None:
            new_game.new_block()

        if new_game.state == 'new' and not new_game.collide():
            new_game.move_down()
        else:
            new_game.state = 'game over'

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN
                                      and (event.key == K_ESCAPE)
                                      and new_game.state == 'game over'):
                # quit the game upon user input
                running = False
                quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    new_game.move_side(-1)
                if event.key == K_RIGHT:
                    new_game.move_side(1)
                if event.key == K_SPACE:
                    new_game.rotate_block()
                if event.key == K_RETURN and new_game.state == 'game over':
                    # restart the game upon user input
                    new_game.__init__(100,60)
                if event.key == K_DOWN:
                    speed *= 3
            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    speed = 6

        # to display only current Block Rect object
        game_display.fill(GREY)

        for i in range(20):
            for j in range(10):
                pygame.draw.rect(game_display, BLACK, [new_game.x + (20*j), new_game.y + (20*i), 20, 20], 1)
                if new_game.gridState[i][j] > 0:
                    pygame.draw.rect(game_display, colors[new_game.gridState[i][j]],
                                     [new_game.x + (20*j) + 1, new_game.y + (20*i) - 1, 20-2, 20-2])

        if new_game.block is not None:
            for i in range(4):
                for j in range(4):
                    if i*4+j in new_game.block.current_block():
                        pygame.draw.rect(game_display,colors[new_game.block.color],
                                         [new_game.x + 20 * (j+new_game.block.x),
                                          new_game.y + 20 * (i+new_game.block.y),
                                         20,20])

        font1 = pygame.font.Font('freesansbold.ttf', 32)
        font2 = pygame.font.Font('freesansbold.ttf',20)

        text = ['Game Over', 'Press "Enter" to restart', 'or "Esc" to exit game']
        gametext_height = 100
        if new_game.state == 'game over':
            for i in text:
                gametext = font1.render(i, True, GOLD, BLACK)
                gametextRect = gametext.get_rect()
                gametext_height += 50
                gametextRect.center = 200, gametext_height
                game_display.blit(gametext, gametextRect)

        score_text = font2.render('Score: {}'.format(str(new_game.score)), True, GOLD, GREY)
        score_textRect = score_text.get_rect()
        score_textRect.center = 50, 75
        game_display.blit(score_text, score_textRect)

        pygame.display.flip()


main()
