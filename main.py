import pygame
import sys
import random
import math
from settings import *
from map_gen import generate_map
from player import Player
from enemies import Haredi, YairMaayan, Bus, Ofir
from ui import UI

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shalev Barkin - Halamish Run")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.state = "PLAYING" # PLAYING, WIN, LOSE
        
    def new_game(self):
        self.grid, self.start_pos, self.mall_pos = generate_map()
        self.player = Player(self.start_pos[0], self.start_pos[1], self.grid)
        self.camera = Camera(GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
        
        self.enemies = pygame.sprite.Group()
        
        spawned_haredim = 0
        while spawned_haredim < HAREDIM_COUNT:
            rx = random.randint(1, GRID_WIDTH - 2)
            ry = random.randint(1, GRID_HEIGHT - 2)
            if self.grid[ry][rx] == 1 and math.hypot(rx - self.start_pos[0], ry - self.start_pos[1]) > 10:
                self.enemies.add(Haredi(rx, ry, self.grid))
                spawned_haredim += 1
                
        placed_yair = False
        while not placed_yair:
            rx = random.randint(1, GRID_WIDTH - 2)
            ry = random.randint(1, GRID_HEIGHT - 2)
            if self.grid[ry][rx] == 1 and math.hypot(rx - self.start_pos[0], ry - self.start_pos[1]) > 10:
                self.enemies.add(YairMaayan(rx, ry, self.grid))
                placed_yair = True
                
        placed_bus = False
        while not placed_bus:
            rx = random.randint(1, GRID_WIDTH - 2)
            ry = random.randint(1, GRID_HEIGHT - 2)
            if self.grid[ry][rx] == 1 and math.hypot(rx - self.start_pos[0], ry - self.start_pos[1]) > 5:
                self.bus = Bus(rx, ry, self.grid)
                self.enemies.add(self.bus)
                placed_bus = True

        self.state = "PLAYING"

    def run(self):
        self.new_game()
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if self.state == "PLAYING":
                self.update(dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state in ["WIN", "LOSE", "LOSE_HAREDIM", "LOSE_YAIR", "LOSE_OFIR"]:
                    self.new_game()

    def update(self, dt):
        self.player.update(dt)
        self.camera.update(self.player)
        
        for enemy in self.enemies:
            enemy.update(dt, self.player)
            # Use a tighter collision radius of 20 pixels instead of the full rect to require a "full collision"
            if math.hypot(self.player.rect.centerx - enemy.rect.centerx, self.player.rect.centery - enemy.rect.centery) < 20:
                if isinstance(enemy, Haredi):
                    self.state = "LOSE_HAREDIM"
                elif isinstance(enemy, YairMaayan):
                    self.state = "LOSE_YAIR"
                elif isinstance(enemy, Ofir):
                    self.state = "LOSE_OFIR"
                else:
                    self.state = "LOSE"
                
        if self.bus.spawned_ofir and self.bus.active_driver == False:
            self.bus.active_driver = None
            ofir = Ofir(self.bus.x // TILE_SIZE, self.bus.y // TILE_SIZE, self.grid, self.bus)
            self.enemies.add(ofir)
            print("Shalev Bad!")
            
        px, py = int(self.player.x // TILE_SIZE), int(self.player.y // TILE_SIZE)
        if 0 <= px < GRID_WIDTH and 0 <= py < GRID_HEIGHT:
            if self.grid[py][px] == 2:
                self.state = "WIN"

    def draw(self):
        self.screen.fill(BLACK)
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile_id = self.grid[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                cam_rect = self.camera.apply_rect(rect)
                
                if not cam_rect.colliderect(self.screen.get_rect()):
                    continue
                    
                if tile_id == 0:
                    self.screen.fill(ROOF_BORDER, cam_rect)
                    pygame.draw.rect(self.screen, ROOF, (cam_rect.x, cam_rect.y, TILE_SIZE, TILE_SIZE - 6))
                elif tile_id == 1:
                    self.screen.fill(ASPHALT, cam_rect)
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(self.screen, ROAD_LINE, (cam_rect.centerx - 2, cam_rect.centery - 2, 4, 4))
                elif tile_id == 2:
                    self.screen.fill(MALL_COLOR, cam_rect)
                    pygame.draw.rect(self.screen, MALL_LIGHT, cam_rect, 4)
                    pygame.draw.rect(self.screen, WINDOW_COLOR, (cam_rect.x + 8, cam_rect.y + 8, 8, 8))
                    pygame.draw.rect(self.screen, WINDOW_COLOR, (cam_rect.right - 16, cam_rect.y + 8, 8, 8))
                
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        for enemy in self.enemies:
            cam_rect = self.camera.apply(enemy)
            self.screen.blit(enemy.image, cam_rect)
            
            if isinstance(enemy, Bus):
                text = self.ui.small_font.render("Ofir Tours, Shalev Bad", True, WHITE)
                self.screen.blit(text, (cam_rect.centerx - text.get_width() // 2, cam_rect.top - 20))
                
            elif isinstance(enemy, Ofir):
                text = self.ui.small_font.render("Shalev Bad!", True, WHITE)
                self.screen.blit(text, (cam_rect.centerx - text.get_width() // 2, cam_rect.top - 20))
                
        self.ui.draw_stamina_bar(self.player.stamina)
        
        px = self.player.rect.centerx
        py = self.player.rect.centery
        mx = self.mall_pos[0] * TILE_SIZE + TILE_SIZE / 2
        my = self.mall_pos[1] * TILE_SIZE + TILE_SIZE / 2
        angle = math.atan2(my - py, mx - px)
        self.ui.draw_arrow(angle)
        
        if self.state != "PLAYING":
            self.ui.draw_game_over(self.state)
            
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
