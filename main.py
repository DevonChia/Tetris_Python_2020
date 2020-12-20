import pygame
import random
import itertools
from pygame.locals import *

pygame.init()
width = 550
height = 455
game_display = pygame.display.set_mode((width,height))

pygame.display.set_caption("First Project - Tetris")

RED= (255, 0, 0)
GREY=(150, 150, 150)
GREEN=(0,255,0)
game_table_height = 450
game_table_top = 0
game_table_left = 10
game_table_right = 280
game_table_width = game_table_right - game_table_left
per_block_size = game_table_width / 9
game_table = Rect(game_table_left, game_table_top, game_table_width+2, game_table_height) #left,top,width,height

long_bar = Rect(((game_table_width/9)*3+game_table_left),game_table_top,((game_table.width/9)*3),(game_table.width/9))

square = Rect(((game_table_width/9)*3+game_table_left), game_table_top, ((game_table_width/9)*2), ((game_table_width/9)*2))

l_bar = [[(per_block_size*3)+game_table_left,0],[(per_block_size*7)+game_table_left,0],[(per_block_size*7)+game_table_left,per_block_size],
         [(per_block_size*4)+game_table_left,per_block_size],[(per_block_size*4)+game_table_left,per_block_size*2],[(per_block_size*3)+game_table_left,per_block_size*2]]
default_l_bar = [[150,15],[250,15],[250,40],[180,40],[180,80],[150,80]]

t_bar = [[(per_block_size*3)+game_table_left,0],
         [(per_block_size*6)+game_table_left,0],
         [(per_block_size*6)+game_table_left, per_block_size],
         [(per_block_size*5)+game_table_left,per_block_size],
         [(per_block_size*5)+game_table_left,per_block_size*2],
         [(per_block_size*4)+game_table_left,per_block_size*2],
         [(per_block_size*4)+game_table_left,per_block_size],
         [(per_block_size*3)+game_table_left,per_block_size]]


l_shape = pygame.draw.polygon(game_display,GREEN,l_bar,3)
l_shape.left = ((game_table_width/9)*3+game_table_left) #shift to the center
t_shape = pygame.draw.polygon(game_display,GREEN,t_bar,3)
t_shape.left = ((game_table_width/9)*3+game_table_left)
print(type(l_shape))
print(l_bar)

all_pieces = [t_bar] #long_bar, t_bar,square, l_bar


def event_handler(block_type,step_counter,theblock,shape):
    # down key shl be incremental in speed and smooth descend
    # dir = { K_LEFT:(-15,0), K_RIGHT:(15,0), K_DOWN:(0,15)}
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT or (
                event.type == KEYDOWN and (
                event.key == K_ESCAPE
        )):
            # pygame.quit()
            quit()
            return False

        if block_type == "square":
            # For SQUARE BLOCK
            if event.type == KEYDOWN:
                if square.left > game_table_left and event.key == K_LEFT and square.bottom <= game_table_height:# | square.bottom < game_table_height:
                    square.move_ip(-per_block_size, 0)
                elif square.right < game_table_right and event.key == K_RIGHT and square.bottom <= game_table_height:
                    square.move_ip(per_block_size, 0)
                elif square.bottom < game_table_height and event.key == K_DOWN:
                    square.move_ip(0,per_block_size)

                else:
                    pass

        elif block_type == "long_bar":
            if event.type == KEYDOWN:
                if long_bar.left > game_table_left and event.key == K_LEFT and long_bar.bottom <= game_table_height:
                    long_bar.move_ip(-per_block_size, 0)
                elif long_bar.right < game_table_right and event.key == K_RIGHT and long_bar.bottom <= game_table_height:
                    long_bar.move_ip(per_block_size, 0)
                elif long_bar.bottom < game_table_height and event.key == K_DOWN:
                    long_bar.move_ip(0,per_block_size)
                else:
                    pass

        elif block_type =="l_bar":
            # For L BAR BLOCK
            if event.type == KEYDOWN:
                if l_shape.left > game_table_left and event.key == K_LEFT and l_shape.bottom <= game_table_height:
                    l_shape.move_ip(-per_block_size,0)
                    for point in l_bar:
                        point[0] -= per_block_size
                elif l_shape.right < game_table_right and event.key == K_RIGHT and l_shape.bottom <= game_table_height:
                    l_shape.move_ip(per_block_size, 0)
                    for point in l_bar:
                        point[0] += per_block_size
                elif l_shape.bottom < game_table_height and event.key == K_DOWN:
                    l_shape.move_ip(0,per_block_size)
                    for point in l_bar:
                        point[1] += per_block_size

                elif event.key == K_SPACE:
                    pass


        elif block_type == "t_bar":
            # for T BAR BLOCK
            if event.type == KEYDOWN:
                if shape.left > game_table_left and event.key == K_LEFT and shape.bottom <= game_table_height:
                    shape.move_ip(-per_block_size,0)
                    for point in theblock:
                        point[0] -= per_block_size
                elif shape.right < game_table_right and event.key == K_RIGHT and shape.bottom <= game_table_height:
                    shape.move_ip(per_block_size, 0)
                    for point in theblock:
                        point[0] += per_block_size
                elif shape.bottom < game_table_height and event.key == K_DOWN:
                    shape.move_ip(0,per_block_size)
                    for point in theblock:
                        point[1] += per_block_size
                elif event.key == K_SPACE:
                    print(step_counter)
                    theblock.clear()
                    for i in [[(per_block_size * 3) + game_table_left +10, 0],
                              [(per_block_size * 6) + game_table_left, 0],
                              [(per_block_size * 6) + game_table_left, per_block_size],
                              [(per_block_size * 5) + game_table_left, per_block_size],
                              [(per_block_size * 5) + game_table_left, per_block_size * 2],
                              [(per_block_size * 4) + game_table_left, per_block_size * 2],
                              [(per_block_size * 4) + game_table_left, per_block_size],
                              [(per_block_size * 3) + game_table_left, per_block_size]]:
                        theblock.append(i)

                return theblock


