import pygame

from models import Player, Enemy
from utils import get_random_position, load_sprite, print_text

class Survival:
    MIN_ENEMY_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.display_scroll = [0, 0]
        self.background = load_sprite("land_1", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.enemies = []
        self.bullets = []
        self.player = Player((400, 300), self.bullets.append)

        self.shooting = pygame.USEREVENT + 1
        pygame.time.set_timer( self.shooting, 500)

        for _ in range(12):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.player.position)
                    > self.MIN_ENEMY_DISTANCE
                ):
                    break
            self.enemies.append(Enemy(position))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Survival")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit() 
            elif (
                self.player
                and event.type == self.shooting
            ):
                self.player.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.player:
            if is_key_pressed[pygame.K_RIGHT]:
                self.player.rotate(clockwise=True)
                self.display_scroll[0] += 5
            elif is_key_pressed[pygame.K_LEFT]:
                self.player.rotate(clockwise=False)
                self.display_scroll[0] -= 5
            elif is_key_pressed[pygame.K_UP]:
                self.player.rotate(clockwise=False)
                self.display_scroll[1] -= 5
            elif is_key_pressed[pygame.K_DOWN]:
                self.player.rotate(clockwise=False)
                self.display_scroll[1] += 5

    def _get_game_object(self):
        games_objects = [*self.enemies, *self.bullets]

        if self.player:
            games_objects.append(self.player)
        
        return games_objects
    
    def _process_game_logic(self):
        for game_object in self._get_game_object():
            game_object.move(self.screen)

        if self.player:
            for enemy in self.enemies:
                if enemy.collides_with(self.player):
                    self.player = None
                    self.message = "Game Over!"
                    break

        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if enemy.collides_with(bullet):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.enemies and self.player:
            self.message = "Houra!"

    def _draw(self):
        self.screen.blit(self.background, (0 - self.display_scroll[0], 0 - self.display_scroll[1]))

        for game_object in self._get_game_object():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60)