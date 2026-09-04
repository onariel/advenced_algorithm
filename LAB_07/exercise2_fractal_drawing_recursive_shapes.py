import matplotlib.pyplot as plt
import numpy as np
import math

def draw_triangle(ax, p1, p2, p3):
    x = [p1[0], p2[0], p3[0], p1[0]]
    y = [p1[1], p2[1], p3[1], p1[1]]
    ax.fill(x, y)


def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def draw_sierpinski(ax, p1, p2, p3, depth):
    if depth == 0:
        draw_triangle(ax, p1, p2, p3)
        return

    m12 = midpoint(p1, p2)
    m23 = midpoint(p2, p3)
    m31 = midpoint(p3, p1)

    draw_sierpinski(ax, p1, m12, m31, depth - 1)
    draw_sierpinski(ax, m12, p2, m23, depth - 1)
    draw_sierpinski(ax, m31, m23, p3, depth - 1)


def draw_tree(ax, x, y, length, angle, depth):
    if depth == 0:
        return

    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    ax.plot([x, x2], [y, y2])

    draw_tree(ax, x2, y2, length * 0.7, angle + 30, depth - 1)
    draw_tree(ax, x2, y2, length * 0.7, angle - 30, depth - 1)


def fractal_dimension(image, box_sizes):
    counts = []

    rows, cols = image.shape

    for size in box_sizes:
        count = 0

        for i in range(0, rows, size):
            for j in range(0, cols, size):
                box = image[i:i + size, j:j + size]
                if np.any(box):
                    count += 1

        counts.append(count)

    x = np.log(1 / np.array(box_sizes))
    y = np.log(np.array(counts))

    slope = np.polyfit(x, y, 1)[0]
    return slope


fig, ax = plt.subplots(figsize=(8, 8))

draw_sierpinski(ax, (0, 0), (1, 0), (0.5, 0.866), 5)

draw_tree(ax, 0.5, 0, 0.2, 90, 5)

ax.set_aspect('equal')
ax.axis('off')
plt.show()
