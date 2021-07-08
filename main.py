import pygame
import random


class Board:
    def __init__(self):
        self.board = (17, 15)
        self.snake = Snake()
        self.food = Food()
        self.score = Score()

    def update_board(self, xdir, ydir, surface):
        if xdir == 0 and ydir == 0:
            self.draw(surface)
            return 'running'
        collision, snake_next_pos = self.snake.get_next_head(xdir, ydir, self.board[0], self.board[1])
        if snake_next_pos == self.food.get_food_pos():
            self.snake.grow(snake_next_pos)
            self.score.update_score()
            self.draw(surface)
            if self.food.gen_food(self.snake.get_body(), self.board[0], self.board[1]):
                return 'running'
            else:
                self.win(surface)
                return 'win'
        elif collision:
            self.game_over(surface)
            return 'lose'
        self.snake.update_pos(snake_next_pos)
        self.draw(surface)
        return 'running'

    def draw(self, surface):
        # score
        font_colour = (255, 255, 255)
        score_font = pygame.font.Font('freesansbold.ttf', 32)
        score_text = score_font.render('Score: ' + str(self.score.get_score()), True, font_colour)
        score_pos = (10, 10)
        screen.blit(score_text, score_pos)

        # board outline
        border_colour = (255, 255, 255)
        pygame.draw.rect(surface, border_colour, pygame.Rect(40-2, 52-2, 820, 724), 2)

        # food
        food_colour = (255, 0, 0)
        food_board_pos = self.food.get_food_pos()
        food_xpos = 40 + food_board_pos[0]*48 + 2
        food_ypos = 52 + food_board_pos[1]*48 + 2
        pygame.draw.rect(surface, food_colour, pygame.Rect(food_xpos, food_ypos, 44, 44))

        # snake
        snake_colour_body = (192, 192, 192)
        snake_colour_head = (255, 255, 255)
        snake_board_pos = self.snake.get_body()
        for i in range(len(snake_board_pos)):
            snake_xpos = 40 + snake_board_pos[i][0]*48 + 2
            snake_ypos = 52 + snake_board_pos[i][1]*48 + 2
            if i == len(snake_board_pos)-1:
                pygame.draw.rect(surface, snake_colour_head, pygame.Rect(snake_xpos, snake_ypos, 44, 44))
            else:
                pygame.draw.rect(surface, snake_colour_body, pygame.Rect(snake_xpos, snake_ypos, 44, 44))

    def game_over(self, surface):
        # score
        font_colour = (255, 255, 255)
        score_font = pygame.font.Font('freesansbold.ttf', 32)
        score_text = score_font.render('Score: ' + str(self.score.get_score()), True, font_colour)
        score_pos = (10, 10)
        screen.blit(score_text, score_pos)

        # board outline
        border_colour = (255, 255, 255)
        pygame.draw.rect(surface, border_colour, pygame.Rect(40 - 2, 52 - 2, 820, 724), 2)

        # game over
        font_colour = (255, 255, 255)
        finish_font = pygame.font.Font('freesansbold.ttf', 32)
        finish_text = finish_font.render('Game Over', True, font_colour)
        finish_text_rect = finish_text.get_rect(center=(450, 400))
        screen.blit(finish_text, finish_text_rect)

        # reset button
        button_colour = (255, 255, 255)
        pygame.draw.rect(screen, button_colour, pygame.Rect(350, 501, 200, 54))
        reset_colour = (0, 0, 0)
        reset_font = pygame.font.Font('freesansbold.ttf', 32)
        reset_text = reset_font.render('Reset', True, reset_colour)
        reset_text_rect = reset_text.get_rect(center=(450, 528))
        screen.blit(reset_text, reset_text_rect)

    def win(self, surface):
        # score
        font_colour = (255, 255, 255)
        score_font = pygame.font.Font('freesansbold.ttf', 32)
        score_text = score_font.render('Score: ' + str(self.score.get_score()), True, font_colour)
        score_pos = (10, 10)
        screen.blit(score_text, score_pos)

        # board outline
        border_colour = (255, 255, 255)
        pygame.draw.rect(surface, border_colour, pygame.Rect(40 - 2, 52 - 2, 820, 724), 2)

        # congratulation
        font_colour = (255, 255, 255)
        finish_font = pygame.font.Font('freesansbold.ttf', 32)
        finish_text = finish_font.render('Congratulations', True, font_colour)
        finish_text_rect = finish_text.get_rect(center=(450, 400))
        screen.blit(finish_text, finish_text_rect)

        # reset button
        button_colour = (255, 255, 255)
        pygame.draw.rect(screen, button_colour, pygame.Rect(350, 501, 200, 54))
        reset_colour = (0, 0, 0)
        reset_font = pygame.font.Font('freesansbold.ttf', 32)
        reset_text = reset_font.render('Reset', True, reset_colour)
        reset_text_rect = reset_text.get_rect(center=(450, 528))
        screen.blit(reset_text, reset_text_rect)


