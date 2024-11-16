"""
References
- https://en.wikipedia.org/wiki/Julia_set#Pseudocode
- https://matplotlib.org/stable/gallery/animation/dynamic_image.html
"""

import sys
from cli.cli import cli
from tkinter import Tk
from gui.gui import JuliaSetGUI
from utils.logging import print_usage


if __name__ == "__main__":
    argv, argc = sys.argv, len(sys.argv)

    program_name = argv[0]

    if not program_name:
        print("ERROR: Could not process arguments", file=sys.stderr)
        sys.exit(1)

    if argc < 2:
        print_usage(program_name)
        sys.exit(1)

    try:
        mode = argv[1]
    except IndexError:
        print("ERROR: Could not read mode command", file=sys.stderr)
        print_usage(program_name)
        sys.exit(1)

    if mode == "-cli":
        cli(argv)
    elif mode == "-gui":
        root = Tk()
        app = JuliaSetGUI(root)
        root.mainloop()
    else:
        print(f"ERROR: Unkown mode <{mode}> ", file=sys.stderr)
        print_usage(program_name)
        sys.exit(1)
