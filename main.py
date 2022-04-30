import pygame
import math
pygame.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

#Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 38, 50)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("comicsans", 14)

#planet class
class Planet():
    #Values for easier understasnding
    AU = 149.6e6 * 1000 # distance from earth to sun
    G = 6.67428e-11 # Gravitational force
    SCALE = 200 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # to update planets 1 day at a time

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        #set x and w to position using middle of screen as anchor
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        #draw the circle on WIN
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if len(self.orbit) > 2:
            # make list of points after updating
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distnace_text = FONT.render(f"{self.distance_to_sun/1000}km", 1, WHITE)
            win.blit(distnace_text, (x - distnace_text.get_width()/2, y - distnace_text.get_height()/2 ))

    def attraction(self, other):
        #get x and y from other object
        other_x, other_y = other.x, other.y
        #get x and y difference
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        #calculate distance
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        #apply the force = mM/r^2 eqution
        force = self.G * self.mass * other.mass / distance**2
        #calculate angle
        theta  = math.atan2(distance_y, distance_x)
        #break down angle into x and y
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        #loop through each planet
        for planet in planets:
            if self == planet:
                continue
            
            #calculate total x_vel using each planet
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        #use F = ma eqution to calculate accelaration
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    #limit the fps
    clock = pygame.time.Clock()
    #run
    run = True

    #Define the planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    #Add planets to renderer
    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



