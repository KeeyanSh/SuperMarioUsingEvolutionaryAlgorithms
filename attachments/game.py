import sys
import pygame
from pygame import QUIT

from attachments.EA import Game

levels = ['__M_____',
          '____G_____',
          '__G___L_',
          '__G__G_L___',
          '____G_ML__G_',
          '____G_MLGL_G_',
          '_M_M_GM___LL__G__L__G_M__',
          '____G_G_MMM___L__L_G_____G___M_L__G__L_GM____L____',
          '___M____MGM________M_M______M____L___G____M____L__G__GM__L____ML__G___G___L___G__G___M__L___G____M__',
          '_G___M_____LL_____G__G______L_____G____MM___G_G____LML____G___L____LMG___G___GML______G____L___MG___']
str = levels[7]

# g = Game(levels=[str], initial_population_size=200, calculate_win_prize=True, p_crossover=0.8, p_mutation=0.1,
#           use_roulette_wheel=False,cross_over_points=1)
g = Game(levels=[str], initial_population_size=500, calculate_win_prize=False, p_crossover=0.8, p_mutation=0.5,
         use_roulette_wheel=True, cross_over_points=2)

g.load_next_level()
cc = g.process()
print(cc)
actions = list(cc)

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Super Mario')
w, h = 1000, 500
screen = pygame.display.set_mode((w, h))

# assets
block = pygame.image.load('../assets/block.png')
block2 = pygame.image.load('../assets/block2.png')
M = pygame.image.load('../assets/M.png')
G = pygame.image.load('../assets/G.png')
L = pygame.image.load('../assets/L.png')
flag = pygame.image.load('../assets/flag.png')
M = pygame.transform.scale(M, (60, 60))
G = pygame.transform.scale(G, (60, 60))
L = pygame.transform.scale(L, (60, 100))
flag = pygame.transform.scale(flag, (80, 200))
walk1 = pygame.image.load('../assets/walk1.png')
walk2 = pygame.image.load('../assets/walk2.png')
walk1 = pygame.transform.scale(walk1, (58, 88))
walk2 = pygame.transform.scale(walk2, (75, 100))
jump = pygame.image.load('../assets/jump.png')
jump = pygame.transform.scale(jump, (67, 97))
sit = pygame.image.load('../assets/sit.png')
sit = pygame.transform.scale(sit, (80, 70))
kill = pygame.image.load('../assets/kill.png')
kill = pygame.transform.scale(kill, (70, 80))
G_dead = pygame.image.load('../assets/G_dead.png')
G_dead = pygame.transform.scale(G_dead, (80, 75))


def plot():
    import matplotlib.pyplot as plt
    plot1 = plt.subplot(3, 1, 1)
    plot2 = plt.subplot(3, 1, 2)
    plot3 = plt.subplot(3, 1, 3)
    plot1.set_title('Max Fitness')
    plot2.set_title('Average Fitness')
    plot3.set_title('Min Fitness')
    xpoints = [i for i in range(len(g.max_fitnesses))]
    plot1.plot(xpoints, g.max_fitnesses)
    plot2.plot(xpoints, g.average_fitnesses)
    plot3.plot(xpoints, g.min_fitnesses)
    plt.tight_layout()
    plt.show()


def display(index):
    if index == len(str):
        plot()
        sys.exit()

    screen.fill((96, 202, 209))

    for i in range(index, 100):
        if i % 4:
            screen.blit(block, ((i - index) * 100, 400))
        else:
            screen.blit(block2, ((i - index) * 100, 400))

        if i >= len(str):
            continue
        if i == len(str) - 1:
            screen.blit(flag, ((i - index) * 100 + 18, 215))

        if str[i] == 'M':
            screen.blit(M, ((i - index) * 100 + 20, 345))
        elif str[i] == 'L':
            screen.blit(L, ((i - index) * 100 + 20, 240))
        elif str[i] == 'G':
            if i == index and index > 1 and actions[index - 2] == '1':
                screen.blit(G_dead, (10, 345))
            else:
                screen.blit(G, ((i - index) * 100 + 20, 345))

    if index and actions[index - 1] == '1':
        screen.blit(jump, (10, 230))
    elif index and actions[index - 1] == '2':
        screen.blit(sit, (10, 335))
    elif index > 1 and actions[index - 2] == '1' and str[index] == 'G':
        screen.blit(kill, (10, 306))

    else:
        if index % 2:
            screen.blit(walk1, (10, 315))
        else:
            screen.blit(walk2, (10, 310))


# update display
i = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display(i)
    pygame.display.update()
    i += 1
    clock.tick(2)
