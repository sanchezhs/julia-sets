import numpy as np
from numpy._typing import NDArray
from tqdm import tqdm


def julia_set(
    width: int,
    height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    c: complex,
    max_iter: int,
    progress_callback,
) -> NDArray[np.float64]:
    julia_set = np.zeros((width, height))

    for x in range(width):
        for y in range(height):
            # Transform pixel coords to complex plane
            zx = x * (x_max - x_min) / (width - 1) + x_min
            zy = y * (y_max - y_min) / (height - 1) + y_min
            z = complex(zx, zy)

            iteration = 0
            while abs(z) < 4 and iteration < max_iter:
                z = z**2 + c
                iteration += 1

            julia_set[x, y] = iteration

        if progress_callback:
            # progress = (x + 1) / max_iter * 100
            progress = x / width * 100
            progress_callback(progress)

    return julia_set


def julia_set_partial(width, height, x_min, x_max, y_min, y_max, c, current_iter):
    julia_set = np.zeros((width, height))

    for x in range(width):
        for y in range(height):
            zx = x * (x_max - x_min) / (width - 1) + x_min
            zy = y * (y_max - y_min) / (height - 1) + y_min
            z = complex(zx, zy)

            iteration = 0
            while abs(z) < 4 and iteration < current_iter:
                z = z**2 + c
                iteration += 1

            julia_set[x, y] = iteration
    return julia_set
