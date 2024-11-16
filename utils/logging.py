def print_usage(program_name: str):
    print(f"Usage: python <{program_name}> <command>")
    print("Commands")
    print(
        "    -cli: Command line mode with different subcommands to draw and save images"
    )
    print("          Subcommands:")
    print("            plot: Generate the image to save it")
    print("            live: Iteratively generate the image")
    print("    -gui: Opens a GUI program where you can visualize the images")
