import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_velocity_A = self.velocity.rotate(random_angle)
        new_velocity_B = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_A = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_B = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_A.velocity = new_velocity_A * 1.2
        asteroid_B.velocity = new_velocity_B * 1.2

