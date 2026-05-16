import cv2
import random


class ImageProcessor:

    def load_image(self, path):

        image = cv2.imread(path)

        if image is None:
            raise Exception("Image not loaded")

        return image


    def generate_differences(self, image):

        modified = image.copy()

        height, width = image.shape[:2]

        difference_regions = []

        while len(difference_regions) < 5:

            region_size = 35

            x = random.randint(
                0,
                width - region_size
            )

            y = random.randint(
                0,
                height - region_size
            )

            overlap = False

            # Check overlap
            for old_x, old_y in difference_regions:

                old_left = old_x
                old_right = old_x + region_size
                old_top = old_y
                old_bottom = old_y + region_size

                new_left = x
                new_right = x + region_size
                new_top = y
                new_bottom = y + region_size

                if (
                    new_left < old_right
                    and new_right > old_left
                    and new_top < old_bottom
                    and new_bottom > old_top
                ):

                    overlap = True
                    break

            if overlap:
                continue

            difference_regions.append((x, y))

            area = modified[
                y:y+region_size,
                x:x+region_size
            ]

            change = random.choice(
                [
                    "colour",
                    "brightness",
                    "blur"
                ]
            )

            # Colour change
            if change == "colour":

                area[:, :, 1] = cv2.add(
                    area[:, :, 1],
                    18
                )

            # Brightness change
            elif change == "brightness":

                modified[
                    y:y+region_size,
                    x:x+region_size
                ] = cv2.convertScaleAbs(
                    area,
                    alpha=1,
                    beta=12
                )

            # Blur effect
            elif change == "blur":

                modified[
                    y:y+region_size,
                    x:x+region_size
                ] = cv2.GaussianBlur(
                    area,
                    (7,7),
                    0
                )

        return modified