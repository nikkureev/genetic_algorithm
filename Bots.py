import pygame
import random

# It's an experimental program. Here i tried to make a genetic algorithm.

# First step - making basic classes:
# Bots and Food
# Bots eat Food and it gives them some HP's to live longer than others
# The fatter is the better :)

# Bots have "genomes"
# It's just a list of numbers from 0 to 4 including both which indicate side to move
# Bots will loss 1 HP for 1 step and no matter what they do


class Bot():

    def __init__(self, x, y,  health_pints=50, height=1, width=1, speed=1, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1
        self.speed = 1
        self.moves = [random.randint(0, 4) for i in range(200)]
        self.health_points = 100
        self.color = color


class Food():

    def __init__(self, x, y, health_points=10, height=1, width=1,):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1
        self.health_points = 40


# Second step - making functions
# This program producing matrix where empty space marked with 0, bots with 1 and food with 5
# All moves are illustrated on a pygame black field (you can choose any other color you like :) )
# So functions should count all coordinates of bots on every step and update a pygame screen (field)

# Here we have a matrix's function
# It needs matrix's height and width


def matrix_init(matrix_width, matrix_height):
    matrix = [[0 for j in range(matrix_width)] for i in range(matrix_height)]
    return matrix

# Also we have function for generating coordinates for bots
# It's important that 2 or more bots shouldn't appear in one cell
# So i decided to make 2 lists where we will remove values when choosing them for bots
# This function needs matrix's height and width and amount of bots and food


def coordinates(amount_of_food, amount_of_bots, matrix_width, matrix_height):

    # there we make 3 lists
    # one for bots coordinates
    # one for food coordinates
    # and the last one for combine the former two
    # all coordinates should be generated together to exclude situations where bot appear in other bot or in food

    b_list, f_list, c_list = [], [], []

    choosing_list_1 = [i for i in range(0, matrix_width)]
    choosing_list_2 = [i for i in range(0, matrix_height)]

    for i in range(amount_of_food + amount_of_bots):
        nm_list = []

        nm_list.append(random.choice(choosing_list_1))
        nm_list.append(random.choice(choosing_list_2))

        choosing_list_1.remove(nm_list[0])
        choosing_list_2.remove(nm_list[1])

        c_list.append(nm_list)

    for i in range(amount_of_food):
        f_list.append(c_list[i])

    for j in range(amount_of_food, amount_of_food + amount_of_bots):
        b_list.append(c_list[j])

    c_list = []
    c_list.append(f_list)
    c_list.append(b_list)
    return c_list

# Also we have moving function
# It will count new coordinates for bots based on their "genome"


def mov_func(genome, x, y, h, w, s, i, matrix_width, matrix_height):
    mov_list = []

    # h and w it's a limitations for bot's moves
    # bots are little squares and their position on pygame field count based on their top left point
    # to illustrate them on filed we just add to this point their sizes (h and w)
    # so bots shouldn't go on last left and last bottom lines of matrix to be inside the box

    if genome[i] == 1 and x > 5:
        x -= s

    if genome[i] == 2 and x < matrix_width - w - 5:
        x += s

    if genome[i] == 3 and y > 5:
        y -= s

    if genome[i] == 4 and y < matrix_height - h - 5:
        y += s

    else:
        x += 0
        y += 0

        # if bots hit the borders of the box they should just stay at the same place they were the step before

    mov_list.append(x)
    mov_list.append(y)
    return mov_list


# Also we have function for initialization of bots and food inside algorithm cycle
# It necessary for creating new bots from survived bots using and changing their "genomes"
# or new food for new generation

def class_init(n, main_list, class_type, j):
    class_list = []

    for i in range(n):
        bot = class_type(main_list[j][i][0], main_list[j][i][1])
        class_list.append(bot)

    return class_list


# Also we have function that will change "genomes" of bots
# It takes "genomes" of survived bots and change one random move from there

def re_moves(list_of_bots, amount_of_new_bots):
    new_moves = []

    # at first we copy every parent's genome to the list of future "genomes" by many times
    # it will be a new population
    for bots in list_of_bots:
        for i in range(amount_of_new_bots):
            new_moves.append(bots.moves)

    # for the next step we take all genomes and change moves
    for i in new_moves:
        e = random.randint(0, len(list_of_bots[0].moves) - 1)
        if i[e] == 0:
            i[e] = random.choice([1, 2, 3, 4])
        if i[e] == 1:
            i[e] = random.choice([0, 2, 3, 4])
        if i[e] == 2:
            i[e] = random.choice([1, 0, 3, 4])
        if i[e] == 3:
            i[e] = random.choice([1, 2, 0, 4])
        if i[e] == 4:
            i[e] = random.choice([1, 2, 3, 0])

    return new_moves


# Here we have one of the most important function
# It will generate all coordinates and classes for new stage of algorithm

def exp_init(amount_of_bots, amount_of_food, matrix_width, matrix_height):
    all_list = []

    places_list = coordinates(amount_of_bots, amount_of_food, matrix_width, matrix_height)
    all_list.append(class_init(amount_of_bots, places_list, Bot, 0))
    all_list.append(class_init(amount_of_food, places_list, Food, 1))

    return all_list

# The third step - main function
# By using this you can change parameters and start experiment


def main(stage, matrix_width, matrix_height, k, food_list, list_of_bots, amount_of_new_bots, amount_of_survived,
         default=False):

    # for start it needs:
    # matrix sizes
    # k - size of bots on pygame field
    # (for example if k = 10 you will have bots with height and width = 10 on pygame field)
    # amount of bots
    # amount of food
    # the additional parameter "amount of survived" for future stages of algorithm
    # and "stage", design parameter, do not influence on experiment

    name = str('STAGE ' + str(stage))
    matrix = matrix_init(matrix_width, matrix_height)
    i = 0

    if default:
        new_world = re_moves(list_of_bots, amount_of_new_bots)

    run = True
    # run indicates should experiment go or not
    # it could be False if you want
    while run:
        pygame.time.delay(50)

        # generating matrix pygame illustration (field)
        win = pygame.display.set_mode((matrix_width * k, matrix_height * k))
        pygame.display.set_caption(name)

        # close field if you want
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # stage counter
        # showing on which stage you are
        i += 1

        # painting field in black
        win.fill((0, 0, 0))

        # generating food
        for food in food_list:
            matrix[food.x][food.y] = 5
            # painting food on pygame screen
            pygame.draw.rect(win, (0, 255, 0), (food.x * k, food.y * k, food.width * k, food.height * k))

        # counter for bots
        # stage should end when only few bots remain
        bots_counter = 0

        # starting to work with bots
        for bots in list_of_bots:

            # we should check bot's health points in every stage
            if bots.health_points <= 0:
                matrix[bots.x][bots.y] = 0
                del list_of_bots[bots_counter]

            # when amount of bots decrease to minimum experiment ends
            if len(list_of_bots) == amount_of_survived:
                run = False

            else:

                # parameter 1 and parameter 2 are coordinates of bots for next stage
                parameter1 = mov_func(bots.moves, bots.x, bots.y,
                                     bots.height, bots.width, bots.speed, i, matrix_width, matrix_height)[0]
                parameter2 = mov_func(bots.moves, bots.x, bots.y,
                                     bots.height, bots.width, bots.speed, i, matrix_width, matrix_height)[1]

                # checking what's in next matrix's cell
                # it could be another bot, in this case bot should just stay where it is
                # but it still loss 1 HP
                if matrix[parameter1][parameter2] == 0:
                    matrix[parameter1][parameter2] = 1
                    matrix[bots.x][bots.y] = 0
                    bots.x = parameter1
                    bots.y = parameter2
                    pygame.draw.rect(win, bots.color, (bots.x * k, bots.y * k, bots.width * k, bots.height * k))
                    bots.health_points -= 1

                # it could be food
                # in this case bot can eat it and get some HP :)
                # after eating it move on this cell
                elif matrix[parameter1][parameter2] == 5:
                    food_counter = 0
                    for food in food_list:
                        if food.x == parameter1 and food.y == parameter2:
                            matrix[parameter1][parameter2] = 0
                            del food_list[food_counter]
                        food_counter += 1

                    matrix[parameter1][parameter2] = 1
                    matrix[bots.x][bots.y] = 0
                    bots.x = parameter1
                    bots.y = parameter2
                    pygame.draw.rect(win, bots.color, (bots.x * k, bots.y * k, bots.width * k, bots.height * k))
                    bots.health_points += 40
                    bots.color = (255, 0, 0)

                # or it could be nothing
                # in this case bot just move on this cell
                else:
                    pygame.draw.rect(win, bots.color, (bots.x * k,
                                    bots.y * k, bots.width * k, bots.height * k))
                    bots.health_points -= 1

            # still counting bots for counter :)
            bots_counter += 1

            # after counting coordinates and moving pygame screen must update
        pygame.display.update()

    # when only few bots remain experiment ends
    pygame.quit()

    # there we have list of survived bots
    # lucky guys :)
    return list_of_bots


# For starting experiment we should have list which will consist of bots for new generation
# But it's empty for the first time
new_gen = []
stage_counter = 0

for i in range(10):
    if len(new_gen) == 0:
        generation = exp_init(40, 40, 100, 100)
        new_gen = main(stage_counter, 100, 100, 10, generation[1], generation[0], 5)
        stage_counter += 1
    else:
        generation = exp_init(40, 40, 100, 100)
        new_gen = main(stage_counter, 100, 100, 10, generation[1], new_gen, 5, default=True)
        stage_counter += 1
