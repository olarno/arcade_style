import pygame
from pygame.math import Vector2
from models import Player, Enemy
from utils import get_random_position, load_sprite, print_text
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Survival:
    MIN_ENEMY_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_scroll = [0, 0]
        self.background = load_sprite("land_1", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.enemies = []
        self.bullets = []
        self.player = Player((400, 300), self.bullets.append)

        self.shooting_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.shooting_event, 50)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Survival")

    def main_loop(self):
        enemy_spawn_timer = pygame.time.get_ticks() 
        
        while True:
            self.screen.fill((24,164,86))
            self._handle_input()
            self._process_game_logic()
            self._draw()
             
            # Check the time elapsed and generate enemies randomly
            current_time = pygame.time.get_ticks()
            if current_time - enemy_spawn_timer >= random.randint(1000, 2000):
                self._generate_enemies_randomly()
                enemy_spawn_timer = current_time  # Reset the timer

    def _generate_enemies_randomly(self):
        while True:
            position = get_random_position(self.screen)
            distance_to_player = position.distance_to(self.player.position)

            if distance_to_player > self.MIN_ENEMY_DISTANCE:
                break

        enemy = Enemy(position, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # enemy.move_towards_center()

        self.enemies.append(enemy)
            
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
                and event.type == self.shooting_event
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
                    # self.player = None
                    # self.message = "Game Over!"
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


    def _draw(self):
        self.screen.blit(self.background, (0 - self.display_scroll[0], 0 - self.display_scroll[1]))

        for game_object in self._get_game_object():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60)