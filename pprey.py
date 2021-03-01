import random

def in_snake(snake, x, y) :
    for block in snake.blocks :
        if (x<block.rect.right and x> block.rect.left) and (y<block.rect.bottom and x> block.rect.top) :
            return True
    return False

def place_prey(snake,w,h) :
    x=random.randrange(5,w-5,step=10)
    y=random.randrange(5,h-5,step=10)
    while in_snake(snake, x, y) :
        x=random.randrange(5,w-5,step=10)
        y=random.randrange(5,h-5,step=10)

    return x,y