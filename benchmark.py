import timeit

setup = """
cell_radius = 5
center_x = 250
center_y = 250
"""

code_original = """
pixels_added = 0
for dx in range(-cell_radius, cell_radius + 1):
    for dy in range(-cell_radius, cell_radius + 1):
        if dx*dx + dy*dy <= cell_radius*cell_radius:
            px, py = center_x + dx, center_y + dy
            if 0 <= px < 500 and 0 <= py < 500:
                pixels_added += 1
"""

code_optimized = """
pixels_added = 0
cell_radius_squared = cell_radius * cell_radius
for dx in range(-cell_radius, cell_radius + 1):
    for dy in range(-cell_radius, cell_radius + 1):
        if dx*dx + dy*dy <= cell_radius_squared:
            px, py = center_x + dx, center_y + dy
            if 0 <= px < 500 and 0 <= py < 500:
                pixels_added += 1
"""

print("Original:", timeit.timeit(code_original, setup=setup, number=100000))
print("Optimized:", timeit.timeit(code_optimized, setup=setup, number=100000))
