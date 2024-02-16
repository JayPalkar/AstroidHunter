import random

import pygame

pygame.font.init()
pygame.mixer.init()

Width, Height = 1280, 720
FPS = 60

score = 0
Score_Font = pygame.font.SysFont('comicsans', 40)
game_over_Font = pygame.font.SysFont('comicsans', 60)
final_score = pygame.font.SysFont('comicsans', 50)
restart_font = pygame.font.SysFont('comicsans', 60)

ShipScale = 100
ShipSpeed = 5

bullet_speed = 5
bullet_hit = pygame.USEREVENT + 1

asteroid_speed = 4
asteroid_hit = pygame.USEREVENT + 2
Asteroid_width = random.randrange(50, 150)
Asteroid_height = random.randrange(50, 150)
Asteroid_x = random.randrange(1288, 1300)
Asteroid_y = random.randrange(50, 620)

Asteroid2_width = random.randrange(50, 150)
Asteroid2_height = random.randrange(50, 150)
Asteroid2_x = random.randrange(1288, 1300)
Asteroid2_y = random.randrange(50, 620)

Asteroid3_width = random.randrange(50, 150)
Asteroid3_height = random.randrange(50, 150)
Asteroid3_x = random.randrange(1288, 1300)
Asteroid3_y = random.randrange(50, 620)

clock = pygame.time.Clock()

Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Asteroid Hunter")
pygame.display.set_icon(pygame.image.load('Assets/SpaceShip.png'))

Bg_img = pygame.transform.scale(pygame.image.load('Assets/BackGround.png'), (Width, Height))
planet_img = pygame.transform.scale(pygame.image.load('Assets/planet.png'), (1000, 1000))

spaceship_img = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load('Assets/spaceship.png'), (ShipScale, ShipScale)), 270)

spaceship_scaled = pygame.transform.scale(pygame.image.load('Assets/spaceship.png'), (300, 300))

asteroids_img = pygame.transform.scale(pygame.image.load('Assets/Ast1.png'), (Asteroid_width, Asteroid_height))
asteroids_img2 = pygame.transform.scale(pygame.image.load('Assets/Ast2.png'), (Asteroid2_width, Asteroid2_height))
asteroids_img3 = pygame.transform.scale(pygame.image.load('Assets/Ast3.png'), (Asteroid3_width, Asteroid3_height))

bullet_sound = pygame.mixer.Sound('Assets/Shooting_sound.mp3')

bullets = []
Yellow = (255, 255, 0)
Voilet = (207, 159, 255)
Black = (0, 0, 0)
White = (255, 255, 255)
Reload = 5


def draw_window(spaceship, planet, asteroids, bullets, asteroids2, asteroids3, score):
    Window.blit(Bg_img, (0, 0))
    Window.blit(spaceship_img, (spaceship.x, spaceship.y))
    Window.blit(asteroids_img, (asteroids.x, asteroids.y))
    Window.blit(asteroids_img2, (asteroids2.x, asteroids2.y))
    Window.blit(asteroids_img3, (asteroids3.x, asteroids3.y))
    Score_Font_Txt = Score_Font.render('Score: ' + str(score), True, White)
    Window.blit(Score_Font_Txt, (580, 10))
    Window.blit(planet_img, (planet.x, planet.y))
    for bul in bullets:
        pygame.draw.rect(Window, Yellow, bul)


