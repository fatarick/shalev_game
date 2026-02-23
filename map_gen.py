import random
from settings import GRID_WIDTH, GRID_HEIGHT

def generate_map():
    """Generates a connected grid of roads with buildings, returning the grid and start/end locations."""
    # 0 = building, 1 = road, 2 = mall
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Generate intersecting straight roads to form city blocks
    num_h_roads = max(5, GRID_HEIGHT // 5)
    num_v_roads = max(5, GRID_WIDTH // 5)
    
    h_roads = []
    while len(h_roads) < num_h_roads:
        y = random.randint(1, GRID_HEIGHT - 2)
        if y not in h_roads and (y-1) not in h_roads and (y+1) not in h_roads: # space out roads
            h_roads.append(y)
            for x in range(1, GRID_WIDTH - 1):
                grid[y][x] = 1
                
    v_roads = []
    while len(v_roads) < num_v_roads:
        x = random.randint(1, GRID_WIDTH - 2)
        if x not in v_roads and (x-1) not in v_roads and (x+1) not in v_roads:
            v_roads.append(x)
            for y in range(1, GRID_HEIGHT - 1):
                grid[y][x] = 1

    h_roads.sort()
    v_roads.sort()
    
    # Player starts top-leftish intersection
    start_x = v_roads[0] if v_roads else GRID_WIDTH // 2
    start_y = h_roads[0] if h_roads else GRID_HEIGHT // 2
    
    # Mall placed random intersection (away from start if possible)
    mall_idx_v = random.randint(min(1, len(v_roads)-1), len(v_roads)-1) if len(v_roads) > 1 else 0
    mall_idx_h = random.randint(min(1, len(h_roads)-1), len(h_roads)-1) if len(h_roads) > 1 else 0
    mall_x = v_roads[mall_idx_v] if v_roads else GRID_WIDTH // 2
    mall_y = h_roads[mall_idx_h] if h_roads else GRID_HEIGHT // 2
    
    # Make the mall slightly larger, e.g., 2x2 blocks if possible
    grid[mall_y][mall_x] = 2
    if mall_y + 1 < GRID_HEIGHT: grid[mall_y + 1][mall_x] = 2
    if mall_x + 1 < GRID_WIDTH: grid[mall_y][mall_x + 1] = 2
    if mall_y + 1 < GRID_HEIGHT and mall_x + 1 < GRID_WIDTH: grid[mall_y + 1][mall_x + 1] = 2
    
    return grid, (start_x, start_y), (mall_x, mall_y)
