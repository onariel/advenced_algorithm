import random
import turtle as t
from turtle import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import numpy as np


def mid_point_displacement(roughness, depth, grid, count):
    if depth == 0:
        return grid
    midpoint = ((grid[0][0] + grid[-1][0]) / 2, (grid[0][1] + grid[-1][1]) / 2)
    middle = len(grid)//2
    count[0] += 1
    grid[middle][1] = midpoint[1] + roughness * (random.randint(-100,100)/100)
    mid_point_displacement(roughness, depth - 1, grid[:middle+1], count)
    mid_point_displacement(roughness, depth - 1, grid[middle:], count)

    return grid

def generate_terrain(roughness, depth, grid):
    if depth == 0:
        return grid
    center = (len(grid)-1)//2

    grid[center][center] = round(((grid[0][0] + grid[-1][0] + grid[0][-1] + grid[-1][-1] ) / 4) + random.uniform(-roughness, roughness),3)

    grid[0][center] = round(((grid[0][0] + grid[-1][0] + grid[center][center] ) / 3) + random.uniform(-roughness, roughness),3)
    grid[-1][center] = round(((grid[-1][0] + grid[-1][-1] + grid[center][center] ) / 3) + random.uniform(-roughness, roughness),3)
    grid[center][0] = round(((grid[0][0] + grid[0][-1] + grid[center][center] ) / 3) + random.uniform(-roughness, roughness),3)
    grid[center][-1] = round(((grid[0][-1] + grid[-1][-1] + grid[center][center] ) / 3) + random.uniform(-roughness, roughness),3)

    generate_terrain(roughness/2, depth - 1, grid[:center+1, center:])
    generate_terrain(roughness/2, depth - 1, grid[center:, center:])
    generate_terrain(roughness/2, depth - 1, grid[center:, :center+1])
    generate_terrain(roughness/2, depth - 1, grid[:center+1, :center+1])
    return grid

def print_grid(grid):
    for row in grid:
        print(row)

def diamond_square(roughness, depth):
    grid = create2dgrid(depth)
    grid[0][0] = round(random.uniform(-roughness, roughness),3)
    grid[-1][-1] = round(random.uniform(-roughness, roughness),3)
    grid[-1][0] = round(random.uniform(-roughness, roughness),3)
    grid[0][-1] = round(random.uniform(-roughness, roughness),3)
    print("grid before")
    print_grid(grid)
    grid = np.array(grid)
    return generate_terrain(roughness, depth, grid)


def visualize_terrain(matrix):
    # 1. Define your exact colors (hex or names)
    # Blue (Water), Green (Grass), Brown (Mountains), White (Snow)
    colors = ['#1f77b4', '#2ca02c', '#8b4513', '#ffffff']

    # 2. Create the discrete colormap
    cmap = mcolors.ListedColormap(colors)

    # 3. Define the elevation boundaries for each color
    # Assuming your matrix values are normalized between 0 and 1
    # Boundaries: [Min, Water_End, Grass_End, Mountain_End, Max]
    boundaries = [0, 0.3, 0.6, 0.85, 1.0]
    norm = mcolors.BoundaryNorm(boundaries, cmap.N)

    fig = plt.figure(figsize=(15, 7))

    # --- 2D Map View ---
    ax1 = fig.add_subplot(1, 2, 1)
    # Use 'nearest' interpolation to ensure colors don't bleed into each other
    im = ax1.imshow(matrix, cmap=cmap, norm=norm, interpolation='nearest', origin='lower')
    ax1.set_title("Discrete 2D Map")

    # Add colorbar with specific labels
    cbar = plt.colorbar(im, ax=ax1, ticks=[0.15, 0.45, 0.72, 0.92])
    cbar.ax.set_yticklabels(['Water', 'Grass', 'Mountain', 'Snow'])

    # --- 3D Perspective View ---
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')

    rows, cols = matrix.shape
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))

    # To keep ONLY your colors without any lighting shadows, set shade=False
    # However, this makes 3D depth hard to see.
    # To see the shape with ONLY your colors, we use antialiased=False
    surf = ax2.plot_surface(x, y, matrix, cmap=cmap, norm=norm,
                            shade=False, linewidth=0, antialiased=False)

    ax2.set_title("Discrete 3D Terrain")
    ax2.view_init(elev=45, azim=-45)

    plt.tight_layout()
    plt.show()

def create1dgrid(depth):
    grid = []
    for i in range(3*2**depth*-1, (3*2**depth)+2 , 2):
        grid.append([i,0])
    return grid

def create2dgrid(depth):
    grid = []
    for i in range(2**depth+1):
        grid.append([])
        for j in range(2**depth+1):
            grid[i].append(0)
    return grid

def detect_artifacts(grid, sensibility):
    length = len(grid)
    lowest = grid[0][0]
    biggest = grid[0][0]
    for row in grid:
        for pixel in row:
            if pixel < lowest:
                lowest = pixel
            if biggest < pixel:
                biggest = pixel
    detection_fator = (biggest - lowest)/ sensibility
    suspicious = []
    for i in range(1,length-1):
        for n in range(1, length-1):
            if abs(grid[i-1][n] - grid[i][n]) > detection_fator:
                if not [i,n] in suspicious:
                    suspicious.append([i,n])
            if abs(grid[i][n-1] - grid[i][n]) > detection_fator:
                if not [i, n] in suspicious:
                    suspicious.append([i, n])
            if abs(grid[i][n+1] - grid[i][n]) > detection_fator:
                if not [i, n] in suspicious:
                    suspicious.append([i, n])
            if abs(grid[i+1][n] - grid[i][n]) > detection_fator:
                if not [i, n] in suspicious:
                    suspicious.append([i, n])
    return suspicious


grid1d = create1dgrid(8)
count = [0]
grid1d = mid_point_displacement(10, 10, grid1d, count)
print(count)
t.teleport(grid1d[0][0],0)
for point in grid1d:
    t.goto(point)


grid2d = diamond_square(0.8, 2)
print("\nfinal grid: ")
print_grid(grid2d)
print("\n suspicious pixel: ",detect_artifacts(grid2d, 2))
visualize_terrain(grid2d)

t.mainloop()