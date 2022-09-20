
import time

import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

BALL_RADUIS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 20)

WINNING_SCORE = 5

START_TIME = 0
TIME_ROUND = 1

class Paddle(object):
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball(object):
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x, y, raduis):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.raduis = raduis
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.raduis)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        # self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"Score: {left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"Score: {right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    pygame.display.update()


def handel_paddel_movement(keys, left_paddle: Paddle, right_paddle: Paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def handel_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle):
    if ball.y + ball.raduis >= HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.raduis <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y * left_paddle.height:
            if ball.x - ball.raduis <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y * right_paddle.height:
            if ball.x + ball.raduis >= right_paddle.x:
                ball.x_velocity *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_vel

def handle_time(ball: Ball, left_paddle: Paddle, right_paddle: Paddle, duration, time_rund):
    if(duration//10 % 10 >= time_rund):
        if left_paddle.VELOCITY >= 0:
            left_paddle.VELOCITY += 1
        else:
            left_paddle.VELOCITY -= 1

        if right_paddle.VELOCITY >= 0:
            right_paddle.VELOCITY += 1
        else:
            right_paddle.VELOCITY -= 1

        if ball.x_velocity >= 0:
            ball.x_velocity += 1
        else:
            ball.x_velocity -= 1

        if ball.y_velocity >= 0:
            ball.y_velocity += 1
        else:
            ball.y_velocity -= 1
        return 1
    else:
        return 0


def main():
    global TIME_ROUND
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADUIS)

    left_score = 0
    right_score = 0

    START_TIME = time.time()

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handel_paddel_movement(keys, left_paddle, right_paddle)

        ball.move()
        handel_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            START_TIME = time.time()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            START_TIME = time.time()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Player 1 Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Player 2 Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            start_time = time.time()
            TIME_ROUND = 1

        duration = int(time.time() - START_TIME)
        TIME_ROUND +=  handle_time(ball, left_paddle, right_paddle, duration, TIME_ROUND)
        print("Time rund", TIME_ROUND)
        print("game duration", duration)
        print("left vel", left_paddle.VELOCITY)
        print("right vel", right_paddle.VELOCITY)
        print("ball x vel", ball.x_velocity)
        print("ball y vel", ball.y_velocity)

    pygame.quit()

if __name__ == "__main__":
    main()
