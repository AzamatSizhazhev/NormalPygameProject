import random
import pygame

pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)


class Game:
    def __init__(self, ):
        self.fight_off = 0
        self.game_over = False
        self.speed = 8

        # self.arial_font = pygame.font.match_font('arial')
        # self.arial_font_48 = pygame.font.Font(self.arial_font, 48)

        self.radius = 10
        self.ball_rect = pygame.rect.Rect(width / 2 - self.radius, height / 2 - self.radius, self.radius * 2,
                                          self.radius * 2)
        self.ball_speed = 7
        self.ball_speed_x = 0
        self.ball_speed_y = 7
        self.ball_beat_first = False

        self.platform_width, self.platform_height = 100, 15
        self.platform_rect = pygame.rect.Rect(width / 2 - self.platform_width, height - self.platform_height * 2 - 50,
                                              self.platform_width, self.platform_height)

    def update(self, screen):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.platform_rect.x += self.speed
            elif keys[pygame.K_LEFT]:
                self.platform_rect.x -= self.speed

            if self.platform_rect.colliderect(self.ball_rect):
                if not self.ball_beat_first:
                    if random.randint(0, 1) == 0:
                        self.ball_speed_x = self.ball_speed
                    else:
                        self.ball_speed_x = - self.ball_speed

                    self.ball_beat_first = True
                self.ball_speed_y = - self.ball_speed
                self.fight_off += 1

            pygame.draw.rect(screen, (255, 255, 255), self.platform_rect)
        else:
            pass
            # TODO: новый скрин проигрыша
            # screen.fill(bg_color)
            # game_over_text = arial_font_48.render(f'Game OVER!  Your kill count: {kill_count}', True, (255, 255, 255))
            # screen.blit(game_over_text, [width / 2 - game_over_text.get_width() / 2, height / 3])

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

        pygame.draw.circle(screen, (255, 255, 255), self.ball_rect.center, self.radius)


def main():
    pygame.display.set_caption('Game')

    game = Game()
    bg_color = (0, 0, 0)
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(bg_color)
        game.update(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
