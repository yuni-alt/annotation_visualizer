import cv2
import numpy as np

from colors import (
    get_color,
    get_alpha,
    get_border_thickness,
    get_font_scale,
    get_font_thickness,
    get_text_color,
)


class AnnotationRenderer:

    def __init__(self, coco_json):

        self.data = coco_json

        self.categories = {
            c["id"]: c["name"]
            for c in coco_json["categories"]
        }

        self.images = {
            img["id"]: img
            for img in coco_json["images"]
        }

        self.annotations = coco_json["annotations"]

    # ----------------------------------------------------

    def get_annotations(self, image_id):

        anns = [
            a for a in self.annotations
            if a["image_id"] == image_id
        ]

        anns.sort(
            key=lambda x: x["bbox"][2] * x["bbox"][3],
            reverse=True
        )

        return anns

    # ----------------------------------------------------

    def draw(self, image, image_id):

        img = image.copy()
        overlay = image.copy()

        annotations = self.get_annotations(image_id)

        used_labels = []

        for ann in annotations:

            x, y, w, h = ann["bbox"]

            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)

            category = ann["category_id"]

            label = self.categories.get(
                category,
                str(category)
            )

            color = get_color(category)

            # ------------------------------------------
            # Transparent Fill
            # ------------------------------------------

            cv2.rectangle(
                overlay,
                (x, y),
                (x + w, y + h),
                color,
                -1
            )

            # ------------------------------------------
            # Border
            # ------------------------------------------

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                color,
                get_border_thickness()
            )

            # ------------------------------------------
            # Label Size
            # ------------------------------------------

            font = cv2.FONT_HERSHEY_SIMPLEX

            scale = get_font_scale()

            thickness = get_font_thickness()

            (tw, th), _ = cv2.getTextSize(
                label,
                font,
                scale,
                thickness
            )

            label_x = x
            label_y = y - 8

            # Keep label inside image

            if label_y < th + 5:
                label_y = y + h + th + 8

            # ------------------------------------------
            # Prevent overlap
            # ------------------------------------------

            while True:

                overlap = False

                for rx1, ry1, rx2, ry2 in used_labels:

                    if (
                        label_x < rx2 and
                        label_x + tw + 8 > rx1 and
                        label_y - th - 8 < ry2 and
                        label_y > ry1
                    ):

                        label_y = ry2 + th + 6
                        overlap = True
                        break

                if not overlap:
                    break

            used_labels.append(
                (
                    label_x,
                    label_y - th - 8,
                    label_x + tw + 8,
                    label_y
                )
            )

            # ------------------------------------------
            # Label Background
            # ------------------------------------------

            cv2.rectangle(
                img,
                (label_x, label_y - th - 8),
                (label_x + tw + 8, label_y),
                color,
                -1
            )

            # ------------------------------------------
            # Label Text
            # ------------------------------------------

            cv2.putText(
                img,
                label,
                (label_x + 4, label_y - 4),
                font,
                scale,
                get_text_color(),
                thickness,
                cv2.LINE_AA
            )

        # ----------------------------------------------
        # Blend Overlay
        # ----------------------------------------------

        img = cv2.addWeighted(
            overlay,
            get_alpha(),
            img,
            1 - get_alpha(),
            0
        )

        return img

    # ----------------------------------------------------

    def get_image_ids(self):

        return list(self.images.keys())

    # ----------------------------------------------------

    def get_image_info(self, image_id):

        return self.images[image_id]