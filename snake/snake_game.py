import pygame
import random
import time

pygame.init()

pygame.mixer.init()

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
bright_green_head = (0, 255, 50)
blue = (0, 0, 255)
dark_blue = (0, 0, 200)
bright_blue_head = (50, 50, 255)
black = (0, 0, 0)
grey = (50, 50, 50)

window_x = 720
window_y = 480

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Python Snake Game")

try:
    apple_img = pygame.image.load('apple.png').convert_alpha()
    apple_img = pygame.transform.scale(apple_img, (10, 10))

    eat_sound = pygame.mixer.Sound('eat_sound.wav')
    game_over_sound = pygame.mixer.Sound('game_over_sound.wav')
except pygame.error as e:
    print(f"Error loading assets: {e}")
    print("Please ensure 'apple.png', 'eat_sound.wav', and 'game_over_sound.wav' are in the same directory as the script.")
    pygame.quit()
    quit()

fps_controller = pygame.time.Clock()
snake_speed = 15

game_state = 'menu'
menu_selection = 0

snake1_position = [100, 50]
snake1_body = [[100, 50], [90, 50], [80, 50]]
snake1_direction = 'RIGHT'
snake1_change_to = 'RIGHT'
snake1_score = 0
snake1_alive = True

snake2_position = [600, 400]
snake2_body = [[600, 400], [610, 400], [620, 400]]
snake2_direction = 'LEFT'
snake2_change_to = 'LEFT'
snake2_score = 0
snake2_alive = True

