import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from image_processor import ImageProcessor


class SpotTheDifferenceGame:

    def __init__(self):

        self.processor = ImageProcessor()

        self.root = tk.Tk()
        self.root.title("Spot The Difference")

        self.region_size = 35

        self.original_image = None
        self.modified_image = None

        self.original_photo = None
        self.modified_photo = None

        self.difference_regions = []
        self.found_regions = []

        self.mistakes = 0
        self.max_mistakes = 3

        self.game_over = False

        self.setup_ui()

    def setup_ui(self):

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.load_button = tk.Button(
            top_frame,
            text="Load Image",
            command=self.load_image
        )
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.reveal_button = tk.Button(
            top_frame,
            text="Reveal",
            command=self.reveal_differences
        )
        self.reveal_button.pack(side=tk.LEFT, padx=5)

        self.remaining_label = tk.Label(
            top_frame,
            text="Remaining: 5"
        )
        self.remaining_label.pack(side=tk.LEFT, padx=20)

        self.mistake_label = tk.Label(
            top_frame,
            text="Mistakes: 0 / 3"
        )
        self.mistake_label.pack(side=tk.LEFT, padx=20)

        image_frame = tk.Frame(self.root)
        image_frame.pack()

        self.original_canvas = tk.Canvas(
            image_frame,
            width=500,
            height=500,
            bg="gray"
        )
        self.original_canvas.pack(side=tk.LEFT, padx=10)

        self.modified_canvas = tk.Canvas(
            image_frame,
            width=500,
            height=500,
            bg="gray"
        )
        self.modified_canvas.pack(side=tk.LEFT, padx=10)

        self.modified_canvas.bind(
            "<Button-1>",
            self.check_click
        )

    def load_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp")
            ]
        )

        if not file_path:
            return

        self.found_regions = []
        self.mistakes = 0
        self.game_over = False

        self.remaining_label.config(
            text="Remaining: 5"
        )

        self.mistake_label.config(
            text="Mistakes: 0 / 3"
        )

        image = self.processor.load_image(file_path)

        modified, regions = (
            self.processor.generate_differences(image)
        )

        self.original_image = image
        self.modified_image = modified

        self.difference_regions = regions

        self.display_images()

    def display_images(self):

        original_rgb = cv2.cvtColor(
            self.original_image,
            cv2.COLOR_BGR2RGB
        )

        modified_rgb = cv2.cvtColor(
            self.modified_image,
            cv2.COLOR_BGR2RGB
        )

        original_pil = Image.fromarray(original_rgb)
        modified_pil = Image.fromarray(modified_rgb)

        self.original_photo = ImageTk.PhotoImage(original_pil)
        self.modified_photo = ImageTk.PhotoImage(modified_pil)

        self.original_canvas.config(
            width=original_pil.width,
            height=original_pil.height
        )

        self.modified_canvas.config(
            width=modified_pil.width,
            height=modified_pil.height
        )

        self.original_canvas.delete("all")
        self.modified_canvas.delete("all")

        self.original_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.original_photo
        )

        self.modified_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.modified_photo
        )

    def check_click(self, event):

        if self.game_over:
            return

        click_x = event.x
        click_y = event.y

        found = False

        for region in self.difference_regions:

            if region in self.found_regions:
                continue

            x, y = region

            if (
                click_x >= x
                and click_x <= x + self.region_size
                and click_y >= y
                and click_y <= y + self.region_size
            ):

                self.found_regions.append(region)

                self.draw_circle(
                    x,
                    y,
                    "red"
                )

                remaining = (
                    5 - len(self.found_regions)
                )

                self.remaining_label.config(
                    text=f"Remaining: {remaining}"
                )

                found = True
                break

        if not found:

            self.mistakes += 1

            self.mistake_label.config(
                text=f"Mistakes: {self.mistakes} / 3"
            )

            if self.mistakes >= self.max_mistakes:

                self.game_over = True

                messagebox.showerror(
                    "Game Over",
                    (
                        "Too many mistakes!\n"
                        f"You found "
                        f"{len(self.found_regions)} "
                        f"differences."
                    )
                )

        if len(self.found_regions) == 5:

            self.game_over = True

            messagebox.showinfo(
                "Congratulations!",
                "You found all 5 differences!"
            )

    def draw_circle(self, x, y, colour):

        padding = 5

        left = x - padding
        top = y - padding

        right = (
            x + self.region_size + padding
        )

        bottom = (
            y + self.region_size + padding
        )

        self.original_canvas.create_oval(
            left,
            top,
            right,
            bottom,
            outline=colour,
            width=3
        )

        self.modified_canvas.create_oval(
            left,
            top,
            right,
            bottom,
            outline=colour,
            width=3
        )

    def reveal_differences(self):

        for region in self.difference_regions:

            if region not in self.found_regions:

                x, y = region

                self.draw_circle(
                    x,
                    y,
                    "blue"
                )

        self.game_over = True

    def run(self):

        self.root.mainloop()