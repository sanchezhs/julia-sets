import queue
import random
import threading
from collections import namedtuple
from tkinter import *
from tkinter import filedialog, ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from PIL import Image, ImageTk

from core.julia import julia_set


class JuliaSetImage:
    def __init__(
        self,
        width=800,
        height=800,
        x_min=-2,
        x_max=2,
        y_min=-2,
        y_max=2,
        c=complex(0, 0),
        max_iter=100,
        colorscheme="twilight",
    ):
        self.width = width
        self.height = height
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_min
        self.c = c
        self.max_iter = max_iter
        self.colorscheme = colorscheme
        self.image = None

    def generate_image_data(self, progress_callback):
        aspect_ratio = self.width / self.height
        j_set = julia_set(
            self.width,
            self.height,
            self.x_min * aspect_ratio,
            self.x_max * aspect_ratio,
            self.y_min,
            self.y_max,
            self.c,
            self.max_iter,
            progress_callback,
        )
        return j_set

    def save_image(self, file_path: str):
        if self.image:
            self.image.save(file_path)
        else:
            print("No hay una imagen generada para guardar.")


class JuliaSetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generate")
        self.root.geometry("850x600")
        self.julia_image = JuliaSetImage()
        self.setup_ui()
        self.queue = queue.Queue()
        self.progress_queue = queue.Queue()
        self.updating = False

    def setup_ui(self):
        # Configuración de la interfaz de usuario
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame para la gráfica
        self.frame_canvas = Frame(self.root, bg="white")
        self.frame_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.canvas = Canvas(self.frame_canvas, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

        # Frame para los controles
        self.frame_controls = Frame(self.root)
        self.frame_controls.grid(row=1, column=0, pady=10, sticky="ew")

        # Sección de Rango del Plano Complejo
        self.setup_range_controls()

        # Sección de Parámetro Complejo c
        self.setup_c_controls()

        # Sección de Iteraciones
        self.setup_iteration_controls()

        # Opciones de imagen
        self.setup_image_options()

        # Botón para generar el conjunto de Julia
        self.generate_button = ttk.Button(
            self.root,
            text="Generate",
            command=self.generate_image_async,
        )
        self.generate_button.grid(row=2, column=0, pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", length=400, mode="determinate"
        )
        self.progress.grid(row=3, column=0, pady=5)
        self.progress.grid_remove()

    def setup_range_controls(self):
        X_RANGE_T = namedtuple("X_RANGE", ["max", "min"])
        Y_RANGE_T = namedtuple("Y_RANGE", ["max", "min"])
        X_RANGE = X_RANGE_T(-10, 10)
        Y_RANGE = Y_RANGE_T(-10, 10)

        range_frame = ttk.LabelFrame(
            self.frame_controls, text="Complex Plane Range", padding=(10, 5)
        )
        range_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.x_min_slider = Scale(
            range_frame,
            from_=X_RANGE.max,
            to=X_RANGE.min,
            orient=HORIZONTAL,
            length=150,
            resolution=0.01,
            label="Min X",
        )
        self.x_min_slider.set(-2)
        self.x_min_slider.grid(row=0, column=0, padx=5)

        self.x_max_slider = Scale(
            range_frame,
            from_=X_RANGE.max,
            to=X_RANGE.min,
            orient=HORIZONTAL,
            length=150,
            resolution=0.01,
            label="Max X",
        )
        self.x_max_slider.set(2)
        self.x_max_slider.grid(row=0, column=1, padx=5)

        self.y_min_slider = Scale(
            range_frame,
            from_=Y_RANGE.max,
            to=Y_RANGE.min,
            orient=HORIZONTAL,
            length=150,
            resolution=0.01,
            label="Min Y",
        )
        self.y_min_slider.set(-2)
        self.y_min_slider.grid(row=1, column=0, padx=5)

        self.y_max_slider = Scale(
            range_frame,
            from_=Y_RANGE.max,
            to=Y_RANGE.min,
            orient=HORIZONTAL,
            length=150,
            resolution=0.01,
            label="Max Y",
        )
        self.y_max_slider.set(2)
        self.y_max_slider.grid(row=1, column=1, padx=5)

    def setup_c_controls(self):
        c_frame = ttk.LabelFrame(
            self.frame_controls, text="Complex param (c = a + bi)", padding=(10, 5)
        )
        c_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        Label(c_frame, text="Re").grid(row=0, column=0, padx=5)
        self.re_entry = Entry(c_frame, width=10)
        self.re_entry.grid(row=0, column=1, padx=5)
        self.re_entry.insert(0, "0")

        Label(c_frame, text="Im").grid(row=0, column=2, padx=5)
        self.im_entry = Entry(c_frame, width=10)
        self.im_entry.grid(row=0, column=3, padx=5)
        self.im_entry.insert(0, "0")

        # Botón para generar un valor aleatorio de c
        random_button = ttk.Button(
            c_frame, text="Random", command=self.generate_random_c
        )
        random_button.grid(row=0, column=4, padx=10)

    def setup_iteration_controls(self):
        iter_frame = ttk.LabelFrame(
            self.frame_controls, text="Iterations", padding=(10, 5)
        )
        iter_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        Label(iter_frame, text="Max iterations").grid(row=0, column=0, padx=5)
        self.max_iter_entry = Entry(iter_frame, width=10)
        self.max_iter_entry.grid(row=0, column=1, padx=5)
        self.max_iter_entry.insert(0, "100")

    def setup_image_options(self):
        image_frame = ttk.LabelFrame(
            self.frame_controls, text="Image Options", padding=(10, 5)
        )
        image_frame.grid(row=0, column=1, padx=10, pady=0, sticky="ew")

        Label(image_frame, text="Colorscheme").grid(row=0, column=0, padx=5)
        self.colorscheme_combobox = ttk.Combobox(
            image_frame,
            values=list(colormaps),
            state="readonly",
        )
        self.colorscheme_combobox.grid(row=0, column=1, padx=5)
        self.colorscheme_combobox.set("twilight")

        save_img_button = ttk.Button(
            image_frame,
            text="Save Image",
            command=self.save_image,
        )
        save_img_button.grid(row=1, column=0, pady=10, padx=5)

    def generate_random_c(self):
        re = random.uniform(-2, 2)
        im = random.uniform(-2, 2)
        self.re_entry.delete(0, END)
        self.re_entry.insert(0, f"{re:.2f}")
        self.im_entry.delete(0, END)
        self.im_entry.insert(0, f"{im:.2f}")

    def generate_image_async(self):
        if not self.updating:
            self.generate_button["state"] = "disabled"
            self.updating = True
            self.progress["value"] = 0
            self.progress.grid()
            threading.Thread(target=self.generate_image_background).start()
            self.root.after(100, self.check_queue)
            self.root.after(25, self.check_progress_queue)

    def generate_image_background(self):
        try:
            # Actualizar parámetros
            self.julia_image.width = self.canvas.winfo_width()
            self.julia_image.height = self.canvas.winfo_height()
            self.julia_image.x_min = float(self.x_min_slider.get())
            self.julia_image.x_max = float(self.x_max_slider.get())
            self.julia_image.y_min = float(self.y_min_slider.get())
            self.julia_image.y_max = float(self.y_max_slider.get())
            self.julia_image.c = complex(
                float(self.re_entry.get()), float(self.im_entry.get())
            )
            self.julia_image.max_iter = int(self.max_iter_entry.get())
            self.julia_image.colorscheme = self.colorscheme_combobox.get()

            # Generar datos de imagen (esto puede ser intensivo)
            image_data = self.julia_image.generate_image_data(
                progress_callback=self.report_progress
            )

            # Poner los datos en la cola para que el hilo principal los procese
            self.queue.put(image_data)
            self.generate_button["state"] = "normal"
        except Exception as e:
            print("Error al generar la imagen:", e)
            self.queue.put(None)
            self.generate_button["state"] = "normal"

    def report_progress(self, progress):
        self.progress_queue.put(progress)

    def check_progress_queue(self):
        try:
            while True:
                progress = self.progress_queue.get_nowait()
                self.progress["value"] = progress
        except queue.Empty:
            pass
        if self.updating:
            self.root.after(25, self.check_progress_queue)

    def check_queue(self):
        try:
            image_data = self.queue.get_nowait()
        except queue.Empty:
            self.root.after(100, self.check_queue)
            return

        if image_data is not None:
            self.display_image(image_data)
        else:
            print("No se pudo generar la imagen.")

        self.updating = False
        self.progress["value"] = 100
        self.progress.grid_remove()

    def display_image(self, image_data):
        norm = plt.Normalize(vmin=image_data.min(), vmax=image_data.max())
        cmap = plt.get_cmap(self.julia_image.colorscheme)
        image_rgb = cmap(norm(image_data))
        image_rgb = (image_rgb[:, :, :3] * 255).astype(np.uint8)
        self.julia_image.image = Image.fromarray(image_rgb)
        self.julia_image.image = self.julia_image.image.resize(
            (self.julia_image.width, self.julia_image.height)
        )

        img_tk = ImageTk.PhotoImage(self.julia_image.image)
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            self.julia_image.save_image(file_path)


if __name__ == "__main__":
    root = Tk()
    app = JuliaSetGUI(root)
    root.mainloop()
