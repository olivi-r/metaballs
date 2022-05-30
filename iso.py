import math, random
import os; os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import noise

dimensions = [600, 400]
pixel_scale = 10

number_of_balls = 10

def rotate2d(vec, angle):
    i = vec[0] * math.cos(math.radians(angle)) - vec[1] * math.sin(math.radians(angle))
    j = vec[0] * math.sin(math.radians(angle)) + vec[1] * math.cos(math.radians(angle))
    vec[0] = i
    vec[1] = j

# initialize colour space offsets
# colours turn in circles in 2d perlin space so colours cycle nicely
t = 0  # angle around circle of colour
off_r = [random.randint(1, 100) for _ in range(2)]
off_g = [random.randint(1, 100) for _ in range(2)]
off_b = [random.randint(1, 100) for _ in range(2)]

def get_colour_scales(t):
    # adjusts colours gradually with perlin noise
    r = [math.sin(math.radians(t + 2)), math.cos(math.radians(t + 2))]
    g = [math.sin(math.radians(t + 1)), math.cos(math.radians(t + 1))]
    b = [math.sin(math.radians(t)), math.cos(math.radians(t))]
    r = (1 + noise.pnoise2(off_r[0] + r[0], off_r[1] + r[1])) / 2
    g = (1 + noise.pnoise2(off_g[0] + g[0], off_g[1] + g[1])) / 2
    b = (1 + noise.pnoise2(off_b[0] + b[0], off_b[1] + b[1])) / 2
    return r, g, b


class Metaball:
    def __init__(self, radius, initial_x, initial_y, direction, speed):
        self.radius = radius
        self.x = initial_x
        self.y = initial_y
        self.direction = direction
        self.speed = speed / pixel_scale

    def update(self):
        # bounce on edge (+ some slight variation)
        if self.x < 0 or self.x > dimensions[0] // pixel_scale:
            self.direction[0] *= -1
            rotate2d(self.direction, (random.randint(0, 2) - 1))

        if self.y < 0 or self.y > dimensions[1] // pixel_scale:
            self.direction[1] *= -1
            rotate2d(self.direction, (random.randint(0, 20)/5 - 2))

        # move in direction
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed


# initialize metaballs
metaballs = []
for i in range(number_of_balls):
    dir = math.radians(random.randint(0, 360))
    dir = [math.cos(dir), math.sin(dir)]
    metaballs.append(Metaball(
        random.randint(3, min(3, 69 // number_of_balls)), random.randrange(0, dimensions[0] // pixel_scale),
        random.randrange(0, dimensions[1] // pixel_scale), dir, random.randrange(5, 10)
    ))


# initialize display
pygame.init()
display = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Metaballs")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False

    display.fill((255, 255, 255))
    # random.seed(1)
    for x in range(dimensions[0] // pixel_scale):
        for y in range(dimensions[1] // pixel_scale):                
            point = pygame.mouse.get_pos()
            dist = 0
            for ball in metaballs:
                try:
                    dist += ball.radius / math.sqrt((ball.x - x) ** 2 + (ball.y - y) ** 2)

                except ZeroDivisionError:
                    dist += float("inf")

            dist *= 100
            dist = max(0, min(255, dist))
            scale_r, scale_g, scale_b = get_colour_scales(t)

            # screen divided into small blocks so as to increase performace instead of using individual pixels
            pygame.draw.rect(
                display, (scale_r * dist, scale_g * dist, scale_b * dist),
                ((x * pixel_scale, y * pixel_scale), ((x + 1) * pixel_scale, (y + 1) * pixel_scale))
            )

    t += 0.5
    for ball in metaballs:
        ball.update()

    pygame.display.update()

pygame.quit()