class Snake:
    def __init__(self):
        self.pos = [(2, 7), (3, 7), (4, 7)]

    def get_snake_length(self):
        return len(self.pos)

    def get_head(self):
        return self.pos[-1]

    def get_body(self):
        return self.pos

    def get_next_head(self, xdir, ydir, xbound, ybound):
        cur_head = self.get_head()
        new_head = (cur_head[0] + xdir, cur_head[1] + ydir)

        # check for collisions
        if new_head in self.pos or new_head[0] >= xbound or new_head[1] >= ybound or new_head[0] < 0 or new_head[1] < 0:
            return True, new_head
        return False, new_head

    def update_pos(self, new_head):
        self.pos.pop(0)
        self.pos.append(new_head)

    def grow(self, new_head):
        self.pos.append(new_head)


class Food:
    def __init__(self):
        self.pos = (12, 7)

    def get_food_pos(self):
        return self.pos

    def gen_food(self, snake_body, xbound, ybound):
        food_pos = []
        for i in range(xbound):
            for j in range(ybound):
                cur_pos = (i, j)
                if cur_pos not in snake_body:
                    food_pos.append(cur_pos)
        if len(food_pos) == 0:
            return False
        self.pos = food_pos[random.randint(0, len(food_pos)-1)]
        return True


class Score:
    def __init__(self):
        self.score = 0

    def get_score(self):
        return self.score

    def update_score(self):
        self.score += 1


# initialisation
pygame.init()
screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load('snake.png'))
clock = pygame.time.Clock()

# initialise the board
game_board = Board()
status = 'running'
x_dir = 0
y_dir = 0

# game loop
running = True
while running:
    # clear the screen
    screen.fill((0, 0, 0))

    # check for events
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False

        # check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and (x_dir != 1 or y_dir != 0) and (x_dir != 0 or y_dir != 0):
                x_dir = -1
                y_dir = 0
            elif event.key == pygame.K_RIGHT and (x_dir != -1 or y_dir != 0):
                x_dir = 1
                y_dir = 0
            elif event.key == pygame.K_UP and (x_dir != 0 or y_dir != 1):
                x_dir = 0
                y_dir = -1
            elif event.key == pygame.K_DOWN and (x_dir != 0 or y_dir != -1):
                x_dir = 0
                y_dir = 1

        # check if the reset button is clicked
        if (status == 'lose' or status == 'win') and event.type == pygame.MOUSEBUTTONUP:
            game_board = Board()
            status = 'running'
            x_dir = 0
            y_dir = 0

    # update the screen
    if status == 'lose':
        game_board.game_over(screen)
    elif status == 'win':
        game_board.win(screen)
    else:
        status = game_board.update_board(x_dir, y_dir, screen)

    pygame.display.update()
    clock.tick(10)
