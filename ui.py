import pygame
from settings import *
from custom_font import CustomPixelFont

class UI:
    def __init__(self, surface):
        self.surface = surface
        self.font = CustomPixelFont(3)
        self.small_font = CustomPixelFont(2)

    def draw_stamina_bar(self, stamina):
        ratio = stamina / PLAYER_STAMINA_MAX
        pygame.draw.rect(self.surface, BLACK, (10, 10, 204, 24))
        pygame.draw.rect(self.surface, BLUE, (12, 12, 200 * ratio, 20))
        
        text = self.small_font.render("Stamina", True, WHITE)
        self.surface.blit(text, (15, 12))

    def draw_game_over(self, state):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        self.surface.blit(overlay, (0, 0))
        
        duck = [
            "    __",
            "___( o)>",
            "\\ <_. )",
            " `---'"
        ]
        
        if state == "WIN":
            msg = "Congrats you won!"
            color = GREEN
            duck_y = HEIGHT // 2
            
            # draw duck
            for i, line in enumerate(duck):
                dtext = self.font.render(line, True, YELLOW)
                self.surface.blit(dtext, (WIDTH // 2 - dtext.get_width() // 2, duck_y + i*40))
                
            ktext = self.font.render("Kiril is the king", True, CYAN)
            self.surface.blit(ktext, (WIDTH // 2 - ktext.get_width() // 2, duck_y + len(duck)*40 + 20))
            
        else:
            if state == "LOSE_HAREDIM":
                msg = "You lost! The Dosim caught Shalev."
            elif state == "LOSE_MAYOR":
                msg = "You lost! The Mayor caught Shalev."
            elif state == "LOSE_OFIR":
                msg = "You lost! Ofir caught Shalev."
            else:
                msg = "You lost!"
            color = RED
            
        text = self.font.render(msg, True, color)
        self.surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        
        restart_text = self.small_font.render("Press SPACE or Tap the Screen to restart", True, WHITE)
        self.surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 80))
