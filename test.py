import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600

# Couleurs
white = (255, 255, 255)
red = (255, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Survival Game")

# Classe pour les ennemis
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        # Position initiale à l'extérieur de la fenêtre
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.center = (0, random.randint(0, screen_height))
        elif side == "right":
            self.rect.center = (screen_width, random.randint(0, screen_height))
        elif side == "top":
            self.rect.center = (random.randint(0, screen_width), 0)
        elif side == "bottom":
            self.rect.center = (random.randint(0, screen_width), screen_height)
        
        # vitesse
        self.speed = 2
        self.collided = False  # Variable pour détecter la collision


    def update(self):
        # Vérification de la collision avec le héros
        if not self.collided:
            dx = screen_width / 2 - self.rect.centerx
            dy = screen_height / 2 - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 20:  # Distance seuil pour la collision
                self.collided = True
                print(self)
                hero.take_damage()
        
        # Si pas encore collidé, continuer à se déplacer vers le centre
        if not self.collided:
            direction = (dx / distance, dy / distance)
            self.rect.x += direction[0] * self.speed
            self.rect.y += direction[1] * self.speed

        # # Calcul de la direction vers le centre
        # dx = screen_width / 2 - self.rect.centerx
        # dy = screen_height / 2 - self.rect.centery
        # distance = math.sqrt(dx**2 + dy**2)
        # direction = (dx / distance, dy / distance)
        
        # # Déplacement de l'ennemi
        # self.rect.x += direction[0] * self.speed
        # self.rect.y += direction[1] * self.speed

# Classe pour le héros
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.health = 10  # Points de vie du héros

    def take_damage(self):
        self.health -= 1
        print(self.health)
        if self.health <= 0:
            self.kill() # Le héros meurt et le jeu se termine

    def getHealt(self):
        self.health

# Groupes de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
hero = Hero()
all_sprites.add(hero)

# Boucle de jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Création d'un nouvel ennemi à intervalles réguliers
    if random.random() < 0.02:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Mise à jour des sprites
    all_sprites.update()

    # Vérification des collisions avec le héros
    hits = pygame.sprite.spritecollide(hero, enemies, False)
    for enemy in hits:
        if not enemy.collided:
            hero.take_damage()
            enemy.collided = True
            
    # Effacement de l'écran
    screen.fill((0, 0, 0))

    # Dessin des sprites
    all_sprites.draw(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
