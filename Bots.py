import pygame
import random
import sys


class Bot():

    def __init__(self, x, y,  helth_pints = 50, height=1, width=1, speed=1, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1
        self.speed = 1
        self.moves = [random.randint(0, 4) for i in range(200)]
        self.helth_points = 100
        self.color = color


class Food():

    def __init__(self, x, y, helth_points=10, height=1, width=1,):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1
        self.helth_points = 40


def matrix_init(matrix_width, matrix_height):
    matrix = [[0 for j in range(matrix_width)] for i in range(matrix_height)]
    return matrix


def coordinates(n, m, matrix_width, matrix_height):
    c_list, n_list, m_list = [], [], []
    choising_list_1 = [i for i in range(0, matrix_width)]
    choising_list_2 = [i for i in range(0, matrix_height)]
    for i in range(n + m):
        nm_list = []
        nm_list.append(random.choice(choising_list_1))
        nm_list.append(random.choice(choising_list_2))
        choising_list_1.remove(nm_list[0])
        choising_list_2.remove(nm_list[1])
        c_list.append(nm_list)
    for i in range(n):
        n_list.append(c_list[i])
    for j in range(n, n + m):
        m_list.append(c_list[j])
    c_list = []
    c_list.append(n_list)
    c_list.append(m_list)
    return c_list


def mov_func(list, x, y, h, w, s, i, matrix_width, matrix_height):
    mov_list = []
    if list[i] == 1 and x > 5:
        x -= s

    if list[i] == 2 and x < matrix_width - w - 5:
        x += s

    if list[i] == 3 and y > 5:
        y -= s

    if list[i] == 4 and y < matrix_height - h - 5:
        y += s

    else:
        x += 0
        y += 0

    mov_list.append(x)
    mov_list.append(y)
    return mov_list


def class_init(n, main_list, class_type, j):
    class_list = []
    for i in range(n):
        bot = class_type(main_list[j][i][0], main_list[j][i][1])
        class_list.append(bot)
    return class_list


def re_moves(list, amount_of_new_bots):
    new_moves = []
    for bots in list:
        for i in range(amount_of_new_bots):
            new_moves.append(bots.moves)
    for i in new_moves:
        e = random.randint(0, len(list[0].moves) - 1)
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


def exp_init(amount_of_bots, amount_of_food, matrix_width, matrix_height):
    all_list = []
    plases_list = coordinates(amount_of_bots, amount_of_food, matrix_width, matrix_height)
    all_list.append(class_init(amount_of_bots, plases_list, Bot, 0))
    all_list.append(class_init(amount_of_food, plases_list, Food, 1))
    return all_list


def main(stage, matrix_width, matrix_height, k, food_list, list_of_bots, amount_of_surv):
    name = str('STAGE ' + str(stage))
    matrix = matrix_init(matrix_width, matrix_height)
    i = 0


    run = True
    while run:
        pygame.time.delay(50)

        win = pygame.display.set_mode((matrix_width * k, matrix_height * k))
        pygame.display.set_caption(name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        i += 1

        win.fill((0, 0, 0))

        for food in food_list:
            matrix[food.x][food.y] = 5
            pygame.draw.rect(win, (0, 255, 0), (food.x * k, food.y * k, food.width * k, food.height * k))

        bots_counter = 0
        for bots in list_of_bots:
            if bots.helth_points <= 0:
                matrix[bots.x][bots.y] = 0
                del list_of_bots[bots_counter]

            else:
                parametr1 = mov_func(bots.moves, bots.x, bots.y,
                                     bots.height, bots.width, bots.speed, i, matrix_width, matrix_height)[0]
                parametr2 = mov_func(bots.moves, bots.x, bots.y,
                                     bots.height, bots.width, bots.speed, i, matrix_width, matrix_height)[1]

                if matrix[parametr1][parametr2] == 0:
                    matrix[parametr1][parametr2] = 1
                    matrix[bots.x][bots.y] = 0
                    bots.x = parametr1
                    bots.y = parametr2
                    pygame.draw.rect(win, bots.color, (bots.x * k, bots.y * k, bots.width * k, bots.height * k))
                    bots.helth_points -= 1

                elif matrix[parametr1][parametr2] == 5:
                    food_counter = 0
                    for food in food_list:
                        if food.x == parametr1 and food.y == parametr2:
                            matrix[parametr1][parametr2] = 0
                            del food_list[food_counter]
                        food_counter += 1

                    matrix[parametr1][parametr2] = 1
                    matrix[bots.x][bots.y] = 0
                    bots.x = parametr1
                    bots.y = parametr2
                    pygame.draw.rect(win, bots.color, (bots.x * k, bots.y * k, bots.width * k, bots.height * k))
                    bots.helth_points += 40
                    bots.color = (255, 0, 0)

                else:
                    pygame.draw.rect(win, bots.color, (bots.x * k,
                                    bots.y * k, bots.width * k, bots.height * k))
                    bots.helth_points -= 1


            pygame.display.update()

            bots_counter += 1

    pygame.quit()

    return list_of_bots


new_gen = []
stage_counter = 0

for i in range(10):
    if len(new_gen) == 0:
        generation = exp_init(40, 40, 100, 100)
        new_gen = main(stage_counter, 100, 100, 10, generation[1], generation[0], 5)
        stage_counter += 1
    else:
        generation = exp_init(40, 40, 100, 100)
        new_gen = main(stage_counter, 100, 100, 10, generation[1], new_gen, 5)
        stage_counter += 1
    print(new_gen)
