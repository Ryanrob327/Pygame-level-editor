import pygame
import button
import csv

pygame.init()
clock = pygame.time.Clock()

#game window
screen_width = 800
screen_height = 608
lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((screen_width + side_margin, screen_height + lower_margin))
pygame.display.set_caption('Level Editor')

#colors
white = (255,255,255)
blue = (0,0,255)
light_blue = (130,200,200)
red = (255,0,0)
black = (0,0,0)

#fonts
font = pygame.font.SysFont('futura', 30)

#variables
max_rows = 150
max_cols = 150
tile_size = 32
tile_types = 23
current_tile = 0

level = 0

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
x_scroll = 0
y_scroll = 0
scroll_speed = 1

#images
save_img = pygame.image.load('save_btn.png').convert_alpha()
load_img = pygame.image.load('load_btn.png').convert_alpha()
#import tile list
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'Tileset - top down/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

#create empty tile list
world_data = []
for row in range(max_rows):
    r = [-1] * max_cols
    world_data.append(r)


#create text function
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))


#functions
#draw grid
def draw_grid():
    #vertical lines
    for c in range(max_cols + 1):
        pygame.draw.line(screen, white, (c * tile_size - x_scroll, 0), (c * tile_size - x_scroll, screen_height))
    #horizontal lines
    for i in range(max_rows + 1):
        pygame.draw.line(screen, white, (0, (-i * tile_size - y_scroll) + screen_height), (screen_width, (-i * tile_size - y_scroll) + screen_height))

#draw tiles on map
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * tile_size - x_scroll, (y-131) * tile_size - y_scroll))

#create buttons
save_button = button.Button(screen_width // 2, screen_height + lower_margin - 50, save_img, 1)
load_button = button.Button(screen_width // 2 + 200, screen_height + lower_margin - 50,load_img, 1)
#buttons
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(screen_width + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:
    screen.fill(light_blue)

    draw_grid()
    draw_world()

    # draw tile panel and tiles
    pygame.draw.rect(screen, light_blue, (screen_width, 0, side_margin, screen_height))
    pygame.draw.rect(screen, light_blue, (0, screen_height, screen_width + side_margin, lower_margin))

    draw_text(f'Level: {level}', font, black, 10, screen_height + lower_margin - 90)
    draw_text('press PgUp or PgDn to change level', font, black, 10, screen_height + lower_margin - 60)

    #save and load data
    if save_button.draw(screen):
        with open(f'Levels - topdown/level{level}_data_topdown.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        x_scroll = 0
        y_scroll = 0
        with open(f'Levels - topdown/level{level}_data_topdown.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    #highlight selected tile
    pygame.draw.rect(screen, red, button_list[current_tile].rect, 2)

    #scroll map
    if scroll_left == True and x_scroll > 0:
        x_scroll -= 5 * scroll_speed
    if scroll_right == True and x_scroll < (max_cols * tile_size) - screen_width:
        x_scroll += 5 * scroll_speed
    if scroll_down == True and y_scroll < 0:
        y_scroll += 5 * scroll_speed
    if scroll_up == True and y_scroll < (max_rows * tile_size) - screen_height:
        y_scroll -= 5 * scroll_speed

    #add new tiles to map
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + x_scroll) // tile_size
    y = (pos[1] + y_scroll) // tile_size + 131

    #check that coordinates are within drawing area
    if pos[0] < screen_width and pos[1] < screen_height:
        #update tile value
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                level += 1
            if event.key == pygame.K_PAGEDOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1


    pygame.display.update()
    clock.tick(60)

pygame.quit()