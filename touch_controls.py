import pygame
import math
from settings import *

class TouchControls:
    def __init__(self, surface_rect):
        self.surface_rect = surface_rect
        self.active_fingers = {} # finger_id: {start_pos: (x, y), current_pos: (x, y), type: "dpad" or "sprint"}
        
        # D-pad center (bottom left)
        self.dpad_center = (100, self.surface_rect.height - 100)
        self.dpad_radius = 60
        self.dpad_deadzone = 10
        
        # Sprint button (bottom right)
        self.sprint_center = (self.surface_rect.width - 100, self.surface_rect.height - 100)
        self.sprint_radius = 50
        
        self.dx = 0
        self.dy = 0
        self.is_sprinting = False

    def process_event(self, event):
        if event.type == pygame.FINGERDOWN:
            x = event.x * self.surface_rect.width
            y = event.y * self.surface_rect.height
            finger_id = event.finger_id
            
            # Check if touch is near D-pad
            dist_dpad = math.hypot(x - self.dpad_center[0], y - self.dpad_center[1])
            if dist_dpad < self.dpad_radius * 2: # generously allow touching reasonably close 
                self.active_fingers[finger_id] = {"start_pos": (x, y), "current_pos": (x, y), "type": "dpad"}
                self.update_movement()
                return True
                
            # Check if touch is near Sprint button
            dist_sprint = math.hypot(x - self.sprint_center[0], y - self.sprint_center[1])
            if dist_sprint < self.sprint_radius * 2:
                self.active_fingers[finger_id] = {"start_pos": (x, y), "current_pos": (x, y), "type": "sprint"}
                self.is_sprinting = True
                return True
                
            # For general screen taps (e.g. restarting)
            return "tap"

        elif event.type == pygame.FINGERMOTION:
            finger_id = event.finger_id
            if finger_id in self.active_fingers:
                x = event.x * self.surface_rect.width
                y = event.y * self.surface_rect.height
                self.active_fingers[finger_id]["current_pos"] = (x, y)
                if self.active_fingers[finger_id]["type"] == "dpad":
                    self.update_movement()
                return True

        elif event.type == pygame.FINGERUP:
            finger_id = event.finger_id
            if finger_id in self.active_fingers:
                if self.active_fingers[finger_id]["type"] == "dpad":
                    self.dx = 0
                    self.dy = 0
                elif self.active_fingers[finger_id]["type"] == "sprint":
                    self.is_sprinting = False
                del self.active_fingers[finger_id]
                return True
        return False

    def update_movement(self):
        self.dx = 0
        self.dy = 0
        dpad_finger = next((f for f in self.active_fingers.values() if f["type"] == "dpad"), None)
        if dpad_finger:
            start_x, start_y = dpad_finger["start_pos"]
            curr_x, curr_y = dpad_finger["current_pos"]
            
            dx = curr_x - start_x
            dy = curr_y - start_y
            
            dist = math.hypot(dx, dy)
            if dist > self.dpad_deadzone:
                # Normalize direction
                self.dx = dx / dist
                self.dy = dy / dist

    def get_input(self):
        return self.dx, self.dy, self.is_sprinting
        
    def draw(self, surface):
        # D-Pad
        dpad_bg = pygame.Surface((self.dpad_radius * 2, self.dpad_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(dpad_bg, (255, 255, 255, 100), (self.dpad_radius, self.dpad_radius), self.dpad_radius)
        surface.blit(dpad_bg, (self.dpad_center[0] - self.dpad_radius, self.dpad_center[1] - self.dpad_radius))
        
        # Draw joystick knob if active
        dpad_finger = next((f for f in self.active_fingers.values() if f["type"] == "dpad"), None)
        if dpad_finger:
            start_x, start_y = dpad_finger["start_pos"]
            curr_x, curr_y = dpad_finger["current_pos"]
            
            # Constrain knob to dpad background radius visually
            dx = curr_x - start_x
            dy = curr_y - start_y
            dist = math.hypot(dx, dy)
            if dist > self.dpad_radius:
                dx = (dx / dist) * self.dpad_radius
                dy = (dy / dist) * self.dpad_radius
                
            knob_x = self.dpad_center[0] + dx
            knob_y = self.dpad_center[1] + dy
            
            pygame.draw.circle(surface, (255, 255, 255, 180), (int(knob_x), int(knob_y)), 20)
        else:
            pygame.draw.circle(surface, (255, 255, 255, 180), self.dpad_center, 20)
            
        # Sprint Button
        sprint_alpha = 180 if self.is_sprinting else 100
        sprint_bg = pygame.Surface((self.sprint_radius * 2, self.sprint_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(sprint_bg, (255, 255, 255, sprint_alpha), (self.sprint_radius, self.sprint_radius), self.sprint_radius)
        surface.blit(sprint_bg, (self.sprint_center[0] - self.sprint_radius, self.sprint_center[1] - self.sprint_radius))
        
        # Simple text for Sprint
        font = pygame.font.Font(None, 24)
        text = font.render("SPRINT", True, (0, 0, 0))
        surface.blit(text, (self.sprint_center[0] - text.get_width() // 2, self.sprint_center[1] - text.get_height() // 2))
