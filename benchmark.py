import math
import time

def create_simple_fiber_list(start_x, start_y, angle, fiber_length):
    pixels = []
    dx = math.cos(angle)
    dy = math.sin(angle)

    for i in range(fiber_length):
        x = int(start_x + i * dx)
        y = int(start_y + i * dy)

        if 50 <= x < 450 and 50 <= y < 450:
            pixels.append((x, y))
            # Add slight thickness
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + offset[0], y + offset[1]
                if 50 <= nx < 450 and 50 <= ny < 450:
                    if (nx, ny) not in pixels:
                        pixels.append((nx, ny))
    return pixels

def create_simple_fiber_set(start_x, start_y, angle, fiber_length):
    pixels = []
    seen_pixels = set()
    dx = math.cos(angle)
    dy = math.sin(angle)

    for i in range(fiber_length):
        x = int(start_x + i * dx)
        y = int(start_y + i * dy)

        if 50 <= x < 450 and 50 <= y < 450:
            pixels.append((x, y))
            seen_pixels.add((x, y))
            # Add slight thickness
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + offset[0], y + offset[1]
                if 50 <= nx < 450 and 50 <= ny < 450:
                    if (nx, ny) not in seen_pixels:
                        pixels.append((nx, ny))
                        seen_pixels.add((nx, ny))
    return pixels

def run_benchmarks():
    iterations = 10000
    fiber_length = 50
    start_x, start_y = 100, 100
    angle = 1.0

    # Warmup and verify
    assert create_simple_fiber_list(start_x, start_y, angle, fiber_length) == create_simple_fiber_set(start_x, start_y, angle, fiber_length)

    start_time = time.time()
    for _ in range(iterations):
        create_simple_fiber_list(start_x, start_y, angle, fiber_length)
    list_time = time.time() - start_time

    start_time = time.time()
    for _ in range(iterations):
        create_simple_fiber_set(start_x, start_y, angle, fiber_length)
    set_time = time.time() - start_time

    print(f"List check time: {list_time:.4f} seconds")
    print(f"Set check time: {set_time:.4f} seconds")
    print(f"Improvement: {(list_time - set_time) / list_time * 100:.2f}%")

if __name__ == '__main__':
    run_benchmarks()
