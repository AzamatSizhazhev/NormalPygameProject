import random
import pygame
from board import BOARD

pygame.init()
size = width, height = 700, 600
screen = pygame.display.set_mode(size)

arial_font = pygame.font.match_font('arial')
arial_font_48 = pygame.font.Font(arial_font, 30)


pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1)


class Game:
    def __init__(self, ):
        self.fight_off = 0
        self.game_over = False
        self.speed = 8

        self.radius = 5
        self.ball_rect = pygame.rect.Rect(width / 2 - self.radius, height / 2 - self.radius, self.radius * 2,
                                          self.radius * 2)
        self.ball_speed = 5
        self.ball_speed_x = 0
        self.ball_speed_y = 5
        self.ball_beat_first = False

        self.platform_width, self.platform_height = 50, 10
        self.platform_rect = pygame.rect.Rect(width / 2 - self.platform_width, height - self.platform_height * 2 - 50,
                                              self.platform_width, self.platform_height)

        self.width = 80
        self.height = 25
        self.left = 0
        self.top = 25
        self.cell_size = 10
        self.objects = list()
        arr = list()
        for i in range(self.height):
            for j in range(self.width):
                arr.append(
                    pygame.rect.Rect((self.left + self.cell_size * j, self.top + self.cell_size * i,
                                      self.cell_size, self.cell_size)))
            self.objects.append(arr.copy())
            arr.clear()

        self.board = BOARD.copy()

    def update(self, screen):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.platform_rect.x < width - self.platform_width:
                self.platform_rect.x += self.speed
            elif keys[pygame.K_LEFT] and self.platform_rect.x > 0:
                self.platform_rect.x -= self.speed

            if self.platform_rect.colliderect(self.ball_rect):
                if not self.ball_beat_first:
                    if random.randint(0, 1) == 0:
                        self.ball_speed_x = self.ball_speed
                    else:
                        self.ball_speed_x = - self.ball_speed
                    self.ball_beat_first = True
                self.ball_speed_y = - self.ball_speed

            pygame.draw.rect(screen, (255, 255, 255), self.platform_rect)

        self.ball_rect.x += self.ball_speed_x
        self.ball_rect.y += self.ball_speed_y
        if self.ball_rect.bottom >= height:
            self.game_over = True
            self.ball_speed_y = - self.ball_speed
        elif self.ball_rect.top <= 0:
            self.ball_speed_y = self.ball_speed
        elif self.ball_rect.left <= 0:
            self.ball_speed_x = self.ball_speed
        elif self.ball_rect.right >= width:
            self.ball_speed_x = - self.ball_speed

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    if self.objects[i][j].collidepoint(
                            (self.ball_rect.top, random.randint(self.ball_rect.left, self.ball_rect.right))) or \
                            self.objects[i][j].collidepoint(
                                (self.ball_rect.bottom, random.randint(self.ball_rect.left, self.ball_rect.right))):
                        self.ball_speed_y = - self.ball_speed_y
                        self.fight_off += 10
                        self.board[i][j] = 1
                    elif self.objects[i][j].collidepoint(
                            (self.ball_rect.left, random.randint(self.ball_rect.top, self.ball_rect.bottom))) or \
                            self.objects[i][j].collidepoint(
                                (self.ball_rect.right, random.randint(self.ball_rect.top, self.ball_rect.bottom))):
                        self.ball_speed_x = - self.ball_speed_x
                        self.fight_off += 10
                        self.board[i][j] = 1

        pygame.draw.circle(screen, (255, 255, 255), self.ball_rect.center, self.radius)

        color = None
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    color = pygame.color.Color('white')
                elif self.board[i][j] == 1:
                    color = pygame.color.Color('black')
                pygame.draw.rect(screen, color, (
                    self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size,
                    self.cell_size))


class GameOver(pygame.sprite.Sprite):
    image = pygame.image.load("data/gameover.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.rect.x = - width
        self.rect.y = (height - self.image.get_height()) // 2
        self.pos_x = - width
        self.fight_off = 0

    def move(self, coordinate):
        self.pos_x += coordinate
        self.rect.x = self.pos_x

    def print_res(self):
        game_over_text_res = arial_font_48.render(f'Your earned points: {self.fight_off}', True, (255, 255, 255))
        screen.blit(game_over_text_res, [width / 2 - game_over_text_res.get_width() / 2, height / 3 + 20])


class Home(GameOver):
    image = pygame.image.load('data/home.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Home.image
        self.rect = self.image.get_rect()
        self.rect.y = (height // 2 - self.image.get_height()) // 2

    def move(self, coordinate):
        super().move(coordinate)


class Restart(GameOver):
    image = pygame.image.load('data/restart.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Restart.image
        self.rect = self.image.get_rect()
        self.rect.y = height // 2 + (height // 2 - self.image.get_height()) // 2

    def move(self, coordinate):
        super().move(coordinate)


def main():
    pygame.display.set_caption('Game')
    pygame.mouse.set_visible(False)

    sprite_game_over = pygame.sprite.Group()
    gameover = GameOver(sprite_game_over)

    sprite_home = pygame.sprite.Group()
    home = Home(sprite_home)

    sprite_restart = pygame.sprite.Group()
    restart = Restart(sprite_restart)

    game = Game()

    bg_color = (0, 0, 0)
    game_over_color = (0, 0, 100)
    fps = 60
    pps = 250
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game.game_over:
            screen.fill(game_over_color)
            sprite_game_over.draw(screen)
            sprite_home.draw(screen)
            sprite_restart.draw(screen)
            if gameover.rect.x < (width - gameover.rect.width) / 2:
                gameover.move(pps / fps)
            if home.rect.x < (width - home.rect.width) / 2:
                home.move(pps / fps)
            if restart.rect.x < (width - restart.rect.width) / 2:
                restart.move(pps / fps)
            gameover.print_res()
            pygame.mouse.set_visible(True)
        else:
            screen.fill(bg_color)
            game.update(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
