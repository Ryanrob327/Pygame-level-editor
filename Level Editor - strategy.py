import pygame
import button
import csv


pygame.init()
clock = pygame.time.Clock()

#game window
screen_width = 832
screen_height = 576
lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((screen_width + side_margin, screen_height + lower_margin))
pygame.display.set_caption('Level Editor')

#colors
white = (255,255,255)
blue = (0,0,255)
highlight_lvl1 = (20, 66, 114)
background_color = (10, 38, 71)
red = (255,0,0)
black = (0,0,0)

#fonts
font = pygame.font.SysFont('futura', 30)

#variables
max_rows = 150
max_cols = 150
tile_size = 64
tile_types = 29
current_tile = 0

level = 0

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
x_scroll = 0
y_scroll = 0
scroll_speed = 1
margin_scroll = 0

#images
save_img = pygame.image.load('save_btn.png').convert_alpha()
load_img = pygame.image.load('load_btn.png').convert_alpha()
highlight = pygame.image.load('highlight.png').convert_alpha()


#import tile list
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'Tileset - strategy/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

# create empty tile list with 150 nested arrays and 150 values to each array representing a 150x150 grid
world_data = [] # Empty 2D array that represents data in level
for row in range(max_rows):
    r = [-1] * max_cols
    world_data.append(r) # Each loop adds a new nested array with 150 "-1" values


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

# draws tiles on map
def draw_world():
    for y, row in enumerate(world_data): # iterate through nested lists representing y-axis
        for x, tile in enumerate(row): # iterate through values inside nested lists representing x-axis
            if tile >= 0:
                # display tile on screen at (x,y) coordinates
                screen.blit(img_list[tile], (x * tile_size - x_scroll, (y-131) * tile_size - y_scroll))

# updates map when tiles placed or removed
def update_world(mouse_x, mouse_y, current_tile, place_tile):
    # checks if tile is placed
    if place_tile == True:
        # enumerates through world_data to find the selected tile
        for y, row in enumerate(world_data):
            if y == mouse_y:
                for x, tile in enumerate(row):
                    if x == mouse_x:
                        # places tile
                        world_data[mouse_y][mouse_x] = current_tile
    # checks if tile is removed
    else:
        # removes tile
        world_data[mouse_y][mouse_x] = -1


#create buttons
save_button = button.Button(screen_width // 2, screen_height + lower_margin - 50, save_img, 1)
load_button = button.Button(screen_width // 2 + 200, screen_height + lower_margin - 50,load_img, 1)

#buttons
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(screen_width + (75 * button_col) + 50, 75 * button_row, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

# main loop, runs every frame
run = True
while run:
    # background blue color
    screen.fill(highlight_lvl1)

    # draws white grid lines and tiles in the level
    draw_grid()
    draw_world()

    # draw tile panel and tiles
    pygame.draw.rect(screen, background_color, (screen_width + 1, 0, side_margin, screen_height + 1))
    pygame.draw.rect(screen, background_color, (0, screen_height + 1, screen_width + side_margin, lower_margin))

    draw_text(f'Level: {level}', font, white, 10, screen_height + lower_margin - 90)
    draw_text('press PgUp or PgDn to change level', font, white, 10, screen_height + lower_margin - 60)

    #save and load data
    if save_button.draw(screen):
        with open(f'Levels - strategy/level{level}_data_strategy.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen): # if load button clicked
        # reset scroll
        x_scroll = 0
        y_scroll = 0
        # convert csv file format to a 2d array format
        with open(f'Levels - strategy/level{level}_data_strategy.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            # iterate through 2d array and replace tiles in world_data with tiles from csv reader
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        # update display with new data
        draw_world()

    #choose a tile
    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight selected tile
    screen.blit(highlight, button_list[current_tile].rect)
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
        if pygame.mouse.get_pressed()[0]: # left mouse
            update_world(x, y, current_tile, True)
        if pygame.mouse.get_pressed()[2]: # right mouse
            update_world(x, y, current_tile, False)


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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #scroll up
                margin_scroll += 10
            elif event.button == 5: #scroll down
                margin_scroll -= 10


    pygame.display.update()
    clock.tick(60)

pygame.quit()