def draw_handler(current_piece,list_of_blocks):
    # current_piece = square
    # random.choice(all_pieces)
    run = 1
    print("outside of inner loop")
    # to centralise L Bar

    # for i in t_bar:
    #     i[0] += ((game_table_width/9)*3+game_table_left)
    step_counter = 0
    while run == 1:
        print("start of inner loop")
        clock = pygame.time.Clock()
        clock.tick(2)
        pygame.draw.rect(game_display, GREY, game_table)
        # iterate list of blocks here
        for i in list_of_blocks:
            if type(i) == list: #check for polygon
                pygame.draw.polygon(game_display,GREEN,i,2)
            else: #check for rect
                pygame.draw.rect(game_display,GREEN,i,2)

        if current_piece == long_bar:
            print("ENTER LONG BAR")
            event_handler("long_bar")
            pygame.draw.rect(game_display, RED, long_bar, 2)

            if long_bar.bottom < game_table_height:  # use square(Rect object) to move
                long_bar.move_ip(0,per_block_size)

            else:
                stored_block = long_bar.copy()
                list_of_blocks.append(stored_block)
                long_bar.left = (per_block_size*3) + game_table_left
                long_bar.top = game_table_top
                run == 0
                break

        elif current_piece == square:
            print("ENTER SQUARE")
            event_handler("square")
            square_shape = pygame.draw.rect(game_display, RED, square, 2)

            if square.bottom < game_table_height:  # use square(Rect object) to move
                square.move_ip(0,per_block_size)

            else:
                stored_block = square.copy()
                list_of_blocks.append(stored_block)
                square.left = (per_block_size*3) + game_table_left
                square.top = game_table_top
                run == 0
                break

        elif current_piece == l_bar:
            print("ENTER L BAR")
            event_handler("l_bar")

            pygame.draw.rect(game_display,GREEN,l_shape,1)
            x = pygame.draw.polygon(game_display, RED, l_bar, 2)
            # pygame.draw.rect(game_display, GREEN, l_shape, 1)
            if l_shape.bottom <= game_table_height:  # use square(Rect object) to move
                l_shape.move_ip(0, per_block_size)

                for point in l_bar:
                    point[1] += per_block_size

            else:
                print("JAM here for L bar ", l_bar)
                stored_block = l_bar.copy()
                list_of_blocks.append(stored_block)
                l_shape.left = ((game_table_width/9)*3+game_table_left)
                l_shape.top = game_table_top
                l_bar.clear()
                for i in [[(per_block_size * 3) + game_table_left, 0], [(per_block_size * 7) + game_table_left, 0],
                          [(per_block_size * 7) + game_table_left, per_block_size],
                          [(per_block_size * 4) + game_table_left, per_block_size],
                          [(per_block_size * 4) + game_table_left, per_block_size * 2],
                          [(per_block_size * 3) + game_table_left,
                           per_block_size * 2]]:  # [[150,15],[250,15],[250,40],[180,40],[180,80],[150,80]]
                    l_bar.append(i)
                run == 0
                break

        else:
            theblock = t_bar
            x_shape = pygame.draw.polygon(game_display, GREEN, theblock,1)
            x_shape.left = ((game_table_width / 9) * 3 + game_table_left)
            t2_shape = pygame.draw.rect(game_display, GREEN, x_shape, 1)
            pygame.draw.polygon(game_display, RED, theblock, 2)
            event_handler("t_bar",step_counter,theblock,t2_shape)
            print("ENTER T BAR")

            if t2_shape.bottom <= game_table_height:  # use t_bar(Rect object) to move
                print('within the grid')
                t2_shape.move_ip(0, per_block_size)

                step_counter += 1
                for point in theblock:
                    point[1] += per_block_size

            else:
                print('end of grid')
                stored_block = theblock.copy()
                list_of_blocks.append(stored_block)
                t_shape.left = ((game_table_width / 9) * 3 + game_table_left)
                t_shape.top = game_table_top
                theblock.clear()
                for i in [[(per_block_size*3)+game_table_left,0],
                         [(per_block_size*6)+game_table_left,0],
                         [(per_block_size*6)+game_table_left, per_block_size],
                         [(per_block_size*5)+game_table_left,per_block_size],
                         [(per_block_size*5)+game_table_left,per_block_size*2],
                         [(per_block_size*4)+game_table_left,per_block_size*2],
                         [(per_block_size*4)+game_table_left,per_block_size],
                         [(per_block_size*3)+game_table_left,per_block_size]]:
                    theblock.append(i)
                run == 0
                step_counter == 0
                break
        # event_handler()
        pygame.display.update()
        # print(l_shape.bottom)
        # print(game_table_height)
        print("inner loop")
    print("end of inner loop")
    return list_of_blocks

    # rect_l_shape.move_ip(100,0)
    # l_shape.move_ip(100,0)
    # pygame.transform.rotate(game_display,15)

    # pygame.draw.rect(game_display, RED, l_bar2, 2)
    # pygame.draw.polygon(game_display, RED, l_bar, 2)

def main():
    list_of_blocks= []
    while True :

        current_piece = random.choice(all_pieces)
        staying_blocks = draw_handler(current_piece,list_of_blocks)
        # pygame.draw.rect(game_display, GREY, game_table)
        pygame.display.update()

        print("comes here")
main()