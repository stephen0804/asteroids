import pygame
import math
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        # autofire code
        self.ticks_since_last_shot = 0
        self.shots_per_second = 2  # Adjust this number to control firing rate

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
    

    # def rotate(self, dt):
    #     self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    # def update(self, dt):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_a]:
    #         self.rotate(- dt)
    #     if keys[pygame.K_d]:
    #         self.rotate(dt)
    #     if keys[pygame.K_w]:
    #         self.move(dt)
    #     if keys[pygame.K_s]:
    #         self.move(- dt)
    #     if keys[pygame.K_SPACE]:
    #         self.shoot()


    def update(self, dt):
        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate the angle between ship and mouse
        dx = mouse_x - self.position.x
        dy = mouse_y - self.position.y
        
        # Calculate target angle in degrees
        target_angle = math.degrees(math.atan2(dy, dx)) - 90
        
        # Calculate the difference between current and target angle
        # This handles angle wrapping correctly
        angle_diff = (target_angle - self.rotation + 180) % 360 - 180
        
        # Calculate maximum rotation this frame based on turn speed
        max_rotation = PLAYER_TURN_SPEED * dt
        
        # Limit rotation to max speed
        if abs(angle_diff) > max_rotation:
            if angle_diff > 0:
                self.rotation += max_rotation
            else:
                self.rotation -= max_rotation
        else:
            # If we're close enough, just set to target
            self.rotation = target_angle
        self.move(dt)
        
        # Increment the tick counter
        self.ticks_since_last_shot += 1
    
        # Auto-fire logic
        if self.ticks_since_last_shot >= 60 / self.shots_per_second:
            self.shoot()
            self.ticks_since_last_shot = 0  # Reset the counter

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED