import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, grid, touch_controls=None):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
        self.draw_sprite()
        self.rect = self.image.get_rect()
        
        self.x = (start_x * TILE_SIZE) + (TILE_SIZE / 2)
        self.y = (start_y * TILE_SIZE) + (TILE_SIZE / 2)
        self.rect.center = (self.x, self.y)
        
        self.grid = grid
        self.touch_controls = touch_controls
        
        self.stamina = PLAYER_STAMINA_MAX
        self.is_running = False
        self.dx = 0
        self.dy = 0

    def draw_sprite(self):
        self.image.fill((0,0,0,0)) # transparent background
        w, h = TILE_SIZE - 10, TILE_SIZE - 10
        # draw shadow
        pygame.draw.ellipse(self.image, (0,0,0,100), (4, h-8, w-8, 8))
        # draw legs
        pygame.draw.rect(self.image, JEANS, (w//2-6, h//2+2, 5, h//2-4))
        pygame.draw.rect(self.image, JEANS, (w//2+1, h//2+2, 5, h//2-4))
        # draw body
        pygame.draw.rect(self.image, BLUE, (w//2-8, h//2-8, 16, 12))
        # draw head
        pygame.draw.circle(self.image, SKIN, (w//2, h//2-10), 6)

    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pygame.key.get_pressed()
        
        touch_dx, touch_dy, sprint = 0, 0, False
        if self.touch_controls:
            touch_dx, touch_dy, sprint = self.touch_controls.get_input()
        
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or sprint) and self.stamina > 0:
            speed = PLAYER_RUN_SPEED
            self.is_running = True
        else:
            speed = PLAYER_SPEED
            self.is_running = False
            
        if keys[pygame.K_w]:
            self.dy = -speed
        if keys[pygame.K_s]:
            self.dy = speed
        if keys[pygame.K_a]:
            self.dx = -speed
        if keys[pygame.K_d]:
            self.dx = speed
            
        if touch_dx != 0 or touch_dy != 0:
            self.dx = touch_dx * speed
            self.dy = touch_dy * speed
            
        if self.dx != 0 and self.dy != 0 and touch_dx == 0 and touch_dy == 0:
            self.dx *= 0.7071
            self.dy *= 0.7071

    def collide_with_walls(self, dir):
        # Create padding to make walking in roads much easier and avoid getting caught on corners
        pad_x = 10
        pad_y = 10
        corners = [
            (self.rect.left + pad_x, self.rect.top + pad_y),
            (self.rect.right - pad_x, self.rect.top + pad_y),
            (self.rect.left + pad_x, self.rect.bottom - pad_y),
            (self.rect.right - pad_x, self.rect.bottom - pad_y)
        ]
        
        for cx, cy in corners:
            gx, gy = int(cx // TILE_SIZE), int(cy // TILE_SIZE)
            if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                if self.grid[gy][gx] == 0:
                    if dir == 'x':
                        if self.dx > 0:
                            self.x = gx * TILE_SIZE - (self.rect.width / 2) - 1
                        if self.dx < 0:
                            self.x = (gx + 1) * TILE_SIZE + (self.rect.width / 2) + 1
                        self.dx = 0
                        self.rect.centerx = self.x
                        return
                    
                    if dir == 'y':
                        if self.dy > 0:
                            self.y = gy * TILE_SIZE - (self.rect.height / 2) - 1
                        if self.dy < 0:
                            self.y = (gy + 1) * TILE_SIZE + (self.rect.height / 2) + 1
                        self.dy = 0
                        self.rect.centery = self.y
                        return

    def update(self, dt):
        self.get_keys()
        
        if self.is_running and (self.dx != 0 or self.dy != 0):
            self.stamina -= STAMINA_DRAIN_RATE * dt
            if self.stamina < 0:
                self.stamina = 0
                self.is_running = False
        else:
            self.stamina += STAMINA_REGEN_RATE * dt
            if self.stamina > PLAYER_STAMINA_MAX:
                self.stamina = PLAYER_STAMINA_MAX

        self.x += self.dx * dt
        self.rect.centerx = self.x
        self.collide_with_walls('x')
        
        self.y += self.dy * dt
        self.rect.centery = self.y
        self.collide_with_walls('y')
