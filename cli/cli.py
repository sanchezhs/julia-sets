import sys
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colormaps
from core.julia import julia_set, julia_set_partial
from utils.logging import print_usage


def live_image(cmap: str, c: complex):
    width, height = 800, 800
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("off")

    ims = []
    for i in range(50):
        im = ax.imshow(
            julia_set_partial(width, height, x_min, x_max, y_min, y_max, c, i),
            cmap=cmap,
            extent=(x_min, x_max, y_min, y_max),
            animated=True,
        )
        if i == 0:
            im = ax.imshow(
                julia_set_partial(width, height, x_min, x_max, y_min, y_max, c, 1),
                cmap=cmap,
                extent=(x_min, x_max, y_min, y_max),
            )
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
    ani.save("julia.mp4")
    plt.show()


def shift(argv: list[str]) -> str | None:
    try:
        return argv.pop(0)
    except IndexError:
        return None


def show_cmaps() -> str:
    for idx, cmap in enumerate(list(colormaps)):
        print(f"[{idx}]: {cmap}")

    selected = int(input("Select a cmap (1,2...): "))
    if selected < 0 or selected > len(list(colormaps)):
        print("Wrong index")
        sys.exit(1)
    return list(colormaps)[selected]


def cli(argv: list[str]):
    random.seed(time.clock_gettime(1))

    program_name = shift(argv)
    _ = shift(argv)  # Mode (-cli)

    if len(argv) <= 0:
        print_usage(program_name)

        sys.exit(1)

    if not (command := shift(argv)):
        print(f"Unkown command {command}")
        sys.exit(1)

    c = complex(random.uniform(-3, 3), random.uniform(-3, 3))
    # c = complex(0.285, 0.01)
    # c = complex(-0.7, 0.27015)

    if command == "plot":
        width, height = 800, 800
        x_min, x_max = -1.5, 1.5
        y_min, y_max = -1.5, 1.5
        max_iter = 256

        if not (command := shift(argv)):
            print("ERROR: Subcommand not provided")
            print(f"Usage: python <{program_name}> plot <subcommand>")
            print("Subcommands:")
            print("  save <file_path>")
            sys.exit(1)

        cmap = "twilight"
        if command == "save":
            if not (file_path := shift(argv)):
                print("ERROR: File path not provided.")
                print(f"Usage: python <{program_name}> plot save <file_path>")
                sys.exit(1)

            j_set = julia_set(
                width, height, x_min, x_max, y_min, y_max, c, max_iter, None
            )
            print("Image generated succesfully")

            cmap = show_cmaps()
            plt.figure(figsize=(10, 10))
            plt.imshow(j_set.T, cmap=cmap, extent=(x_min, x_max, y_min, y_max))
            plt.axis("off")
            plt.savefig(file_path)
            sys.exit(0)

        if command == "show":
            j_set = julia_set(
                width, height, x_min, x_max, y_min, y_max, c, max_iter, None
            )
            print("Image generated succesfully")

            cmap = show_cmaps()
            plt.figure(figsize=(10, 10))
            plt.imshow(j_set.T, cmap=cmap, extent=(x_min, x_max, y_min, y_max))
            plt.axis("off")
            plt.show()
            sys.exit(0)

    if command == "live":
        cmap = show_cmaps()
        live_image(cmap, c)

    print(f"Command {command} not supported.")
    sys.exit(1)
