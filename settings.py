# Screen attributes
WIDTH = 800
HEIGHT = 600
FPS = 60

# Tile sizes
TILE_SIZE = 40
GRID_WIDTH = 40
GRID_HEIGHT = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100) # Buildings
DARK_GRAY = (50, 50, 50) # Roads
BLUE = (0, 0, 255) # Shalev
GREEN = (0, 255, 0) # Mall "RD Arad"
GRAY = (82, 82, 82) # Haredim
RED = (255, 0, 0) #Loss Screen
YELLOW = (255, 255, 0) # Yair Maayan
ORANGE = (255, 165, 0) # Bus
CYAN = (0, 255, 255) # Ofir

# New palette
SKIN = (255, 218, 185)
DARK_HAT = (30, 30, 30)
WHITE_SHIRT = (240, 240, 240)
JEANS = (40, 80, 150)
ROOF = (70, 70, 70)
ROOF_BORDER = (40, 40, 40)
ASPHALT = (60, 60, 60)
ROAD_LINE = (200, 200, 200)
MALL_COLOR = (46, 204, 113)
MALL_LIGHT = (144, 238, 144)
WINDOW_COLOR = (135, 206, 235)

# Player Settings
PLAYER_SPEED = 200 # pixels per second
PLAYER_RUN_SPEED = 400
PLAYER_STAMINA_MAX = 100
STAMINA_DRAIN_RATE = 25 # points per second
STAMINA_REGEN_RATE = 15

# Enemy Settings
HAREDIM_COUNT = 30
HAREDIM_SPEED = 80
HAREDIM_CHASE_RADIUS = 200

MAYOR_SPEED = 150
MAYOR_CHASE_RADIUS = 400

BUS_SPEED = 250
BUS_TRIGGER_RADIUS = 150 # How close the bus needs to get to Shalev to spawn Ofir

OFIR_SPEED = 150 # Driver chasing speed
OFIR_GIVE_UP_RADIUS = 200 # Distance at which Ofir gives up and returns to bus
