import pygame
import random
import math
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, grid, color, speed, chase_radius):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
        self.draw_base_sprite(color)
        self.rect = self.image.get_rect()
        
        if x < GRID_WIDTH and y < GRID_HEIGHT:
            self.x = (x * TILE_SIZE) + (TILE_SIZE / 2)
            self.y = (y * TILE_SIZE) + (TILE_SIZE / 2)
        else:
            self.x = x
            self.y = y
            
        self.rect.center = (self.x, self.y)
        self.grid = grid
        self.speed = speed
        self.chase_radius = chase_radius
        
        self.dx = 0
        self.dy = 0
        self.pick_random_direction()

    def draw_base_sprite(self, color):
        self.image.fill((0,0,0,0))
        w, h = TILE_SIZE - 10, TILE_SIZE - 10
        pygame.draw.ellipse(self.image, (0,0,0,100), (4, h-8, w-8, 8))
        pygame.draw.rect(self.image, DARK_HAT, (w//2-6, h//2+2, 5, h//2-4))
        pygame.draw.rect(self.image, DARK_HAT, (w//2+1, h//2+2, 5, h//2-4))
        pygame.draw.rect(self.image, color, (w//2-8, h//2-8, 16, 12))
        pygame.draw.circle(self.image, SKIN, (w//2, h//2-10), 6)

    def pick_random_direction(self):
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = random.choice(dirs)
        self.dx = dx * self.speed
        self.dy = dy * self.speed

    def check_wall_ahead(self, dt):
        future_x = self.x + self.dx * dt
        future_y = self.y + self.dy * dt
        gx = int(future_x // TILE_SIZE)
        gy = int(future_y // TILE_SIZE)
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            if self.grid[gy][gx] == 0:
                return True
        return True
        
    def distance_to(self, target):
        return math.hypot(self.x - target.x, self.y - target.y)

    def chase(self, target):
        angle = math.atan2(target.y - self.y, target.x - self.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self, dt, player):
        dist = self.distance_to(player)
        if dist < self.chase_radius:
            self.chase(player)
        else:
            if self.check_wall_ahead(dt) or random.random() < 0.02:
                self.pick_random_direction()
                
        future_x = self.x + self.dx * dt
        future_y = self.y + self.dy * dt
        gx, gy = int(future_x // TILE_SIZE), int(future_y // TILE_SIZE)
        
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT and self.grid[gy][gx] != 0:
            self.x = future_x
            self.y = future_y
            self.rect.center = (self.x, self.y)
        else:
            if dist >= self.chase_radius:
                self.pick_random_direction()

class Haredi(Enemy):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, GRAY, HAREDIM_SPEED, HAREDIM_CHASE_RADIUS)
        # Add black hats
        w, h = TILE_SIZE - 10, TILE_SIZE - 10
        pygame.draw.rect(self.image, DARK_HAT, (w//2-8, h//2-12, 16, 4))
        pygame.draw.rect(self.image, DARK_HAT, (w//2-6, h//2-16, 12, 4))

class YairMaayan(Enemy):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, YELLOW, YAIR_SPEED, YAIR_CHASE_RADIUS)
        w, h = TILE_SIZE - 10, TILE_SIZE - 10
        # Draw special hair
        pygame.draw.rect(self.image, ORANGE, (w//2-6, h//2-14, 12, 4))

class Ofir(Enemy):
    def __init__(self, x, y, grid, bus):
        super().__init__(x, y, grid, CYAN, OFIR_SPEED, 99999)
        w, h = TILE_SIZE - 10, TILE_SIZE - 10
        pygame.draw.rect(self.image, BLACK, (w//2-6, h//2-14, 12, 4)) # Black hair
        self.bus = bus
        self.returning = False
        
    def update(self, dt, player):
        if not self.returning:
            # Chasing player
            dist = self.distance_to(player)
            if dist > OFIR_GIVE_UP_RADIUS:
                self.returning = True
            else:
                self.chase(player)
        else:
            # Returning to Bus
            self.chase(self.bus)
            if self.distance_to(self.bus) < 30:
                self.bus.resume_driving()
                self.kill() # Remove Ofir from sprite group
                return
                
        # Apply movement
        future_x = self.x + self.dx * dt
        future_y = self.y + self.dy * dt
        gx, gy = int(future_x // TILE_SIZE), int(future_y // TILE_SIZE)
        
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT and self.grid[gy][gx] != 0:
            self.x = future_x
            self.y = future_y
            self.rect.center = (self.x, self.y)
        else:
            self.pick_random_direction()

class Bus(pygame.sprite.Sprite):
    def __init__(self, x, y, grid):
        super().__init__()
        w, h = TILE_SIZE * 1.5, TILE_SIZE - 10
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        
        # shadow
        pygame.draw.ellipse(self.image, (0,0,0,100), (4, h-8, w-8, 12))
        # wheels
        pygame.draw.rect(self.image, BLACK, (4, h-4, 8, 4))
        pygame.draw.rect(self.image, BLACK, (w-12, h-4, 8, 4))
        # body
        pygame.draw.rect(self.image, ORANGE, (0, 0, w, h-2), border_radius=4)
        # windows
        pygame.draw.rect(self.image, WINDOW_COLOR, (4, 4, w//2 - 6, h//2))
        pygame.draw.rect(self.image, WINDOW_COLOR, (w//2 + 2, 4, w//2 - 6, h//2))
        
        self.rect = self.image.get_rect()
        
        self.x = (x * TILE_SIZE) + (TILE_SIZE / 2)
        self.y = (y * TILE_SIZE) + (TILE_SIZE / 2)
        self.rect.center = (self.x, self.y)
        self.grid = grid
        
        self.dx = 0
        self.dy = 0
        self.pick_random_direction()
        self.spawned_ofir = False
        self.active_driver = True
        
    def distance_to(self, target):
        return math.hypot(self.x - target.x, self.y - target.y)
        
    def pick_random_direction(self):
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = random.choice(dirs)
        self.dx = dx * BUS_SPEED
        self.dy = dy * BUS_SPEED

    def resume_driving(self):
        self.active_driver = True
        self.spawned_ofir = False
        self.pick_random_direction()

    def update(self, dt, player):
        if not self.active_driver:
            return
            
        if self.distance_to(player) < BUS_TRIGGER_RADIUS and not self.spawned_ofir:
            self.spawned_ofir = True
            self.active_driver = False
            self.dx, self.dy = 0, 0
            return
            
        future_x = self.x + self.dx * dt
        future_y = self.y + self.dy * dt
        gx, gy = int(future_x // TILE_SIZE), int(future_y // TILE_SIZE)
        
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT and self.grid[gy][gx] != 0:
            self.x = future_x
            self.y = future_y
            self.rect.center = (self.x, self.y)
        else:
            self.pick_random_direction()
