import random
import pygame

pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)

def main():
    pygame.display.set_caption('Game')
    # Игровые переменные
    kill_count = 0
    game_over = False
    speed = 8
    # шрифт
    arial_font = pygame.font.match_font('arial')
    arial_font_48 = pygame.font.Font(arial_font, 48)
    # мячик
    radius = 10
    ball_rect = pygame.rect.Rect(width / 2 - radius,
                                 height / 2 - radius,
                                 radius * 2,
                                 radius * 2)
    ball_speed = 7
    ball_speed_x = 0
    ball_speed_y = ball_speed
    ball_beat_first = False
    # платформа
    platform_width, platform_height = 100, 15
    platform_rect = pygame.rect.Rect(width / 2 - platform_width,
                                     height - platform_height * 2 - 50,
                                     platform_width,
                                     platform_height)
    bg_color = (0, 0, 0)
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(bg_color)
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                platform_rect.x += speed
            elif keys[pygame.K_LEFT]:
                platform_rect.x -= speed

            if platform_rect.colliderect(ball_rect):
                if not ball_beat_first:
                    if random.randint(0, 1) == 0:
                        ball_speed_x = ball_speed
                    else:
                        ball_speed_x = -ball_speed

                    ball_beat_first = True
                ball_speed_y = -ball_speed
                kill_count += 1

            pygame.draw.rect(screen, (255, 255, 255), platform_rect)
        else:
            screen.fill(bg_color)
            game_over_text = arial_font_48.render(f'Game OVER!  Your kill count: {kill_count}', True, (255, 255, 255))
            screen.blit(game_over_text, [width / 2 - game_over_text.get_width() / 2, height / 3])

        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y
        if ball_rect.bottom >= height:
            game_over = True
            ball_speed_y = -ball_speed
        elif ball_rect.top <= 0:
            ball_speed_y = ball_speed
        elif ball_rect.left <= 0:
            ball_speed_x = ball_speed
        elif ball_rect.right >= width:
            ball_speed_x = -ball_speed

        pygame.draw.circle(screen, (255, 255, 255), ball_rect.center, radius)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
