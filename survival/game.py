import pygame

from models import Player, Enemy
from utils import  get_random_position, load_sprite

class Survival:
    MIN_ENEMY_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("land_1", False)
        self.clock = pygame.time.Clock()
        self.player = Player((400, 300))
        self.enemies = []

        for _ in range(6):
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

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.player.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.player.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.player.accelerate()
        if is_key_pressed[pygame.K_DOWN]:
            self.player.decelerate()

    def _get_game_object(self):
        return [*self.enemies, self.player]
    
    def _process_game_logic(self):
        for game_object in self._get_game_object():
            game_object.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_object():
            game_object.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(60)