food_position = [random.randrange(1, (window_x // 10)) * 10,
                 random.randrange(1, (window_y // 10)) * 10]
food_spawn = True

def reset_game_variables():
    global snake1_position, snake1_body, snake1_direction, snake1_change_to, snake1_score, snake1_alive
    global snake2_position, snake2_body, snake2_direction, snake2_change_to, snake2_score, snake2_alive
    global food_position, food_spawn

    snake1_position = [100, 50]
    snake1_body = [[100, 50], [90, 50], [80, 50]]
    snake1_direction = 'RIGHT'
    snake1_change_to = 'RIGHT'
    snake1_score = 0
    snake1_alive = True

    snake2_position = [600, 400]
    snake2_body = [[600, 400], [610, 400], [620, 400]]
    snake2_direction = 'LEFT'
    snake2_change_to = 'LEFT'
    snake2_score = 0
    snake2_alive = True

    food_position = [random.randrange(1, (window_x // 10)) * 10,
                     random.randrange(1, (window_y // 10)) * 10]
    food_spawn = True


def display_message(message, color, font, size, x, y):
    font_obj = pygame.font.SysFont(font, size)
    text_surface = font_obj.render(message, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    game_window.blit(text_surface, text_rect)

def show_scores(mode):
    if mode == 'single_player':
        score_font = pygame.font.SysFont('consolas', 20)
        score_surface = score_font.render('Score : ' + str(snake1_score), True, white)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (window_x / 10, 15)
        game_window.blit(score_surface, score_rect)
    elif mode == 'two_player':
        score_font = pygame.font.SysFont('consolas', 20)
        p1_score_surface = score_font.render('P1 Score : ' + str(snake1_score), True, green)
        p1_score_rect = p1_score_surface.get_rect()
        p1_score_rect.midtop = (window_x / 10, 15)
        game_window.blit(p1_score_surface, p1_score_rect)

        p2_score_surface = score_font.render('P2 Score : ' + str(snake2_score), True, blue)
        p2_score_rect = p2_score_surface.get_rect()
        p2_score_rect.midtop = (window_x - (window_x / 10), 15)
        game_window.blit(p2_score_surface, p2_score_rect)


def game_over(loser_snake=None, mode='single_player'):
    global game_state
    game_over_sound.play()
    game_state = 'game_over'

    game_window.fill(black)

    if mode == 'single_player':
        display_message('GAME OVER!', red, 'times new roman', 70, window_x / 2, window_y / 3)
        display_message('Your Score is : ' + str(snake1_score), white, 'times new roman', 40, window_x / 2, window_y / 2)
    elif mode == 'two_player':
        if loser_snake == 'P1':
            display_message('PLAYER 1 LOST!', red, 'times new roman', 60, window_x / 2, window_y / 3)
            display_message('PLAYER 2 WINS!', blue, 'times new roman', 60, window_x / 2, window_y / 3 + 70)
        elif loser_snake == 'P2':
            display_message('PLAYER 2 LOST!', red, 'times new roman', 60, window_x / 2, window_y / 3)
            display_message('PLAYER 1 WINS!', green, 'times new roman', 60, window_x / 2, window_y / 3 + 70)
        else:
            display_message('DOUBLE COLLISION!', red, 'times new roman', 60, window_x / 2, window_y / 3)


    display_message('Press R to Restart or M for Menu', white, 'times new roman', 25, window_x / 2, window_y / 4 * 3)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_input = False
                    reset_game_variables()
                    if mode == 'single_player':
                        main_game_loop('single_player')
                    else:
                        main_game_loop('two_player')
                if event.key == pygame.K_m:
                    waiting_for_input = False
                    game_state = 'menu'
                    reset_game_variables()


def draw_menu():
    global menu_selection

    game_window.fill(black)
    display_message("SNAKE GAME", white, 'times new roman', 80, window_x / 2, window_y / 3)

    play_color = green if menu_selection == 0 else white
    two_player_color = green if menu_selection == 1 else white

    display_message("Play", play_color, 'consolas', 40, window_x / 2, window_y / 2 + 50)
    display_message("2 Player", two_player_color, 'consolas', 40, window_x / 2, window_y / 2 + 120)

    display_message("Use UP/DOWN to select, ENTER to confirm", grey, 'consolas', 20, window_x / 2, window_y - 30)

    pygame.display.update()


def main_game_loop(mode):
    global game_state, snake1_position, snake1_body, snake1_direction, snake1_change_to, snake1_score, snake1_alive
    global snake2_position, snake2_body, snake2_direction, snake2_change_to, snake2_score, snake2_alive
    global food_position, food_spawn

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake1_change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    snake1_change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    snake1_change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    snake1_change_to = 'RIGHT'

                if mode == 'two_player':
                    if event.key == pygame.K_w:
                        snake2_change_to = 'UP'
                    if event.key == pygame.K_s:
                        snake2_change_to = 'DOWN'
                    if event.key == pygame.K_a:
                        snake2_change_to = 'LEFT'
                    if event.key == pygame.K_d:
                        snake2_change_to = 'RIGHT'


        if snake1_alive:
            if snake1_change_to == 'UP' and snake1_direction != 'DOWN':
                snake1_direction = 'UP'
            if snake1_change_to == 'DOWN' and snake1_direction != 'UP':
                snake1_direction = 'DOWN'
            if snake1_change_to == 'LEFT' and snake1_direction != 'RIGHT':
                snake1_direction = 'LEFT'
            if snake1_change_to == 'RIGHT' and snake1_direction != 'LEFT':
                snake1_direction = 'RIGHT'

            if snake1_direction == 'UP':
                snake1_position[1] -= 10
            if snake1_direction == 'DOWN':
                snake1_position[1] += 10
            if snake1_direction == 'LEFT':
                snake1_position[0] -= 10
            if snake1_direction == 'RIGHT':
                snake1_position[0] += 10

            snake1_body.insert(0, list(snake1_position))

            if snake1_position[0] == food_position[0] and snake1_position[1] == food_position[1]:
                snake1_score += 10
                food_spawn = False
                eat_sound.play()
            else:
                snake1_body.pop()

        if mode == 'two_player' and snake2_alive:
            if snake2_change_to == 'UP' and snake2_direction != 'DOWN':
                snake2_direction = 'UP'
            if snake2_change_to == 'DOWN' and snake2_direction != 'UP':
                snake2_direction = 'DOWN'
            if snake2_change_to == 'LEFT' and snake2_direction != 'RIGHT':
                snake2_direction = 'LEFT'
            if snake2_change_to == 'RIGHT' and snake2_direction != 'LEFT':
                snake2_direction = 'RIGHT'

            if snake2_direction == 'UP':
                snake2_position[1] -= 10
            if snake2_direction == 'DOWN':
                snake2_position[1] += 10
            if snake2_direction == 'LEFT':
                snake2_position[0] -= 10
            if snake2_direction == 'RIGHT':
                snake2_position[0] += 10

            snake2_body.insert(0, list(snake2_position))

            if snake2_position[0] == food_position[0] and snake2_position[1] == food_position[1]:
                snake2_score += 10
                food_spawn = False
                eat_sound.play()
            else:
                snake2_body.pop()


        if not food_spawn:
            while True:
                new_food_pos = [random.randrange(1, (window_x // 10)) * 10,
                                 random.randrange(1, (window_y // 10)) * 10]
                collision_with_snake = False
                for pos in snake1_body:
                    if new_food_pos == pos:
                        collision_with_snake = True
                        break
                if mode == 'two_player' and not collision_with_snake:
                    for pos in snake2_body:
                        if new_food_pos == pos:
                            collision_with_snake = True
                            break
                if not collision_with_snake:
                    food_position = new_food_pos
                    break
            food_spawn = True


        game_window.fill(black)

        for x in range(0, window_x, 10):
            pygame.draw.line(game_window, grey, (x, 0), (x, window_y))
        for y in range(0, window_y, 10):
            pygame.draw.line(game_window, grey, (0, y), (window_x, y))

        if snake1_alive:
            for i, pos in enumerate(snake1_body):
                if i == 0:
                    pygame.draw.rect(game_window, bright_green_head, pygame.Rect(pos[0], pos[1], 10, 10))
                else:
                    if i % 2 == 0:
                        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
                    else:
                        pygame.draw.rect(game_window, dark_green, pygame.Rect(pos[0], pos[1], 10, 10))
                    pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1], 10, 10), 1)

        if mode == 'two_player' and snake2_alive:
            for i, pos in enumerate(snake2_body):
                if i == 0:
                    pygame.draw.rect(game_window, bright_blue_head, pygame.Rect(pos[0], pos[1], 10, 10))
                else:
                    if i % 2 == 0:
                        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
                    else:
                        pygame.draw.rect(game_window, dark_blue, pygame.Rect(pos[0], pos[1], 10, 10))
                    pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1], 10, 10), 1)


        if snake1_alive or snake2_alive:
            game_window.blit(apple_img, food_position)

        p1_collision = False
        p2_collision = False

        if snake1_alive:
            if snake1_position[0] < 0 or snake1_position[0] > window_x - 10 or \
               snake1_position[1] < 0 or snake1_position[1] > window_y - 10:
                p1_collision = True
            for block in snake1_body[1:]:
                if snake1_position[0] == block[0] and snake1_position[1] == block[1]:
                    p1_collision = True
            if mode == 'two_player' and snake2_alive:
                for block in snake2_body:
                    if snake1_position[0] == block[0] and snake1_position[1] == block[1]:
                        p1_collision = True
            if p1_collision:
                snake1_alive = False

        if mode == 'two_player' and snake2_alive:
            if snake2_position[0] < 0 or snake2_position[0] > window_x - 10 or \
               snake2_position[1] < 0 or snake2_position[1] > window_y - 10:
                p2_collision = True
            for block in snake2_body[1:]:
                if snake2_position[0] == block[0] and snake2_position[1] == block[1]:
                    p2_collision = True
            for block in snake1_body:
                if snake2_position[0] == block[0] and snake2_position[1] == block[1]:
                    p2_collision = True
            if p2_collision:
                snake2_alive = False

        if mode == 'single_player':
            if not snake1_alive:
                game_over(mode='single_player')
                running = False
        elif mode == 'two_player':
            if not snake1_alive and snake2_alive:
                game_over(loser_snake='P1', mode='two_player')
                running = False
            elif snake1_alive and not snake2_alive:
                game_over(loser_snake='P2', mode='two_player')
                running = False
            elif not snake1_alive and not snake2_alive:
                game_over(loser_snake=None, mode='two_player')
                running = False

        if mode == 'two_player' and not snake1_alive and not snake2_alive:
            game_over(loser_snake=None, mode='two_player')
            running = False


        show_scores(mode)

        pygame.display.update()
        fps_controller.tick(snake_speed)

    if game_state != 'menu' and game_state != 'quit':
        pass

while True:
    if game_state == 'menu':
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % 2
                if event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % 2
                if event.key == pygame.K_RETURN:
                    reset_game_variables()
                    if menu_selection == 0:
                        game_state = 'single_player'
                        main_game_loop('single_player')
                    elif menu_selection == 1:
                        game_state = 'two_player'
                        main_game_loop('two_player')

    elif game_state == 'single_player':
        pass

    elif game_state == 'two_player':
        pass

    elif game_state == 'game_over':
        pass