def draw_gameover(score):
    Window.fill(Voilet)
    Window.blit(spaceship_scaled, (Width // 2 - 150, Height // 2 - 150))
    game_name = game_over_Font.render('Asteroid Hunter', True, Black)
    game_name_rect = game_name.get_rect(center=(640, 80))
    score_text = final_score.render('Score : ' + str(score), True, Black)
    score_text_rect = score_text.get_rect(center=(640, 150))
    restart_font_text = restart_font.render('Press SPACE to restart the game', True, Black)
    restart_font_rect = restart_font_text.get_rect(center=(640, 600))
    Window.blit(game_name, game_name_rect)
    Window.blit(score_text, score_text_rect)
    Window.blit(restart_font_text, restart_font_rect)


def ship_movements(keys, spaceship):
    if keys[pygame.K_w] and spaceship.y - ShipSpeed > 50:
        spaceship.y -= ShipSpeed
    if keys[pygame.K_s] and spaceship.y - ShipSpeed < 620:
        spaceship.y += ShipSpeed
    if keys[pygame.K_a] and spaceship.x - ShipSpeed > 200:
        spaceship.x -= ShipSpeed
    if keys[pygame.K_d]:
        spaceship.x += ShipSpeed


def bullet_handle(bullets, asteroids, asteroids2, asteroids3):
    for b in bullets:
        b.x += bullet_speed

        if asteroids.colliderect(b):
            pygame.event.post(pygame.event.Event(bullet_hit))
            asteroids.x = Asteroid_x
            asteroids.y = random.randrange(50, 620)
            bullets.remove(b)

        if asteroids2.colliderect(b):
            pygame.event.post(pygame.event.Event(bullet_hit))
            asteroids2.x = Asteroid2_x
            asteroids2.y = random.randrange(50, 620)
            bullets.remove(b)

        if asteroids3.colliderect(b):
            pygame.event.post(pygame.event.Event(bullet_hit))
            asteroids3.x = Asteroid3_x
            asteroids3.y = random.randrange(50, 620)
            bullets.remove(b)

        if b.x > Width:
            bullets.remove(b)


def main():
    spaceship = pygame.Rect(250, 360, ShipScale, ShipScale)
    planet = pygame.Rect(-800, -145, 1000, 1000)
    asteroids = pygame.Rect(Asteroid_x, Asteroid_y, Asteroid_width, Asteroid_height)
    asteroids2 = pygame.Rect(Asteroid2_x, Asteroid2_y, Asteroid2_width, Asteroid2_height)
    asteroids3 = pygame.Rect(Asteroid3_x, Asteroid3_y, Asteroid3_width, Asteroid3_height)
    score = 0
    game_active = True

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN and len(bullets) < Reload:
                    if event.button == 1:
                        bullet = pygame.Rect(spaceship.x + spaceship.width, spaceship.y + spaceship.height // 2 - 2, 10,
                                             5)
                        bullets.append(bullet)
                        bullet_sound.play()

                if event.type == pygame.K_RCTRL and len(bullets) < Reload:
                    if event.button == 1:
                        bullet = pygame.Rect(spaceship.x + spaceship.width, spaceship.y + spaceship.height // 2 - 2, 10,
                                             5)
                        bullets.append(bullet)
                        bullet_sound.play()

                if event.type == bullet_hit:
                    score += 1

                if event.type == asteroid_hit:
                    score = 0
                    asteroids.x = Asteroid_x
                    asteroids.y = random.randrange(50, 620)
                    asteroids2.x = Asteroid2_x
                    asteroids2.y = random.randrange(50, 620)
                    asteroids3.x = Asteroid3_x
                    asteroids3.y = random.randrange(50, 620)

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    score = 0
                    asteroids.x = Asteroid_x
                    asteroids2.x = Asteroid2_x
                    asteroids3.x = Asteroid3_x

        if game_active:
            keys = pygame.key.get_pressed()
            ship_movements(keys, spaceship)
            bullet_handle(bullets, asteroids, asteroids2, asteroids3)
            asteroids.x -= asteroid_speed
            asteroids2.x -= asteroid_speed
            asteroids3.x -= asteroid_speed

            draw_window(spaceship, planet, asteroids, bullets, asteroids2, asteroids3, score)

            if asteroids.x < -10:
                asteroids.x = Asteroid_x
                asteroids.y = random.randrange(50, 620)

            if asteroids2.x < -10:
                asteroids2.x = Asteroid2_x
                asteroids2.y = random.randrange(50, 620)

            if asteroids3.x < -10:
                asteroids3.x = Asteroid3_x
                asteroids3.y = random.randrange(50, 620)

            if spaceship.colliderect(asteroids):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))

            elif spaceship.colliderect(asteroids2):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))

            elif spaceship.colliderect(asteroids3):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))

            elif planet.colliderect(asteroids):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))

            elif planet.colliderect(asteroids2):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))

            elif planet.colliderect(asteroids3):
                game_active = False
                # pygame.event.post(pygame.event.Event(asteroid_hit))
        else:
            draw_gameover(score)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
